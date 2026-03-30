---
name: find-session
description: Find a Claude Code session matching a natural language description. Use when the user types /find-session, asks to "find a session", "search sessions", or wants to resume a past conversation.
---

Find a Claude Code session matching a natural language description.

usage: `/find-session <description>` — pass `--all` to search across all projects

```bash
python3 ~/.claude/commands/find-session.py $ARGUMENTS
```

Present the output verbatim. If the user picks a session, give them the `claude --resume <id>` command.
