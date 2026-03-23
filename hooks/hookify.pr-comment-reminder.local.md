---
name: pr-comment-reminder
enabled: true
event: bash
conditions:
  - field: command
    operator: regex_match
    pattern: gh\s+(api\s+.*-f\s+body=|pr\s+(comment|create|review|edit)|issue\s+comment)
action: warn
---

**style check** - read your text as if a colleague wrote it. does it sound human or like a bot? lowercase, concise, no filler.
