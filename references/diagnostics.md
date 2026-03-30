# Diagnostics

Two layers: sentence-level (5 checks) and argument-level (4 checks). Both must pass before presenting output.

## Layer 1: Sentence-Level Anti-Pattern Diagnostics

### 1. Hedging Soup

Stacking uncertainty markers drains every sentence of meaning.

**Threshold:** max 2 hedging words per paragraph.

**Words to count:** potentially, possibly, may, might, seems, could, arguably, perhaps, likely, conceivably, presumably, ostensibly, somewhat, tends to, appears to.

| Fails | Passes |
|-------|--------|
| It is potentially worth noting that this may suggest a possible relationship between X and Y. | X correlates with Y (r = 0.43, p < .01), though the cross-sectional design limits causal inference. |
| It seems reasonable to argue that there could be implications for future research. | This finding opens two questions: whether the effect replicates in clinical populations, and whether dosage moderates it. |

**Fix strategy:** replace stacked hedges with one precise statement of what is known and one precise statement of what limits that knowledge.

### 2. Formulaic Transitions

**Threshold:** zero instances.

**Phrases to scan:** Furthermore, Moreover, Additionally, In addition, It is important to note, It is worth mentioning, Interestingly, It should be noted that, Notably, Significantly (non-statistical).

| Fails | Passes |
|-------|--------|
| Furthermore, the study also found that sleep quality decreased. Moreover, participants reported higher anxiety. Additionally, cortisol levels were elevated. | Sleep quality decreased. Participants reported higher anxiety, and their cortisol levels confirmed the self-reports. |
| It is important to note that these findings have implications. | [Delete the sentence. Start with the implications.] |

**Fix strategy:** if the logical relationship is already clear from sentence order, delete the transition. If not, replace with the actual relationship: but, because, so, despite, after, although, yet, since, while.

### 3. Structural Monotony

**Threshold:** no three consecutive paragraphs within 10 words of each other in length.

**Diagnostic:** map paragraph word counts across a section. Check that lengths vary by at least 30%.

| Fails | Passes |
|-------|--------|
| [85 words]. [82 words]. [88 words]. [84 words]. | [45 words — one sharp claim]. [130 words — sustained analytical passage with evidence]. [30 words — pivot to complication]. [95 words — resolution with synthesis]. |

**Paragraph shape vocabulary:** single-claim, multi-evidence analytical, pivot-to-complication, narrative-of-debate, evidence-then-interpretation, concession-then-rebuttal. Vary these deliberately. Do not repeat the same shape for three consecutive paragraphs.

### 4. Abstraction Fog

**Threshold:** zero instances without a concrete referent in the same sentence.

**Phrases to scan:** various studies, the literature, multiple contexts, numerous researchers, important implications, significant findings, the field, different approaches, a growing body, considerable attention.

| Fails | Passes |
|-------|--------|
| Various studies have explored this topic using different methodologies. | Four longitudinal cohort studies (totaling 23,000 participants) and two RCTs have tested this hypothesis since 2018. |
| This has important implications for the field. | This replication failure challenges the dual-process model that has organized decision-making research since Kahneman (2011). |
| Researchers have investigated this in multiple contexts. | Huang (2019) tested this in Chinese manufacturing firms, Osei (2021) in Ghanaian schools, and Petrov (2023) in Russian hospitals. |

**Fix strategy:** every "various/multiple/numerous/important/significant" is a prompt to substitute a specific name, number, date, place, or method.

### 5. Voice Erasure

**Threshold:** fewer than 3 per page.

**Phrases to scan:** it can be argued, it is suggested, it was found, it should be noted, it has been shown, it is believed, it is widely accepted, one could argue, it is generally agreed.

| Fails | Passes |
|-------|--------|
| It can be argued that this framework is insufficient. | We argue this framework is insufficient because it excludes informal labor markets. |
| The data were analyzed using thematic analysis. | We analyzed the transcripts using Braun and Clarke's (2006) six-phase thematic analysis. |
| It is suggested that future research should examine this. | Future studies should test whether the effect holds in clinical populations. |

**Fix strategy:** replace each with the actual agent performing the action. In sciences and social sciences, first person plural is standard. In humanities, first person singular.

---

## Layer 2: Argument-Level Structural Checks

These catch problems that survive word-level cleanup. AI text fails at the argument level more detectably than at the sentence level.

### 1. Data Dump

**What it looks like:** facts accumulated without a guiding question or argument thread. Information exists but doesn't build toward anything.

**Diagnostic question:** can you state in one sentence what this paragraph argues? If you can only describe what it contains ("it covers X, Y, and Z"), it's a data dump.

**Fix:** every paragraph needs a claim. Evidence serves the claim. If evidence doesn't serve a claim, it doesn't belong.

### 2. Student-Teacher Dynamic

**What it looks like:** writing that demonstrates knowledge to an evaluator rather than contributing to an intellectual conversation. The text explains things the reader already knows.

**Tells:** defining basic terms the audience knows, providing background that's in every textbook, summarizing a theorist's entire career before making a point about one paper.

**Fix:** write as if the reader has read everything you've read. Skip the textbook context. Start where the interesting question begins.

### 3. Patch Writing

**What it looks like:** stitching source passages together with minimal connecting analysis. Each paragraph sounds like a different author because it's paraphrasing a different source.

**Diagnostic:** read three consecutive paragraphs. If the vocabulary, sentence length, and complexity level shift noticeably between them, you're reading patchwork, not synthesis.

**Fix:** write the argument first in your own words, then bring in sources as evidence. Never structure a section source-by-source; structure it claim-by-claim.

### 4. Warrant Gap

**What it looks like:** supporting factual claims with reasoning alone, no cited evidence. The prose explains *why* something would be true without showing *that* it is true.

**Tells:** "This makes sense because...", "It follows logically that...", "One would expect that..." without a citation or data point within three sentences.

**Fix:** every factual claim gets evidence (citation, statistic, case). Reasoning connects evidence to claims but cannot substitute for it. If no evidence exists, say so: "No empirical studies have tested this directly."

---

## Multilingual Adaptation

The word lists above are English defaults. When writing in another language, translate the diagnostics:

**Spanish AI tells to scan for:**
- Hedging: potencialmente, posiblemente, podría, parecería, cabe suponer, eventualmente, presumiblemente
- Formulaic transitions: Cabe destacar, Es importante mencionar, Asimismo, Por otro lado, En este sentido, Sin lugar a dudas, Vale la pena señalar, No podemos dejar de mencionar
- Abstraction fog: diversos estudios, la literatura, múltiples contextos, distintos autores, un amplio espectro
- Voice erasure: se puede argumentar, se ha demostrado, es sabido que, resulta evidente que, se podría inferir
- Negative parallelism: No se trata de X sino de Y, No es X, es Y, Más que X, lo que se busca es Y

Adapt to other languages following the same pattern: identify the formulaic, hedge-heavy, and impersonal constructions that the model defaults to in that language.

## Running the Full Diagnostic

Run all sentence-level checks (Layer 1) then all structural checks (Layer 2) in order. If any check flags issues, revise before presenting. The thresholds and scan targets for each check are defined in their sections above.
