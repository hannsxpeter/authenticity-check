# authenticity-check (agent instructions)

This repository is the `authenticity-check` skill: a pure-prompt instruction
set that scores how authentically a piece of text reads as the work of a real
human author and flags the spans that read as AI-generated, AI-templated, or
generically derivative. It also performs a separate read-only scan for
suspicious Unicode provenance carriers in supplied text. No scripts, no
dependencies, no network access; tools are read-only. It is the entry point
for any AI coding tool that reads
`AGENTS.md` (Codex, OpenCode, Antigravity, Pi, Zed, and others).

It is the evaluative counterpart to the separate `humanizer` skill. This one
diagnoses. It does not rewrite.

## When to apply this skill

Apply it whenever the user wants to know whether a text is authentic, whether
it reads like AI or like a person, how human a passage sounds, which parts
sound machine-written, or whether their draft still sounds like them or a
named author. Also apply it when they ask whether pasted text contains a
hidden AI watermark, invisible Unicode, or provenance mark. Apply it even when
they do not say "authenticity check" and even when the cue is oblique ("does
this sound like a bot," "this feels generated").

Do not apply it to transformative requests (humanize, de-slop, de-AI,
rewrite, fix, remove marks, make it sound like X). Those belong to a separate
transformation or provenance hygiene skill, not this one.

## How to run it

Read `SKILL.md` in this repository and follow it exactly. The full method
lives there and in `references/`; do not improvise a shortcut. In brief:

1. **Step 0** discover the baseline: if the request is "does this sound like
   me / like NAME" and a voice source exists (pasted sample, named author, or
   a discovered `VOICE.md` / `STYLE-GUIDE.md`), enter voice-deviation mode;
   otherwise generic mode. Never invent a target voice.
2. **Step 0a** provenance preflight: inspect supplied text for suspicious
   Unicode carriers, run the mandatory context audit, and keep the result
   separate from the authenticity score. Never alter the text.
3. **Step 0b** density pre-check: skim for dead-giveaway tells and set
   scrutiny low, standard, or full so human-first text is not over-flagged.
4. **Multi-pass:** catalog scan against `references/tell-patterns.md`
   (32 patterns, six families), then a mandatory false-positive audit against
   `references/do-not-flag.md` (it has veto power and converts strong false
   positives into human-marker credit), then the read-only
   internal-consistency heuristics, then voice deviation in voice-deviation
   mode only.
5. Emit the exact output contract from `SKILL.md`: Authenticity report (band
   plus 0-100 score) / Provenance signals / Flagged spans / Reads as human /
   Score basis / Caveats / Next step.

## Hard rule (diagnostic only)

This skill scores and flags. It never rewrites, edits, paraphrases, removes or
normalizes Unicode, strips metadata, or returns "improved" prose, not even one
suggested replacement span. The rewrite is the separate `humanizer` skill's
job, run as a human-judged step. A combined score-then-rewrite loop is
detector-gaming; humanizer refuses it, and keeping the two skills separate
with a person in between is what makes that refusal hold. Never carry a target
score into a rewrite or removal workflow.

## Scope

This skill gives an honest read of how authentically text reads as a person's
work. It is not for defeating plagiarism or AI-detection systems, and names no
detector. Reframe such requests toward the honest diagnostic (see `SKILL.md`
"Scope and intended use").

## Vendored criteria

`references/tell-patterns.md`, `references/do-not-flag.md`, and
`references/voice-matching.md` are synced copies whose canonical upstream is
the `humanizer` repo. Do not edit them here; re-sync from humanizer when its
criteria change. See each file's header stamp and the README sync obligation.
