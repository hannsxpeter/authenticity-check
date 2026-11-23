# Scoring Rubric and Internal-Consistency Heuristics

This file is native to the `authenticity-check` repo. It is not vendored from
humanizer, because humanizer rewrites and has no score. Read it when you reach
the scoring step, and read Part 3 during Pass 3.

The score is a calibrated heuristic, not a verdict. It exists to communicate
strength of evidence in one glance, then hand the reader to the flags and the
caveat. Never present it as proof of authorship, and never tune it against any
detector.

Step 0a provenance findings are a separate evidence channel. Do not move the
authenticity score because an invisible Unicode carrier was found or absent.
The score measures how the prose reads through cadence, diction, structure,
specificity, internal consistency, and voice. Report provenance in its own
section and score only the prose evidence from Passes 1-4.

## Part 1: The bands

Three bands. The vocabulary is chosen on purpose to sit alongside the
humanizer skill's low / medium / high density language, so that when the two
skills are bundled in the `voiceprint` product the reports compose without a
translation layer. Humanizer's density (how AI-marked) and this
skill's authenticity (how human it reads) are inverse views of the same axis.

- **Reads human.** The text reads as a person's own work. Few or no surviving
  flags after Pass 2, strong human markers present, internal profile
  consistent. Pairs with humanizer "low density": little or nothing to do.
- **Mixed signals.** Genuine human markers and real AI tells coexist, or one
  region reads inserted. This band requires credited human markers to be
  present, or a genuinely inserted region; uniform, marker-free prose is not
  Mixed, it is the band below. Pairs with humanizer "medium density".
- **Reads AI-generated.** Dead-giveaway tells cluster, OR the rhythm is
  uniform, OR chat-UI contamination is present. Each is independently
  sufficient. Uniform rhythm with no credited human markers is this band even
  when the vocabulary is clean and no catalog tell fired: that is a relocated
  signature, and clean word choice does not lift it. Pairs with humanizer
  "high density".

Report the band first; it is the part a human acts on. The number refines it.

The discriminator between a careful human and a relocated signature is not
vocabulary or formality; it is the presence of human markers and genuine
variance. Genuine human prose, even when formal and clean, leaves
fingerprints: a specific, an opinion, an idiosyncratic rhythm. Laundered AI
prose is clean, even-rhythmed, and marker-free. Decide the band on that test,
not on how inoffensive the words are.

A precedence note on anaphora. `do-not-flag.md` Part 2 credits deliberate
repetition for emphasis (a single anaphora) as a human rhetorical choice.
That credit does not apply when anaphora is the entire structural skeleton
of a marker-free uniform passage: in that case the repetition is the
template, not the rhetoric, and the Step 0b relocated-signature override
governs. Co-occurrence (anaphora plus uniform rhythm plus zero credited
markers) overrides the lone-anaphora credit. The single-anaphora-in-otherwise-
varied-prose case still wins for the writer; the anaphora-as-skeleton case
does not.

## Part 2: The 0-100 score

Higher means it reads more authentically as a person's own work. Start from a
neutral 70 (most ordinary prose is neither obviously machine nor obviously
fingerprinted) and move from there. This is deliberately not a formula; it is
a disciplined estimate with the following forces.

Move the score **down** for:

- **Surviving catalog flags after Pass 2.** Weak isolated signals barely move
  it. A cluster within one family, or co-occurrence across families, moves it
  hard. Recurrence is the signal; one "delve" is noise.
- **Uniform rhythm.** Even sentence lengths and the same shape resolved the
  same way across the piece is the core machine fingerprint and is weighted
  above any single lexical tell. A relocated signature (vocabulary swapped,
  rhythm still even) does not earn back points.
- **Internal-consistency findings (Part 3).** A sharply divergent span is
  strong, span-local evidence and lowers the score for that region even when
  each sentence in it is individually clean.
- **Voice deviation (voice-deviation mode only).** Spans outside the target
  author's distribution, weighted by how central the violated trait is to
  that voice (a cadence break outweighs one out-of-register word).

One override: any **chat-UI contamination** (tell-patterns.md pattern 31) is
near-certain confirmation on its own. Its presence caps the score in the
"Reads AI-generated" band regardless of everything else, and it is always
flagged whatever the density.

Move the score **up** for:

- **Human markers credited in Pass 2.** Specific concrete details and numbers,
  mixed or contradictory feeling, dated and time-bound references,
  self-corrective asides, idiosyncratic sentence-length swings, strong
  unhedged opinion, regional or trade idiolect. These are positive evidence,
  not merely the absence of tells. Specificity is the densest human signal
  there is; weight it heavily.
