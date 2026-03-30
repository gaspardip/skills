---
name: rubric2
description: Iterative quality convergence loop. Runs /rubric repeatedly, fixing issues and simplifying between rounds, until a target score is reached or diminishing returns are detected. Use when the user types /rubric2, asks to "converge", "iterate rubric", or wants to push code quality to a target score.
---

# Rubric Squared

Run the rubric skill in a convergence loop: evaluate → fix → simplify → re-evaluate, until the code reaches a target quality or further improvement isn't worth it.

## Invocation

- `/rubric2` — converge with defaults (target 4.5/5, auto-detect scope)
- `/rubric2 src/auth/` — converge on specific path
- `/rubric2 4.0` — converge to custom score threshold
- `/rubric2 4.0 src/auth/` — both
- `/rubric2 4.0 the caching layer` — threshold 4.0, description "the caching layer"

Parse arguments: if the first argument is a number between 1.0 and 5.0 (with optional decimal), it is the target threshold. If the first argument is not a number, treat the entire argument string as scope and use the default threshold (4.5). Everything after the threshold is passed as a single scope argument to the rubric skill — it can be a path, a description, or both. Reject threshold values outside 1.0-5.0.

## Execution Mechanics

- **Rubric evaluation**: dispatch a subagent (via Agent tool) to evaluate. The subagent receives only the file paths (and the locked criteria from round 1, if applicable) — never the conversation history, fix rationale, or diffs. This ensures the evaluator scores the artifact cold, without authorship bias from the fixing agent. The subagent follows the rubric skill's full process and returns the complete rubric output. If subagent dispatch fails, abort the loop — do not fall back to inline evaluation. **Expected output from subagent**: overall score, per-criterion scores with names and criticality, criteria definitions (for locking), priority fixes list, and file list evaluated.
- **Simplify**: after fixes, review the changed code for opportunities to reduce complexity — remove dead code, flatten unnecessary nesting, consolidate duplication, simplify conditionals. Scope to the locked file list and limit to changes made during the current round's fix step. Do not invoke `/simplify` as a separate command.
- **Change log**: maintain a running list of fixes as you go. After each fix, append a bullet describing what changed and why. This log is emitted in the final output.

## The Loop

### Round 1: Baseline

1. Dispatch a subagent (via Agent tool, which starts a fresh context) to evaluate the target (rubric's resolution: args > git diff > conversation > ask). Pass only file paths — no conversation context about intent or changes. If the Agent tool is unavailable, abort — do not fall back to inline evaluation.
2. Record the **file list** evaluated and the **criteria generated** — both are locked for all subsequent rounds.
3. Record the overall score and per-criterion scores as the baseline.
4. Check stop conditions (below). If already met, stop and emit the baseline rubric as the final output (skip convergence summary).
5. Fix the issues listed in the Priority Fixes, working top-down by impact. Append each fix to the change log.
6. Simplify the locked files, focusing on changes made in step 5. If no simplification needed, note "no-op" in round status.
7. Print a one-line round status (format below).

### Round N (N > 1): Iterate

1. Dispatch a subagent to re-evaluate the **locked file list** using the **same criteria** from round 1. Pass the file paths and full criteria definitions (not just names) — not the fix rationale or change log. Criteria names and definitions stay fixed — only scores change. If a criterion becomes irrelevant due to fixes, exclude it from the overall score calculation rather than scoring it 5/5 (which would inflate the average).
2. Record the new overall score and per-criterion scores.
3. Check stop conditions. If any triggers, stop.
4. Fix the Priority Fixes from this round's evaluation. Append each fix to the change log.
5. Simplify the locked files, focusing on changes made in step 4. If no simplification needed, note "no-op" in round status.
6. Print a one-line round status.

## Stop Conditions

Stop when **any** of these is true:

| Condition | Trigger | Rationale |
|-----------|---------|-----------|
| **Target reached** | Overall score >= threshold (default 4.5/5) | Goal achieved |
| **Plateau** | Score delta < 0.3 between consecutive rounds (applies from round 2 onward) | Not worth another pass |
| **Stuck criteria** | Majority of criteria score identically for 2 consecutive rounds despite attempted fixes | Can't improve this further |
| **Regression** | Overall score drops vs. previous round | Making things worse |
| **Hard cap** | 5 rounds completed | Safety valve for token cost |

When stopping, note which condition triggered.

## Output

### During execution — one line per round:

```
Round 1: 2.8/5 (baseline, 6 criteria)
Round 2: 3.4/5 (+0.6, fixed 4 issues, simplified)
Round 3: 3.9/5 (+0.5, fixed 2 issues, simplified)
Round 4: 4.2/5 (+0.3, fixed 2 issues, simplified)
Round 5: 4.3/5 (+0.1) — stopped: plateau (delta 0.1 < 0.3)
```

### Final output:

1. **Full rubric** from the last round (standard rubric output format with criteria, scores, suggestions).
2. **Convergence summary**:
   ```
   ## Convergence Summary
   Start: 2.8/5 → End: 4.3/5 (+1.5)
   Rounds: 5 | Stop reason: plateau
   Total fixes applied: 11
   ```
3. **Change log** — cumulative bullet list of all fixes applied across all rounds, grouped by round:
   ```
   ### Round 1
   - Extracted validation into `validate.ts` (criterion: separation of concerns)
   - Added error context to catch block on line 47 (criterion: error handling)
   ### Round 2
   - ...
   ```

## Rules

- **Lock the scope.** Round 1 determines the file list. If fixes create new files, add them to the scope. If fixes delete files, remove them. The lock prevents scope drift from re-evaluation, not from the consequences of fixes.
- **Fix then simplify.** Always fix rubric issues before simplifying. Simplify cleans up the fix, not the other way around.
- **Don't re-fix what's already fixed.** If a priority fix from a previous round was already addressed, skip it. Focus on new or persistent issues.
- **Respect the rubric's scoring.** Do not inflate scores. Do not argue with the rubric. The rubric is the source of truth for each round.
- **One priority fix item per change.** Apply fixes incrementally. Don't bundle unrelated priority fix items in a single change.
- **Show your work.** The per-round status line must be printed before proceeding to the next round so the user can see progress in real time.
