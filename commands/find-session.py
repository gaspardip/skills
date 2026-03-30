#!/usr/bin/env python3
"""find-session: Search Claude Code sessions by natural language description.

Scans JSONL session files under ~/.claude/projects/, extracts metadata from
the first N lines of each, and ranks by keyword relevance + completeness + recency.
No external dependencies.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
SCAN_LINES = 80  # lines to parse per session (metadata + first messages)
MAX_RESULTS = 7


@dataclass
class SessionInfo:
    project_key: str
    session_id: str
    cwd: str | None = None
    slug: str | None = None
    branch: str | None = None
    first_ts: str | None = None
    last_ts: str | None = None
    user_prompts: list[str] = field(default_factory=list)
    files_touched: list[str] = field(default_factory=list)
    file_size: int = 0
    mtime: float = 0.0
    msg_count: int = 0


def cwd_to_key(cwd: str) -> str:
    return cwd.replace("/", "-")


def detect_projects() -> list[str]:
    """Return project keys matching cwd and its children."""
    cwd = Path.cwd()
    cwd_key = cwd_to_key(str(cwd))
    keys: list[str] = []

    if not PROJECTS_DIR.is_dir():
        return keys

    for d in PROJECTS_DIR.iterdir():
        if not d.is_dir() or not any(d.glob("*.jsonl")):
            continue
        if d.name == cwd_key or d.name.startswith(cwd_key + "-"):
            keys.append(d.name)

    # Also check parents of cwd (e.g. running from ~/src/creator/src/js)
    if not keys:
        for path in cwd.parents:
            key = cwd_to_key(str(path))
            d = PROJECTS_DIR / key
            if d.is_dir() and any(d.glob("*.jsonl")):
                keys.append(key)
                break

    return keys


def shorten(path: str | None) -> str:
    if not path:
        return "?"
    home = str(Path.home())
    return "~" + path[len(home) :] if path.startswith(home) else path


def fmt_ts(ts: str | None) -> str:
    if not ts:
        return "?"
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%b %d %H:%M")
    except ValueError:
        return ts[:16]


def extract(jsonl: Path, project_key: str) -> SessionInfo | None:
    """Extract searchable metadata from a session JSONL."""
    stat = jsonl.stat()
    info = SessionInfo(
        project_key=project_key,
        session_id=jsonl.stem,
        file_size=stat.st_size,
        mtime=stat.st_mtime,
    )

    files_seen: set[str] = set()
    n = 0

    try:
        with open(jsonl) as f:
            for line in f:
                n += 1
                if n > SCAN_LINES:
                    for _ in f:
                        n += 1
                    break

                try:
                    e = json.loads(line)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue

                if not info.cwd and e.get("cwd"):
                    info.cwd = e["cwd"]
                if not info.slug and e.get("slug"):
                    info.slug = e["slug"]
                if not info.branch and e.get("gitBranch"):
                    info.branch = e["gitBranch"]
                if e.get("sessionId"):
                    info.session_id = e["sessionId"]

                ts = e.get("timestamp")
                if ts:
                    if not info.first_ts:
                        info.first_ts = ts
                    info.last_ts = ts

                # user messages
                if e.get("type") == "user" and "message" in e:
                    content = e["message"].get("content", "")
                    if isinstance(content, list):
                        content = " ".join(
                            c.get("text", "")
                            for c in content
                            if isinstance(c, dict) and c.get("type") == "text"
                        )
                    if content and not content.startswith("[Request interrupted"):
                        if len(info.user_prompts) < 5:
                            info.user_prompts.append(content[:300])

                # files from tool calls
                if e.get("type") == "assistant" and "message" in e:
                    blocks = e["message"].get("content", [])
                    if isinstance(blocks, list):
                        for b in blocks:
                            if isinstance(b, dict) and b.get("type") == "tool_use":
                                fp = b.get("input", {}).get("file_path", "")
                                if fp and fp not in files_seen:
                                    files_seen.add(fp)
    except (OSError, KeyError, UnicodeDecodeError):
        return None

    info.files_touched = list(files_seen)[:20]
    info.msg_count = n

    if not info.user_prompts:
        return None

    return info


# Lines that are boilerplate — skip when building preview
_BOILERPLATE = re.compile(
    r"^(implement the following plan|"
    r"\<local-command-caveat\>|"
    r"request interrupted|"
    r"---+|"
    r"##?\s*context)\s*:?\s*$",
    re.IGNORECASE,
)


def extract_preview(prompts: list[str]) -> str:
    """Pull the most descriptive line from the first user prompts."""
    for prompt in prompts:
        for line in prompt.split("\n"):
            line = line.strip()
            if not line:
                continue
            if _BOILERPLATE.match(line):
                continue
            if line.startswith("# "):
                return line[2:].strip()[:120]
            if line.startswith("## "):
                return line[3:].strip()[:120]
            return line[:120]
    return ""


def tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z][a-z0-9]*|[0-9]+", text.lower()) if len(t) > 1}


def score_session(query: str, qtoks: set[str], s: SessionInfo) -> float:
    sc = 0.0
    ql = query.lower()

    prompts = " ".join(s.user_prompts).lower()

    # exact substring in prompts
    if ql in prompts:
        sc += 50

    # token overlap — prompts (primary signal)
    ptoks = tokenize(prompts)
    if qtoks and ptoks:
        sc += (len(qtoks & ptoks) / len(qtoks)) * 40

    # token overlap — branch, slug, files (secondary, non-overlapping)
    branch = (s.branch or "").lower()
    slug = (s.slug or "").lower()
    files = " ".join(s.files_touched).lower()
    extra_only = tokenize(f"{branch} {slug} {files}") - ptoks
    if qtoks and extra_only:
        sc += (len(qtoks & extra_only) / len(qtoks)) * 10

    # completeness (capped at 3 pts)
    sc += min(s.msg_count / 50, 3)

    # recency tiebreaker
    days = (datetime.now().timestamp() - s.mtime) / 86400
    if days < 1:
        sc += 2
    elif days < 7:
        sc += 1
    elif days < 30:
        sc += 0.5

    return round(sc, 1)


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(
        prog="find-session",
        description="Search Claude Code sessions by description",
    )
    p.add_argument("query", nargs="*", help="keywords or description")
    p.add_argument("-a", "--all", action="store_true", help="search all projects")
    p.add_argument("-n", "--limit", type=int, default=MAX_RESULTS)
    args = p.parse_args()

    query = " ".join(args.query).strip()
    if not query:
        p.print_help()
        sys.exit(1)

    # --- scope ---
    if args.all:
        keys: list[str] = []
    else:
        keys = detect_projects()

    if keys:
        dirs = [PROJECTS_DIR / k for k in keys]
        scope = shorten(str(Path.cwd()))
    else:
        dirs = [d for d in PROJECTS_DIR.iterdir() if d.is_dir()] if PROJECTS_DIR.is_dir() else []
        scope = "all projects"

    # --- index ---
    sessions: list[SessionInfo] = []
    for d in dirs:
        pk = d.name
        for f in d.glob("*.jsonl"):
            info = extract(f, pk)
            if info:
                sessions.append(info)

    if not sessions:
        print(f"No sessions found ({scope})")
        sys.exit(1)

    # --- search ---
    qtoks = tokenize(query)
    scored = [(score_session(query, qtoks, s), s) for s in sessions]
    scored = [(sc, s) for sc, s in scored if sc > 5]
    scored.sort(key=lambda x: (-x[0], x[1].slug or "", -x[1].mtime))
    results = scored[: args.limit]

    if not results:
        msg = f"No matches in {scope} ({len(sessions)} sessions)"
        if keys:
            msg += ". Try: find-session --all ..."
        print(msg)
        sys.exit(0)

    # --- output ---
    print(
        f"{len(results)} match{'es' if len(results) != 1 else ''} "
        f"(searched {len(sessions)} in {scope})\n"
    )

    recommended_cmd: str | None = None
    prev_slug: str | None = None
    for i, (sc, s) in enumerate(results):
        is_rec = i == 0 and (len(results) == 1 or sc > results[1][0] * 1.3)
        pfx = "→" if is_rec else " "

        slug = s.slug or "unnamed"
        resume_id = s.slug or s.session_id
        branch = s.branch or "?"
        cwd = shorten(s.cwd)
        ts = fmt_ts(s.first_ts)
        msgs = s.msg_count

        # Group consecutive sessions with the same slug
        slug_label = slug if slug != prev_slug else "  └─"
        prev_slug = slug

        preview = extract_preview(s.user_prompts)

        # Show UUID suffix only when slug is absent
        id_hint = f" ({s.session_id[:8]})" if s.slug else ""
        print(f"{pfx} {i + 1}. {slug_label}{id_hint}")
        print(f"     {cwd} | {branch} | {ts} | {msgs} msgs")
        if preview:
            print(f'     "{preview}"')
        resume_cmd = f"claude --resume {resume_id} --dangerously-skip-permissions"
        print(f"     {resume_cmd}")
        print()

        if is_rec:
            recommended_cmd = resume_cmd

    if results[0][0] < 12:
        print("(low confidence — try more specific keywords)")

    # Copy recommended resume command to clipboard
    if recommended_cmd:
        try:
            subprocess.run(
                ["pbcopy"], input=recommended_cmd.encode(), check=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            print(f"Copied to clipboard: {recommended_cmd}")
        except (OSError, subprocess.CalledProcessError):
            pass


if __name__ == "__main__":
    main()