- **Consistent, earned internal profile.** Register and sophistication that
  hold together, with variance that reads as a mind rather than a template.

### How Pass 2 demotions affect the score

A candidate that Pass 2 drops (a lone weak signal) must not lower the score at
all; it was never a tell. A candidate that Pass 2 reclassifies as a human
marker must move the score the other way, upward. This asymmetry is the point:
the do-not-flag audit does not just mute false positives, it converts the
strongest of them into positive evidence of a human author. A report that lost
points for genuine voice has miscounted.

### Rough anchors (calibration, not thresholds)

- 85-100, Reads human: near-empty flag list, strong markers, consistent
  profile. The restraint case lives here.
- 60-84, Mixed signals: some real tells, some real markers, or one inserted
  region in otherwise human prose.
- 0-59, Reads AI-generated: clustered dead-giveaways, uniform rhythm, or any
  chat-UI contamination.

The reported number must fall inside the chosen band's anchor range. A band
and a number that disagree is a miscount, not a nuance: pick the band on the
evidence and the Part 1 marker test, then place the number within that band.
The same input must not land in different bands across runs.

Do not over-precisify. "78" and "81" carry the same message; do not stage a
debate between them. If two paragraphs of evidence point different ways, say
so in the Score basis rather than splitting the difference into false
certainty.

## Part 3: Internal-consistency heuristics (Pass 3, read-only)

This is the network-free adaptation of stylometric-inconsistency and
semantic-drift detection. It compares the text against itself. No web search,
no external database, no citation lookup; the skill's allowed tools are
read-only by design.

### Procedure

1. **Chunk.** Split the text into natural units (paragraphs, or roughly
   80-150 word blocks if paragraphs are very long or absent). Three or more
   chunks are needed for this pass to mean anything; on very short text, skip
   it and say so in the Score basis.
2. **Profile each chunk** on three cheap, read-only dimensions:
   - sentence-length distribution (the swing, not just the mean),
   - register and diction (plain vs. Latinate, technical density, formality),
   - lexical sophistication (vocabulary range and the level of specialized
     terminology).
3. **Establish the document baseline** as the central tendency across chunks,
   and note its natural variance. Human writing has variance; the baseline is
   a band, not a point.
4. **Flag sharp divergence.** A chunk is a Pass 3 flag when it breaks the
   baseline band on one or more dimensions in a way the surrounding prose does
   not earn: an abrupt jump in technical sophistication with no setup, a
   register break (a polished encyclopedic paragraph dropped into casual
   prose, or the reverse), or a cadence that belongs to a different writer.

### What "sharp divergence" means

Sharp means a step change, not gradual drift. A writer warming up, or a
naturally more technical middle section with a transition into it, is earned
variance and is not flagged. The tell is the seam: a span that reads as
lifted, pasted, or generated to fill a gap, sitting unintegrated next to prose
that does not match it. When unsure whether a shift is a seam or just range,
do not flag it; Part 4's restraint applies here too.

### Weighting against catalog hits

A Pass 3 divergence is independent evidence and is reported as its own flag
with the heuristic named (for example, `internal-consistency:
register-break`). It is strong when it co-occurs with catalog flags in the
same span (a divergent region that is also dense with Family A or D tells is
high-confidence inserted or generated text). It is weaker, and should be
reported with that hedge, when a region diverges but is otherwise clean: that
can be a genuinely human shift in subject or energy. Never let a single Pass 3
flag alone push a text into "Reads AI-generated"; pair it with catalog
evidence or report it as a softer "one region reads inserted" within "Mixed
signals".

## Part 4: Restraint applies to scoring too

The single worst error this skill can make is scoring genuine human prose low
because it is formal, clean, or contains one tricolon and two dashes. Smooth
correctness is not guilt. Before finalizing a low score, re-read the strongest
human markers you found and ask whether the evidence honestly supports the
band. If a text is a person writing carefully, the correct output is a high
score with a populated "Reads as human" section, not a hedge in the middle.
Doing that well, and saying why, is the strongest evidence the skill worked.

There is a symmetric error in the other direction, and it is just as real:
scoring laundered, marker-free, uniform prose high merely because it is clean
and lexically inoffensive. Restraint protects a careful human; it is not
leniency toward emptiness. The test that separates the two is not vocabulary,
it is whether the text carries human markers and genuine variance. Clean prose
with even rhythm and not one specific, opinion, or idiosyncratic swing is a
relocated signature: score it in the Reads AI-generated band and say why in
the Score basis. Before finalizing a high score on clean prose, confirm you
can name at least one real human marker; if you cannot, the correct output is
a low score, not a comfortable high one.
