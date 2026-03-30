Find a Claude Code session matching a natural language description.

usage: `/find-session <description>` — pass `--all` to search across all projects

```bash
python3 ~/.claude/commands/find-session.py $ARGUMENTS
```

Present the output verbatim. If the user picks a session, give them the `claude --resume <id>` command.
