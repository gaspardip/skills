---
name: deferred
description: Use when the user runs /deferred to review accumulated deferred work items, scan current or past sessions for deferrals, and create Linear tickets.
---

# Deferred Work Tracker

Track work the user explicitly defers during sessions and create Linear tickets for it.

## Two Behaviors

### 1. Tracking (passive, during any session)

Tracking behavior (trigger phrases, entry format, confirmation) is defined in CLAUDE.md. This section covers file-level details only.

**Deferred file location:** `~/.claude/projects/<project-key>/deferred.jsonl`

Where `<project-key>` is the current project directory with `/` replaced by `-` (matching Claude Code's convention, e.g., `-Users-gaspar-src-creator`). If no project key exists for the cwd, derive one from the cwd path using the same convention.

**File format rules:**
- Lines starting with `#` are config/comments — skip when reading entries. Only one `# config:team=<team-name>` line should exist per file; overwrite it when the user picks a different team.
- All other lines are JSON entries, one per line
- Skip lines that fail JSON parse and warn: "Skipped N malformed entries in deferred.jsonl"

### 2. Review & Create (on `/deferred` invocation)

#### `/deferred` (no args)

1. Verify Linear MCP is available by calling `list_teams`. If it fails, warn the user and offer review-only mode (show list, allow discard, but no ticket creation). Entries remain in the file for later.
2. Read `~/.claude/projects/<project-key>/deferred.jsonl` (skip `#` lines, skip malformed JSON lines)
3. If empty or missing: "Nothing deferred."
4. Show the list as a numbered table: `#`, `Summary`, `Context`, `When`. Flag items older than 30 days with `[stale]` in the When column.
5. Ask the user to review. Accepts batch commands: "all" (approve everything), "approve 1,3,5", "discard 2,4", "edit 3: new summary here" (inline edit). Unapproved/unmentioned items remain in the file.
6. For approved items, create Linear tickets:
   - **Team**: Check if `# config:team=<team-name>` exists in deferred.jsonl. If so, use that team. Otherwise, call `list_teams` and attempt to match the working directory name, repository name, or git remote to a team. If no confident match (not just ambiguous — zero match counts too), ask the user which team to use. Cache their choice by writing `# config:team=<team-name>` as the first line of deferred.jsonl. If the user specifies a different team during review, overwrite the existing `# config:team=` line.
   - **Title**: the summary
   - **Description**: the context, plus a footer: `> Deferred on <timestamp> in \`<project>\` (branch: \`<branch>\`, at \`<sha>\`)`
   - **State**: "Backlog"
   - **Labels**: ["Deferred"] — if the label doesn't exist yet, create it as a workspace label (color: `#95a2b3`)
   - **Priority**: 4 (Low)
6. Report created tickets with their identifiers (e.g., `CRE-123`)
7. Remove processed entries (approved + discarded) from the file. Keep only items not yet reviewed and `#` config lines. Re-read the file immediately before rewriting to pick up any entries appended by other sessions since the initial read — new entries not in the original review set must be preserved.

#### `/deferred scan`

Scan the current conversation for deferred work that wasn't tracked.

1. Read through the conversation looking for explicit deferral decisions — the user making a deliberate choice to postpone specific work. Look for deferral verbs paired with a task-like object: "skip [the/that/this] + [noun]", "defer [noun/gerund]", "[verb] that later", "punt on [noun]", "come back to [noun]".
2. Ignore figures of speech and conversational filler: "I'll explain later", "later in this file", "see below", "added later". If a match looks like speech rather than a decision to postpone work, skip it.
3. After context compaction, earlier deferrals may only appear in summaries — check those too.
4. Cross-reference against existing entries in `deferred.jsonl` to avoid duplicates.
5. Present found items for approval.
6. Approved items get appended to `deferred.jsonl` (not directly to Linear — user runs `/deferred` for that).

#### `/deferred scan-history`

Scan past conversation transcripts for the current project.

1. Find JSONL transcript files in `~/.claude/projects/<project-key>/` (only files modified in the last 30 days by default; accepts `--since <date>` to override)
2. Dispatch a subagent (see scan-history-prompt.md) to parse transcripts and extract deferrals
3. Present found items for approval
4. Approved items get appended to `deferred.jsonl`

#### `/deferred --all`

Show deferred items across all projects.

1. Glob `~/.claude/projects/*/deferred.jsonl` to find all projects with deferred items.
2. Read and merge entries, grouped by project in the review table.
3. Same review & create flow, but resolve the Linear team per project independently (each project may have its own `# config:team=` or need separate inference).

## Linear Tools Reference

- `mcp__linear-mcp__list_teams` — find the right team
- `mcp__linear-mcp__save_issue` — create tickets (title, team, description, state, labels, priority)
- `mcp__linear-mcp__list_issue_labels` — check if "Deferred" label exists
- `mcp__linear-mcp__create_issue_label` — create "Deferred" label if needed

## Common Mistakes

- Don't create tickets without user review — always show the list first
- Don't track vague deferrals — if the user says "maybe later" about something unclear, ask what specifically should be tracked
- Don't duplicate — check existing entries before appending
- Don't force a Linear team match — if there's no confident match, ask
