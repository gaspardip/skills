---
name: pr-comment-style
enabled: true
event: bash
conditions:
  - field: command
    operator: regex_match
    pattern: gh\s+(api\s+.*-f\s+body=|pr\s+(comment|create|review|edit)|issue\s+comment)
  - field: command
    operator: regex_match
    pattern: \u2014|I've \w+|I have \w+|I'll \w+|I'd \w+|I would \w+|Here's |Here is |As (requested|mentioned|noted|per |a result)|This (ensures|change ensures|allows|enables|provides|approach|makes it|is needed)|In order to|In addition|Additionally|Furthermore|Moreover|Specifically|Consequently|Subsequently|Accordingly|[Nn]otably|To summarize|In summary|In conclusion|Overall,|It's (worth noting|worth mentioning|important to (note|highlight))|It is (worth (noting|mentioning)|important to note)|It should be noted|Please note|For your reference|Going forward|With respect to|In terms of|With regard[s]? to|The following|Let me (know|explain)|Per the (discussion|ticket|review)|Regarding|By (implementing|leveraging|utilizing|employing|embracing|adopting|harnessing|prioritizing)|cannot be overstated|plays a crucial role|ensure[s]? (that |proper )|significantly |fundamentally |substantially |effectively |essentially |seamlessly |comprehensively |robustly |holistically |leverag(e|ing|es)|utiliz(e|ing|es)|facilitat(e|ing|es)|streamlin(e|ing|es)| crucial | robust | comprehensive | holistic |pivotal |seamless |worth (noting|mentioning|highlighting)
action: block
---

**blocked - formal/LLM language in pr comment**

per global CLAUDE.md:
- casual, lowercase, talk like a colleague
- no emdashes - use `-` or `:` instead
- no self-narration ("I've ...", "I'll ...")
- no formal connectors (Additionally, Furthermore, Moreover)
- no adverb inflation (significantly, fundamentally, seamlessly, essentially)
- no upgraded verbs (leverage, utilize, facilitate, streamline)
- no buzzword adjectives (crucial, robust, pivotal, holistic, comprehensive)
- no filler openers (Overall, In summary, It's worth noting)
- no "By X-ing" structures (By implementing, By leveraging)
- lead with the point, skip preamble

rewrites:
- "significantly improves" -> "improves" (let the reader judge significance)
- "leveraging the utility" -> "using the utility"
- "robust error handling" -> "error handling" or "better error handling"
- "By implementing X, we ensure Y" -> "X. Y."
- "Overall, this PR" -> just start talking about the changes
- "crucial for the release" -> "needed for the release"

fix the text and retry.
