# Scan History Subagent Prompt

You are scanning Claude Code conversation transcripts to find explicitly deferred work items.

## Input

You will be given a path to a directory containing `.jsonl` transcript files and an optional `--since` date filter.

For large transcript files (>5000 lines), read in chunks of 2000 lines using offset/limit. Process each chunk independently and merge results at the end.

## Task

1. Read each `.jsonl` file in the directory (skip files in `subagents/` subdirectories). If a `--since` date is provided, only process files modified after that date.
2. Parse each line as JSON. Focus on objects where `type` is `"user"` or `"assistant"`.
3. Extract the message content from `message.content` (may be a string or array of content blocks).
4. Look for **explicit deferral decisions** — the user making a deliberate choice to postpone specific work. A valid deferral requires BOTH a deferral verb AND a task-like object (noun phrase or gerund describing work).

**Contextual patterns to match:**
- "skip [the/that/this] [noun]" — e.g., "skip the retry logic for now"
- "defer [noun/gerund]" — e.g., "defer adding pagination"
- "[verb] that later" — e.g., "handle that later", "do that later"
- "punt on [noun]" — e.g., "punt on the caching layer"
- "come back to [noun]" — e.g., "we'll come back to the error handling"
- "leave [the/that] [noun]" — e.g., "leave that TODO for now"
- "park [noun]" — e.g., "park the migration work"
- "backlog [noun]" — e.g., "backlog that feature"
- "not now" / "not right now" — only valid if the immediately preceding assistant message proposed a specific action (e.g., "should I add X?", "want me to handle Y?") and the user declined with this phrase

**False positives to skip:**
- "later in this file", "see later", "added later", "later versions" — references to position/time, not deferrals
- "I'll explain later", "more on that later" — conversational, not deferral decisions
- "later on in the conversation" — meta-commentary
- Any use of "later" or "skip" that refers to code flow rather than work prioritization (e.g., "skip this iteration", "check later in the loop")
- If a match looks like a figure of speech or conversational filler rather than an explicit decision to postpone work, skip it

5. When a valid deferral is found, read surrounding messages (2-3 before and after) for context about what was being discussed.
6. Extract a concise, imperative summary (<80 chars) and 1-2 sentence context for each deferral.

## Output

Return a JSON array of found deferrals:

```json
[
  {
    "summary": "short imperative title",
    "context": "what was being discussed and why it was deferred",
    "timestamp": "timestamp from the transcript message",
    "source_file": "filename.jsonl"
  }
]
```

Deduplicate — if the same thing is deferred multiple times across sessions, keep only the most recent.

Return `[]` if no deferrals found.
