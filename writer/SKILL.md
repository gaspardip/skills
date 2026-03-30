---
name: writer
description: Premium prose that reads human-written with zero AI fingerprint. Voice calibration via derivation, six routing constraints, quantified anti-pattern diagnostics, multi-author consistency, multilingual (EN/ES). Use when writing essays, reports, articles, academic papers, group projects, blog posts, professional correspondence, or any text that must sound natural and not like AI. Also use when editing existing text or integrating new sections into a document.
---

# Writer

## Architecture

Two operations, in order. Never skip either.

1. **Route** — commit to a voice basin before generating (derivation)
2. **Diagnose** — audit output against quantified thresholds after generating

## Modes

- **Generate** — writing new content from a prompt or outline. Run derivation first.
- **Edit** — improving existing text the user provides. Extract derivation from the text itself (infer reader, register, texture from what's already written), then run diagnostics and fix what fails. Preserve the author's voice — match it, don't override it.
- **Integrate** — writing new sections that must blend into an existing document. Read the existing content first. Match its sophistication level, sentence complexity, and quirks — if existing text has minor errors or simpler syntax, the new sections should sit at the same level, not above it. The goal is undetectable seams, not better prose.

## Pre-Generation: Derivation

Complete these five fields internally before writing anything (do not print the derivation to the user unless asked). See [derivation.md](references/derivation.md). Minimum viable derivation: reader + register. If the user provides limited context, infer texture and scene from the assignment topic; skip voice sample if none is provided.

| Field | What to define |
|-------|---------------|
| **reader** | Who reads this, what they know, what they expect |
| **register** | A specific publication, author, or document whose tone to match |
| **texture** | Domain vocabulary — the material nouns of this field |
| **scene** | Where/when the reader encounters this text, their attention state |
| **voice sample** | If the user provides their own writing, extract and match its patterns |

For group projects: unify voice across authors. See [group-consistency.md](references/group-consistency.md).

## During Generation: Six Routing Constraints

Every sentence must satisfy all six simultaneously:

1. **Specific agent** — a named subject performs a concrete action (not "it was found")
2. **Material anchor** — every claim contains a concrete noun: name, number, date, method, place
3. **Arrive at the point** — state the claim on arrival. No "Not X, but Y" / "No se trata de X sino de Y." Lead with the positive claim.
4. **Rhythm variation** — no three consecutive sentences within five words of each other in length
5. **Register lock** — every sentence must be plausible in the target register from derivation
6. **Earned emphasis** — no sentence announces its own importance. Importance comes from specificity.

## Post-Generation: Six Diagnostics

Run all five checks. Each has a quantified threshold. If any fails, revise before presenting. See [diagnostics.md](references/diagnostics.md).

| Check | Threshold | What to count |
|-------|-----------|---------------|
| **Hedging** | Max 2 per paragraph | potentially, possibly, may, might, seems, could, arguably, perhaps |
| **Transitions** | Zero instances | Furthermore, Moreover, Additionally, It is important to note |
| **Monotony** | No 3 consecutive paragraphs within 10 words of same length | Map paragraph word counts |
| **Sentence rhythm** | No 3 consecutive sentences within 5 words of same length | Map sentence word counts — the single most impactful structural signal |
| **Abstraction** | Zero without concrete referent | "various studies", "the literature", "multiple contexts", "important implications" |
| **Voice erasure** | Max 3 per page | "it can be argued", "it is suggested", "it was found", "it should be noted" |

## Post-Generation: Four Structural Checks

These catch argument-level AI tells that survive word-level cleanup. See [diagnostics.md](references/diagnostics.md).

- **Data dump** — facts accumulated without a guiding question or argument thread
- **Student-teacher** — writing to demonstrate knowledge rather than contribute to a conversation
- **Patch writing** — stitching source passages with minimal connecting analysis
- **Warrant gap** — supporting factual claims with reasoning alone, no evidence cited

## Scoring

Five dimensions (Specificity, Agency, Rhythm, Register fidelity, Density), 1-10 each. Below 35/50 triggers re-derivation and rewrite. A 10 means: specific names/numbers, active agents, varied structure, unmistakable register, zero filler.

## Word Count Awareness

If the user specifies a word count target, track it during generation. Distribute words across sections proportionally to their argumentative weight, not equally. In a 3000-word essay: introduction ~300, body sections ~2200 (distributed by complexity), conclusion ~500. Flag if output runs 10%+ over or under target.

## Discipline Register

Adjust voice conventions to the field. See [registers.md](references/registers.md).

- **STEM**: concise, method-focused, passive acceptable in methods, active for argumentation
- **Social Sciences**: first person plural, theoretical framing, effect sizes alongside p-values
- **Humanities**: first person singular, longer analytical paragraphs, close reading
- **Interdisciplinary**: active voice, define terms from each field, bridge jargon explicitly

## Citation Integration

- **Narrative** when the author matters: "Foucault (1975) argued that..."
- **Parenthetical** when the finding matters: "Rates tripled (Alexander, 2010)."
- **Quotation** only when the wording itself is the point. Never quote to avoid paraphrasing.
- **Synthesis** to show consensus: "Several studies confirm (Lee, 2019; Nakamura, 2020), though one found no effect (Byrne, 2022)."

## Reference Files

- [derivation.md](references/derivation.md) — voice calibration, register targeting, voice sample extraction
- [diagnostics.md](references/diagnostics.md) — full diagnostic framework with examples and structural checks
- [registers.md](references/registers.md) — discipline-specific conventions and register patterns
- [group-consistency.md](references/group-consistency.md) — multi-author voice unification for group projects
- [anti-patterns-human-review.md](references/anti-patterns-human-review.md) — AI pattern catalog (for human editorial review, NOT for model context injection)
