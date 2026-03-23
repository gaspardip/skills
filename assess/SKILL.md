---
name: assess
description: Deep project-level assessment of an entire codebase. Use when the user types /assess, asks to "assess the project", "evaluate the codebase", or wants a comprehensive project-level evaluation. For bounded scope (file, diff, function), use /rubric instead.
---

# Assess

Map an entire project, generate assessment categories from its actual concerns, build an investigation checklist per category, and evaluate each with evidence-tagged findings and severity-tagged issues.

## Step 1: Map the Project

1. **Read structure** — `ls` root, scan key directories, read manifest (package.json / Cargo.toml / pyproject.toml / etc). Determine: web app, API, CLI, library, monorepo, mobile app.
2. **Identify stack** — language(s), framework(s), database(s), infra, key deps.
3. **Read key files** — entry points, main config, README, CLAUDE.md, CI config, schema/migrations. Read enough to understand the architecture, not everything.
4. **Present overview** — summarize what you found before evaluating. Let the user correct misunderstandings first.

**Monorepos / multi-project repos:** ask which sub-project to assess, or assess top-level orchestration if they want a holistic view. **No manifest file:** find entry points from build config, Makefile, or directory structure.

## Step 2: Generate Categories and Investigation Plans

Generate **5-8 categories** from the project's actual concerns. No fixed list — a CLI tool doesn't need "Event Architecture."

Example categories by project type (calibrate, don't copy):
- **Web app**: architecture & layering, data model & persistence, auth, error handling & resilience, frontend quality, test coverage, deployment & config
- **API service**: endpoint design & contracts, input validation & security, data access patterns, error responses, auth boundaries, observability, tests
- **CLI tool**: arg parsing & help text, error messages & exit codes, input validation, output formatting, cross-platform, tests
- **Library**: API surface design, docs & examples, backwards compatibility, edge cases, tests, bundle size

Skip irrelevant categories entirely. Use N/A only for borderline-relevant ones.

**Always include a Dependency & Runtime Currency category** when the project has a manifest file. Check the main runtime, primary framework, and up to 2 architecturally central dependencies. Compare installed vs latest stable versions.

**Rank by criticality:** **High** (failure = significant damage), **Medium** (quality issues), **Low** (nice-to-have).

**For each category, generate 4-8 specific investigation points** based on the project's stack — concrete things you will check, not abstract concerns. These make the evaluation exhaustive and transparent. Example: for "Security" in an Express + Postgres app, investigation points might be: SQL injection vectors in query construction, auth middleware coverage across routes, secret handling in config/env, input sanitization on user-facing endpoints, CORS configuration, rate limiting on auth endpoints.

**Reading strategy varies by category.** Architecture needs broad reading across many files. Auth needs deep reading into a specific area. Adjust per category.

## Step 3: Evaluate Each Category

For each category, produce **investigation points**, **findings**, **issues**, **score**, **top suggestion** — in that order.

**Investigation points** — list what you checked. This makes the evaluation accountable — the user can see what was covered and spot gaps.

**Findings** — strengths and observations about the project's approach. Tag every substantive finding:
- `[Observed]` — you can point to a specific file/line that shows this
- `[Inferred]` — concluded from patterns or absence; no single line proves it
- `[Not verifiable]` — requires running the app, checking external services, or info not in the repo

Do not present inferences as facts.

**Issues** — specific, actionable problems that should be fixed. Tag with severity:
- `[Critical]` — security vuln, data loss risk, broken functionality
- `[Major]` — significant quality or reliability problem
- `[Minor]` — noticeable but low-impact
- `[Nit]` — style/preference, not a real problem

Reference specific files and lines. No vague issues.

**Score: X/5** — 1=poor, 2=below expectations, 3=adequate, 4=good (no concrete flaw), 5=excellent (actively searched, found nothing). After writing findings, re-read: if you described real issues, that's a 3, not a 4. Err lower when in doubt.

**Top suggestion** — single highest-impact improvement for this category.

## Step 4: Devil's Advocate Pass

After completing your evaluation, dispatch a subagent with this prompt:

> You are a devil's advocate reviewer. Read the project at [path] and the assessment below. Your job is to find things the assessment was too generous about, missed entirely, or where evidence was tagged `[Observed]` but should be `[Inferred]`. For each finding, cite specific files/lines. Only report genuine disagreements — don't nitpick for the sake of it.

Feed the subagent your full assessment output and the project path. When it returns:
- If it found real issues you missed, add them to the relevant categories and adjust scores downward.
- If it caught inflated evidence tags, correct them.
- If it disagrees but you stand by your evaluation, note the disagreement in the category as `**Contested:** [what the advocate flagged and why you disagree]`.

This step catches the generosity bias that a single-pass evaluation can't self-correct.

## Step 5: Summarize and Prioritize

1. **Sanity check** — if all scores are the same or all 4+, go back and adjust before proceeding.
2. **Summary table** — categories, criticality, scores, overall average.
3. **Priority fixes** — top 5 cross-cutting improvements (lowest score x highest criticality). Each with concrete action, impact (H/M/L), effort (H/M/L).

## Output Format

```markdown
## Assessment: [project name]
[what this is, stack, scope]

### Scope
**Inspected:**
- Root structure: `src/`, `config/`, `tests/`, ...
- Data layer: `src/db/schema.ts`, `migrations/`, ...
- Domain logic: `src/services/`, `src/models/`, ...
- API / routes: `src/routes/`, `src/handlers/`, ...
- Tests: `tests/unit/`, `tests/integration/`, ...
- Config: `package.json`, `.env.example`, `docker-compose.yml`, ...

**Excluded:** [what was skipped and why]

### 1. [Category Name]

**Checked:** [list of investigation points]

**Findings:**
- [Observed] ...
- [Inferred] ...

**Issues:**
- [Major] ...
- [Minor] ...

**Score: X/5**

**Contested:** [if advocate flagged something you disagree with: what they flagged and why you stand by your evaluation]

Top suggestion: [concrete action]

### N. Dependency & Runtime Currency

| Component | Role | Installed | Latest | Status |
|-----------|------|-----------|--------|--------|
| Node.js   | Runtime | 18.x | 22.x | Behind |
| Express   | Framework | 4.18 | 4.21 | Behind |

**Issues:**
- [Major] ...

**Score: X/5**

Top suggestion: [concrete action]

---

## Summary

| # | Category | Criticality | Score |
|---|----------|-------------|-------|
| 1 | ...      | High        | X/5   |
|   | **Overall** |          | **X.X/5** |

## Priority Fixes
| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | ...    | High   | Medium |
```

## Rules

- **Evidence tagging is not optional.** Every finding gets `[Observed]`, `[Inferred]`, or `[Not verifiable]`.
- **Severity tagging is not optional.** Every issue gets `[Critical]`, `[Major]`, `[Minor]`, or `[Nit]`.
- **Investigation points are not optional.** Every category lists what was checked before presenting findings.
- **Read strategically.** Entry points, key modules, config, tests. State what you inspected and excluded.
- **No fixed categories.** Generate from the project's actual concerns.
- **One suggestion per category.** Priority fixes table handles cross-cutting recs.
