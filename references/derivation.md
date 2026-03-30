# Voice Derivation

Complete all five fields before generating any prose. This commits the model to a specific voice basin rather than the default AI-academic register.

## The Five Fields

### 1. Reader Profile

Who reads this text, what they already know, and what they expect.

**Generic (bad):** "Academic audience"
**Specific (good):** "A political science professor who has read 200 of these assignments and can spot padding in the first paragraph. She values tight argumentation over breadth of coverage."

**Specific (good):** "A grading TA who skims introductions and reads conclusions first. They check whether claims in the conclusion actually appear in the body."

### 2. Register Target

Name a specific publication, author, or document type whose tone to match. This is the single most impactful field — it gives the model a concrete distribution to aim toward.

**Academic register examples:**
- "Annual Review of Psychology literature review" — authoritative, synthesizing, measured certainty
- "Nature methods section" — compressed, replicable, no commentary
- "Harvard Business Review research brief" — accessible rigor, practitioner-oriented
- "Journal of Philosophy close reading" — slow, precise, each sentence earned
- "NBER working paper" — technical but readable, author voice present
- "IEEE transactions" — dense, formal, equation-heavy
- "Sociology of Education empirical section" — theory-driven, variable-focused

### 3. Texture Vocabulary

The domain-specific material nouns that ground the text. These are the words that only someone in this field would use naturally.

**Economics:** basis points, yield curve, real terms, purchasing power parity, Gini coefficient
**Psychology:** effect size, ecological validity, demand characteristics, attrition, moderation analysis
**CS:** time complexity, cache invalidation, race condition, backpressure, idempotency
**Political Science:** median voter, veto player, path dependence, institutional isomorphism
**Sociology:** habitus, social reproduction, intersectionality, thick description
**Biology:** phenotypic plasticity, allelic frequency, knockout model, Western blot

Fill this field with 8-12 terms specific to the assignment's domain.

### 4. Scene Anchor

Where and when the reader encounters this text. This constrains formality, length expectations, and attention assumptions.

**Examples:**
- "Reading a printed stack of 30 assignments at a desk, coffee, pen in hand, marking in margins"
- "Skimming a PDF on a laptop between meetings, checking whether the methodology section is rigorous enough"
- "Reading carefully on a tablet, comparing this paper against two others on the same topic"

### 5. Voice Sample (when available)

If the user provides their own previous writing, extract these patterns:

- **Sentence length distribution** — short/medium/long ratio
- **Opening patterns** — how they start paragraphs (topic sentence? question? anecdote? data?)
- **Transition style** — explicit connectors? logical ordering? paragraph breaks?
- **Hedging level** — confident? cautious? evidence-qualified?
- **Pronoun usage** — "we argue" vs "this paper argues" vs "I contend"
- **Vocabulary range** — plain words? specialized? mixed?

Match these patterns. Do not improve them. The goal is consistency with the person's actual voice, not idealized academic prose.

## Derivation Example

**Assignment:** 3000-word group essay on EU climate policy effectiveness for a political science course.

```
reader:    Prof. Martínez, comparative politics, values empirical evidence over
           theoretical breadth, penalizes unsupported claims, reads conclusions first
register:  Comparative Political Studies empirical article — measured, data-driven,
           first-person-plural, theory-tested-against-cases
texture:   policy diffusion, regulatory stringency index, compliance gap,
           implementation deficit, Europeanization, carbon leakage,
           burden-sharing mechanism, nationally determined contributions
scene:     Reading PDF on laptop, pen and rubric in hand, 25 essays to grade
           this weekend, looking for clear thesis + evidence chain
voice:     [paste 1-2 paragraphs of a group member's previous essay]
```

This derivation makes it structurally difficult to produce generic AI prose because every sentence must contain texture vocabulary, match the register of Comparative Political Studies, and satisfy a reader who penalizes unsupported claims.
