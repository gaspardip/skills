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
4. **Conversational artifact** — if the user asks to evaluate a plan, approach, architecture, or concept described in conversation (not in files), treat the conversation content as the artifact. Score against the same rubric structure — the artifact doesn't need to be a file.
5. **No arguments, no diff, no context** — ask the user what to evaluate. Do not guess.

**Scoping:** If the target exceeds ~10 files or ~1000 lines, identify the most critical files and evaluate those in depth rather than all files superficially. State what was evaluated and what was excluded. Skip binary files and non-text content in diffs. If the user references a specific function or section within a file, focus the evaluation on that scope but consider its context within the broader file. If the target has no evaluable content (empty diff, binary-only changes, or a concept that can't be scored against criteria), report this and ask the user for a different target.

**Diffs vs. files:** When evaluating a diff, score the changed code in the context of the surrounding file. The rubric applies to the changes, but the file context informs whether those changes are correct and complete.

**Polyglot artifacts:** When a change spans multiple languages or runtimes (e.g., TypeScript frontend + Python backend + SQL migration), identify the primary language for criterion generation and note which criteria apply language-specifically vs. cross-cutting.

Once you have the target, read all relevant code thoroughly. Before scoring, identify at least one downstream effect of each change (what breaks if this is wrong, what depends on this behavior). Do not score based on surface-level pattern matching.

## Step 2: Generate the Rubric

First, identify and **write out** the artifact's **domain**, **primary concerns**, and **failure modes** in the output. This block must appear before any criteria — it makes the derivation chain auditable. What could go wrong with this specific thing? What does "good" look like for this kind of artifact? Derive criteria from those concerns — not from a generic mental checklist.

Generate **one criterion per distinct concern** identified in the domain analysis above. If you end up with fewer than 4 or more than 8, revisit whether you're splitting too fine or lumping too broad. For trivially small artifacts (under ~20 lines), 2-3 focused criteria may be sufficient — do not pad to reach a minimum. If the artifact spans multiple domains (e.g., a component that also handles API calls and caching), pick the primary domain for criterion generation but let secondary domains inform 1-2 additional criteria.

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

**Example criteria by domain** (for calibration — do not copy these verbatim, derive your own from the artifact's actual concerns):
- **API endpoint**: input validation coverage, error response contract, idempotency guarantees, authentication boundary, response payload design
- **LLM prompt**: instruction unambiguity, edge case coverage, output format enforceability, resistance to default model tendencies, domain vocabulary precision

**When generating criteria, rank them by criticality** — which ones, if they fail, cause the most damage? This ranking must be visible in the output (see summary table format) and feeds directly into the priority fixes. Use **High** (failure here causes significant damage), **Medium** (causes inconvenience or quality issues), or **Low** (nice-to-have improvement).

**Criteria must be:**
- Observable and measurable — not "good quality" but "error paths return meaningful messages"
- Specific to the domain — if you could copy-paste the criterion name to any codebase and it would make equal sense, it's too generic
- Distinguishable — no overlapping criteria that measure the same thing

**Scale (always 1-5):**

| Score | Meaning | Code example (error handling) | Non-code example (documentation) |
|-------|---------|-------------------------------|----------------------------------|
| 1 | Poor — fundamentally broken or missing | No error handling; exceptions crash the process | Key sections missing; contradicts the actual behavior |
| 2 | Below expectations — significant issues | Catch blocks swallow errors silently | Covers happy path only; outdated after recent changes |
| 3 | Adequate — meets basic expectations | Errors caught and logged, but messages are generic | Accurate and structured, but lacks edge cases and examples |
| 4 | Good — minor issues only | Actionable messages; edge cases handled; one retry path unclear | Complete, with examples; one section could be clearer |
| 5 | Excellent — found nothing meaningful | Every path tested, messages specific, recovery logic documented | Comprehensive, current, with runnable examples and caveats |

Do not grade on a curve. Do not be generous. A 3 is the baseline for "it works and is acceptable." Most decent work lands between 3-4. A 5 requires that you actively looked for flaws and found nothing.

## Step 3: Score Each Criterion

For each criterion, produce this structure in order:

1. **Reasoning** — what the artifact does well and where it falls short. Reference specific lines, sections, patterns, or content. Be concrete. Lead with what it does, then what it misses. At minimum, identify one specific strength and one specific weakness with references — a single sentence is not sufficient reasoning. For High-criticality criteria, address at least two specific aspects and explain the failure impact if the weakness were triggered. This section does the actual thinking — it must come before the score to avoid anchoring.
2. **Score: X/5** — after writing the reasoning, re-read it. If you described a real flaw, that's a 3, not a 4. If you found no concrete flaw to point at, that's a 4. A 5 requires you to have actively searched for problems and found nothing — enumerate what you checked (e.g., "checked error paths, boundary inputs, concurrent access, and naming consistency — no issues found"). Err toward the lower score when in doubt. If you lack sufficient domain knowledge to evaluate a criterion confidently, state this explicitly, score it 3/5 (baseline), and note "limited confidence" in the summary.
3. **Suggestion** — one specific, actionable improvement. Not "consider improving error handling" but "the catch block on line 47 swallows the database connection error — propagate it or log with context."

Do not manufacture weaknesses to justify a lower score. If genuine analysis finds no concrete flaw but you lack full confidence in your thoroughness, score 4 — reserve 5 for verified thoroughness with enumerated checks. The calibration examples in this prompt are for illustration only — never copy them verbatim into your output.

## Step 4: Summarize and Prioritize

After all criteria are scored:

1. **Sanity check** — review your scores before writing the summary. If all criteria scored the same value, you're not differentiating enough — go back and adjust your weakest and strongest criteria before proceeding. If everything is 4+, re-read your reasoning sections: did you actually name flaws? If so, the scores are inflated — lower them to match the reasoning. If your reasoning genuinely found no concrete flaws, the scores are valid — the sanity check guards against inflation, not against acknowledging good work.
2. **Summary table** — all criteria with criticality and scores, plus an overall score. Compute as `sum(score × weight) / sum(weight)` where High=3, Medium=2, Low=1. If any High-criticality criterion scores ≤2, flag it explicitly in the summary regardless of the overall score.
3. **Priority fixes** — a ranked list of the top 3-5 improvements, ordered by impact. Rank by `(5 - score) * criticality_weight` where High=3, Medium=2, Low=1. Each item must be a concrete action, not a restatement of the criterion.
4. **Verdict** — one line: `≥4.0` ship as-is, `3.0–3.9` fix priority items before shipping, `<3.0` rework needed.

## Output Format

```markdown
## Rubric: [concise name for what's being evaluated]
[one line: what this is and what scope was evaluated]

**Domain:** [domain name]
**Primary concerns:** [2-4 bullet points]
**Failure modes:** [what goes wrong if this is bad]

### 1. [Criterion Name]
[Reasoning: what it does well, then what it misses. Specific references. At least one strength and one weakness.]

**Score: X/5**

Suggestion: [concrete improvement]

(repeat for all criteria)

---

## Summary

| # | Criterion | Criticality | Score |
|---|-----------|-------------|-------|
| 1 | ...       | High        | X/5   |
| 2 | ...       | Medium      | X/5   |
|   | **Overall** |           | **X.X/5** |

## Priority Fixes
1. [highest impact action]
2. [next]
3. [next]

**Verdict:** [≥4.0 ship | 3.0–3.9 fix first | <3.0 rework]
```

## Rules

- **One suggestion per criterion.** The priority fixes list handles prioritization — each criterion gets its single best improvement.
