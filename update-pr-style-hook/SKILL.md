---
name: update-pr-style-hook
description: Add a new LLM-ism pattern to the PR comment style hook. Use when the user types /update-pr-style-hook, spots a new LLM phrase that should be blocked, or wants to expand the PR comment style filter.
---

Add a new LLM-ism pattern to the PR comment style hook.

usage: `/update-pr-style-hook <offending phrase or pattern>`

examples:
- `/update-pr-style-hook "I've shipped the fix"`
- `/update-pr-style-hook "meticulously"`
- `/update-pr-style-hook "It bears mentioning"`

## instructions

1. if `$ARGUMENTS` is empty, ask what phrase to add and stop
2. read the hook file at `~/.claude/hookify.pr-comment-style.local.md`
3. extract the `pattern` field from the second condition (the LLM-ism regex)
4. test whether `$ARGUMENTS` is already caught by the current pattern:
   ```bash
   python3 -c "import re; print('ALREADY CAUGHT' if re.search(r'''<current_pattern>''', '''$ARGUMENTS''') else 'NOT CAUGHT')"
   ```
5. if already caught, say so, show which part of the pattern matches, and stop
6. determine the right way to add it:

   **category: self-narration** (`I've \w+`, `I'll \w+`, etc.)
   - these use `\w+` wildcards, so any "I've <word>" is already caught
   - if the phrase is "I've <word>", it's already covered — tell the user

   **category: adverb inflation** (`significantly `, `fundamentally `, etc.)
   - add the adverb followed by a space: `newadverb `
   - insert near the other adverbs in the pattern

   **category: upgraded verbs** (`leverag(e|ing|es)`, `utiliz(e|ing|es)`, etc.)
   - add all conjugations: `newverb(e|ing|es|ed)` or `newverb(s|ing|ed)`
   - insert near the other verbs in the pattern

   **category: buzzword adjectives** (` crucial `, ` robust `, etc.)
   - add with leading space: ` newadj ` or `newadj ` for start-of-phrase
   - insert near the other adjectives

   **category: formal connector** (`Additionally`, `Furthermore`, etc.)
   - add capitalized form
   - insert near the other connectors

   **category: filler phrase** (`It's worth noting`, `Please note`, etc.)
   - add the full phrase
   - insert near similar phrases

   **category: new** (doesn't fit above)
   - add as a new top-level alternative with `|`
   - add at the end of the pattern

7. escape any regex special characters in the phrase if it's meant as a literal match (`.` -> `\.`, `(` -> `\(`, etc.)
8. update the message body: add a rewrite example for the new pattern if it's common
9. verify the updated regex compiles:
   ```bash
   python3 -c "import re; re.compile(r'''<updated_pattern>''')"
   ```
10. verify the original phrase is now caught:
    ```bash
    python3 -c "import re; print('CAUGHT' if re.search(r'''<updated_pattern>''', '''$ARGUMENTS''') else 'STILL MISSED')"
    ```
11. if either verification fails, revert the change and report the error
12. write the updated file
13. show a summary:
    - what was added
    - which category it was added to
    - the original phrase confirmed as caught
    - a suggested rewrite for the phrase

## rules

- never add duplicates — always test first
- prefer broadening existing patterns over adding narrow ones
- preserve the pattern's readability — group related items
- always verify compile + match before saving
- if the phrase contains no LLM-ism (user misidentified), say so and suggest why it might be fine
- the hook file path is `~/.claude/hookify.pr-comment-style.local.md`
