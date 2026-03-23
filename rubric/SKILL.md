---
name: rubric
description: Evaluate code, features, or any work against a dynamically generated domain-specific rubric. Use when the user types /rubric, asks to "evaluate", "score", "grade", or "run a rubric against" something.
---

# Rubric

Evaluate whatever is in context against a rigorous, domain-specific rubric generated on the fly. No static checklists — criteria are tailored to the specific thing being evaluated.

## Step 1: Determine What to Evaluate

Resolve the target in this order:

1. **Arguments provided** — if the user passed a path or description (e.g., `/rubric src/auth/middleware.ts` or `/rubric the caching layer`), use that. Read the referenced files. If a directory is passed, read all files in it. If the path doesn't exist, tell the user and ask for clarification.
2. **No arguments, check git diff** — run `git diff` and `git diff --cached` to find recent unstaged/staged changes. If the diff spans multiple unrelated changes, ask the user which to focus on. If it's a cohesive change, evaluate the whole diff.
3. **Conversational reference** — if the user references something from the conversation (e.g., `/rubric the thing we just built`), use conversation context to identify the relevant files. If the context clearly identifies specific files, proceed. If the reference is ambiguous, confirm with the user.
4. **No arguments, no diff, no context** — ask the user what to evaluate. Do not guess.

**Scoping:** If the target exceeds ~10 files or ~1000 lines, identify the most critical files and evaluate those in depth rather than all files superficially. State what was evaluated and what was excluded. Skip binary files and non-text content in diffs. If the user references a specific function or section within a file, focus the evaluation on that scope but consider its context within the broader file.

Once you have the target, read all relevant code thoroughly. Do not skim. You need deep understanding to generate good criteria and score accurately.

## Step 2: Generate the Rubric

First, identify the artifact's **domain**, **primary concerns**, and **failure modes**. What could go wrong with this specific thing? What does "good" look like for this kind of artifact? Derive criteria from those concerns — not from a generic mental checklist.

Generate **5-8 criteria** specific to this domain and this artifact.

Draw criteria from these four types (not all apply every time — pick what's relevant):

For **code**:
- **Product** — correctness, completeness, edge case handling, API design, error handling, data validation, type safety
- **Process** — separation of concerns, naming, idiomatic patterns, code organization, DRY, single responsibility
- **Impact** — performance, security, accessibility, UX, reliability
- **Meta** — testability, maintainability, extensibility, readability by others

For **non-code artifacts** (docs, specs, configs, prompts, designs):
- **Product** — content accuracy, completeness, internal consistency
- **Process** — structure, organization, logical flow, appropriate level of detail
- **Impact** — usefulness to its audience, clarity of actionable guidance, fitness for purpose
- **Meta** — maintainability over time, adaptability to changing needs, discoverability

Use the vocabulary of the domain:
- A React component rubric talks about re-renders, hook rules, prop drilling
- A database migration rubric talks about reversibility, data integrity, index impact
- A CLI tool rubric talks about exit codes, help text, argument parsing
- A prompt/skill rubric talks about ambiguity, edge case coverage, instruction clarity, LLM steering effectiveness
- A config file rubric talks about default safety, environment separation, secret handling
- A design doc rubric talks about constraint completeness, alternative analysis, dependency identification

**Example criteria by domain** (for calibration — do not copy these verbatim, derive your own from the artifact's actual concerns):
- **API endpoint**: input validation coverage, error response contract, idempotency guarantees, authentication boundary, response payload design
- **Vue component**: prop interface design, reactivity correctness, render efficiency, accessibility, slot/emit contract
- **LLM prompt**: instruction unambiguity, edge case coverage, output format enforceability, resistance to default model tendencies, domain vocabulary precision
- **Config file**: default safety, secret separation, environment-aware overrides, validation on load, documentation of non-obvious values

**When generating criteria, rank them by criticality** — which ones, if they fail, cause the most damage? This ranking must be visible in the output (see summary table format) and feeds directly into the priority fixes. Use **High** (failure here causes significant damage), **Medium** (causes inconvenience or quality issues), or **Low** (nice-to-have improvement).

**Criteria must be:**
- Observable and measurable — not "good quality" but "error paths return meaningful messages"
- Specific to the domain — if you could copy-paste the criterion name to any codebase and it would make equal sense, it's too generic
- Distinguishable — no overlapping criteria that measure the same thing

**Scale (always 1-5):**

| Score | Meaning |
|-------|---------|
| 1 | Poor — fundamentally broken or missing |
| 2 | Below expectations — works but has significant issues |
| 3 | Adequate — meets basic expectations, room for improvement |
| 4 | Good — solid implementation, minor issues only |
| 5 | Excellent — actively searched for problems and found nothing meaningful |

Do not grade on a curve. Do not be generous. A 3 is the baseline for "it works and is acceptable." Most decent work lands between 3-4. A 5 requires that you actively looked for flaws and found nothing.

## Step 3: Score Each Criterion

For each criterion, produce this structure in order:

1. **Reasoning** — what the artifact does well and where it falls short. Reference specific lines, sections, patterns, or content. Be concrete. Lead with what it does, then what it misses. At minimum, identify one specific strength and one specific weakness with references — a single sentence is not sufficient reasoning. This section does the actual thinking — it must come before the score to avoid anchoring.
2. **Score: X/5** — after writing the reasoning, re-read it. If you described a real flaw, that's a 3, not a 4. If you found no concrete flaw to point at, that's a 4. A 5 requires you to have actively searched for problems and found nothing. Err toward the lower score when in doubt.
3. **Suggestion** — one specific, actionable improvement. Not "consider improving error handling" but "the catch block on line 47 swallows the database connection error — propagate it or log with context."

## Step 4: Summarize and Prioritize

After all criteria are scored:

1. **Sanity check** — review your scores before writing the summary. If all criteria scored the same value, you're not differentiating enough — go back and adjust your weakest and strongest criteria before proceeding. If everything is 4+, re-read your reasoning sections: did you actually name flaws? If so, the scores are inflated — go back and lower them to match the reasoning.
2. **Summary table** — all criteria with criticality and scores, plus an overall score. Use a simple average unless criticality is uneven, in which case weight accordingly and note it.
3. **Priority fixes** — a ranked list of the top 3-5 improvements, ordered by impact (lowest score x highest criticality first). Each item must be a concrete action, not a restatement of the criterion.

## Output Format

```markdown
## Rubric: [concise name for what's being evaluated]
[one line: what this is and what scope was evaluated]

### 1. [Criterion Name]
[Reasoning: what it does well, then what it misses. Specific references. At least one strength and one weakness.]

**Score: X/5**

Suggestion: [concrete improvement]

### 2. [Criterion Name]
...

(repeat for all criteria)

---

## Summary

| # | Criterion | Criticality | Score |
|---|-----------|-------------|-------|
| 1 | ...       | High        | X/5   |
| 2 | ...       | Medium      | X/5   |
| ... | ...     | ...         | ...   |
|   | **Overall** |           | **X.X/5** |

## Priority Fixes
1. [highest impact action]
2. [next]
3. [next]
```

## Rules

- **One suggestion per criterion.** The priority fixes list handles prioritization — each criterion gets its single best improvement.
- **Read deeply before scoring.** Follow the code paths. Check what functions are called. Look at the types. Don't score based on surface-level pattern matching.
