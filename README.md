# authenticity-check

![version](https://img.shields.io/badge/version-1.2.3-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![type](https://img.shields.io/badge/type-pure--prompt%20skill-purple)
![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![mode](https://img.shields.io/badge/mode-diagnostic%20only-red)
![tools](https://img.shields.io/badge/works%20with-13%20AI%20coding%20tools-teal)
![release](https://img.shields.io/github/v/release/hannsxpeter/authenticity-check?label=release&color=blue)
[![drift check](https://github.com/hannsxpeter/authenticity-check/actions/workflows/drift.yml/badge.svg)](https://github.com/hannsxpeter/authenticity-check/actions/workflows/drift.yml)

A standalone, pure-prompt skill that scores how authentically a piece of text
reads as the work of a real human author, and flags the specific spans that
read as AI-generated, AI-templated, or generically derivative. It also scans
supplied text for suspicious Unicode provenance carriers and reports them in
a separate evidence channel. It is just instructions: `SKILL.md` plus a few
reference files. No scripts, no dependencies, no network access. Its tools
are read-only by design.

It is the evaluative counterpart to the `humanizer` skill. This one
diagnoses. It does not rewrite.

## Where this comes from

This skill is the diagnostic half of a pair. Its detection criteria descend
from the voice-preservation logic that powers
[Scriveno](https://github.com/hannsxpeter/scriveno) (formerly Scriven), an
AI-native longform writing, publishing, and translation pipeline whose core
promise is that drafted prose should sound like the writer, not like AI.
[`humanizer`](https://github.com/hannsxpeter/humanizer) lifted the de-slop,
restraint, and voice-matching layer of that pipeline into a standalone
rewrite skill. `authenticity-check` is the read-only counterpart: it applies
the same catalog and the same restraint to *diagnose* rather than transform,
and it vendors humanizer's criteria so the two agree on what a tell is. If
you want the rewrite, use humanizer. If you want the whole writing pipeline,
see Scriveno (npm package `scriveno`, run with `npx scriveno@latest`).

## What it does

Given a piece of text, it returns:

- an authenticity band (Reads human / Mixed signals / Reads AI-generated),
- a 0-100 authenticity score (higher means it reads more like a person's own
  work),
- span-level flags, each with the reason it reads as AI-generated,
  AI-templated, or derivative,
- a read-only provenance preflight for suspicious invisible or format Unicode,
- a "Reads as human" section naming what it deliberately did not flag,
- and a caveat that the score is a heuristic read, not proof.

It runs in generic mode by default, and in a voice-deviation mode when you
ask whether a draft still sounds like you (or a named author) and a voice
sample or profile is available.

## Text provenance preflight

Every run includes a separate scan for inspectable text carriers such as
zero-width and format controls, bidi controls, tag characters, variation
selectors, and unusual spaces. Candidate characters go through a mandatory
context audit so normal multilingual orthography, directional text,
byte-order marks, and load-bearing visible sequences are not mislabeled.

Version 1.2.0 adapted only the Unicode carrier taxonomy and context guardrails
from the MIT-licensed
[`watermarks-remover`](https://github.com/guillaumemeyer/watermarks-remover)
project. Those two elements are represented here as pure-prompt instructions
for a read-only inspection of supplied text. The link is source attribution,
not a claim that this skill ports, wraps, or integrates the upstream tool.
This is a point-in-time adaptation from upstream v0.4.0 at commit
`28eca2d91fd4`, not an ongoing feature-parity or compatibility promise.

| Included in `authenticity-check` v1.2.0 | Not included |
|---|---|
| Unicode carrier classes and a mandatory context audit | Deterministic Python scripts, services, or other upstream executable code |
| Escaped-codepoint and context reporting | Deletion, normalization, substitution, rewriting, or re-saving content |
| Inspection of carrier candidates exposed in supplied text | Binary-file inspection or C2PA, EXIF, XMP, and document-metadata inspection or stripping |
| A provenance evidence channel separate from the prose score | Statistical token-watermark detection or removal, and image-watermark scoring or removal |

The preflight considers only carrier candidates that the agent can inspect in
supplied text. It does not inspect images, audio, or video. Provenance findings
are reported separately and do not change the prose authenticity score by
themselves.

## The pairing with humanizer (a pair, never a merge)

`authenticity-check` and [`humanizer`](https://github.com/hannsxpeter/humanizer)
are designed to be used together, as separate skills, with a human deciding
between them:

```
authenticity-check  ->  you read the flags and decide  ->  humanizer
   (diagnose)               (judgment, not automation)       (rewrite)
        ^                                                        |
        |________________ re-verify, fresh read _________________|
```

They are deliberately kept apart. A single tool that scores text and then
rewrites it to raise its own score is a detector-gaming loop: it optimizes
prose against a metric instead of improving it for a reader. The humanizer
skill explicitly refuses that loop. Keeping diagnosis and transformation in
two skills, with a person in between, is what prevents the loop from forming.
So this skill never rewrites, never carries a "target score" into a rewrite,
and never instructs humanizer how to move a number. The re-verify step is a
fresh diagnosis of the revised text, not a continuation of the first.

## voiceprint (future bundle, designed for, not built here)

A future product, `voiceprint`, will bundle `humanizer` (transform) and
`authenticity-check` (diagnose) into one combined offering. This repo is
built to compose cleanly into that bundle: no assumption that it is the only
skill installed, clean separation of the skill from its criteria files, and
no global names that collide with humanizer (the skill name, the Cursor rule
filename, and the frontmatter `name` are all `authenticity-check`). The band
vocabulary is chosen to sit alongside humanizer's density language so the two
reports compose without a translation layer. `voiceprint` is not built here;
this repo simply does not block it.

## Vendored criteria and the sync obligation

The detection criteria live canonically in the `humanizer` repo
(`references/tell-patterns.md`, `references/do-not-flag.md`, and
`references/voice-matching.md`). Because `authenticity-check` is a standalone
repo and the humanizer repo must stay untouched, this repo vendors synced
copies of those three files into its own `references/` directory. Each
vendored file carries a header stamp recording that it is a synced copy, that
its canonical upstream is the humanizer repo, and the obligations below.

- **These three files are synced copies, not the source of truth:**
  `references/tell-patterns.md`, `references/do-not-flag.md`,
  `references/voice-matching.md`. Last synced 2026-10-07 from humanizer
  commit `09bf76d`. The stamp records the last criteria sync, not every
  humanizer commit; humanizer changes that do not touch the three vendored
  files (for example, adapter additions) do not require a re-vendor.
- **Re-sync when humanizer's criteria change.** Do not edit the criteria in
  this repo independently. A fix belongs upstream in humanizer and is then
  re-vendored here. Editing the copies in place makes the two repos drift and
  the diagnose/rewrite pair stop agreeing on what a tell is.
- **Reconciliation is planned.** When the `voiceprint` product is built,
  these vendored copies and humanizer's originals will be collapsed into a
  single shared source of truth. Until then, the header stamp on each file is
  the contract.

`references/scoring.md` and `references/examples.md` are native to this repo
(humanizer has no score and no diagnostic examples) and are not synced.

## Supported tools

| Tool | File it reads | Install |
|---|---|---|
| Claude Code | `SKILL.md` | `cp -r` this repo to `~/.claude/skills/authenticity-check/`, or use the repo in-project |
| Cursor | `.cursor/rules/authenticity-check.mdc` | Open this repo in Cursor, or copy `.cursor/rules/authenticity-check.mdc` + `SKILL.md` + `references/` into your project |
| Codex | `AGENTS.md` | Clone this repo into (or beside) your project; Codex reads `AGENTS.md` |
| Antigravity | `AGENTS.md` | Same as Codex: keep `AGENTS.md` + `SKILL.md` + `references/` in the workspace |
| Gemini CLI | `GEMINI.md` | Keep `GEMINI.md` + `SKILL.md` + `references/` in the project Gemini runs in |
| Pi | `AGENTS.md` | Point Pi at this repo / its `AGENTS.md` |
| OpenCode | `AGENTS.md` or `SKILL.md` | Copy the skill into OpenCode's skills directory, or keep `AGENTS.md` in the project |
| GitHub Copilot | `.github/copilot-instructions.md` | Copy `.github/copilot-instructions.md` + `SKILL.md` + `references/` into the target repository |
| Windsurf | `.windsurfrules` | Keep `.windsurfrules` + `SKILL.md` + `references/` in the project Windsurf opens |
| Cline | `.clinerules` | Keep `.clinerules` + `SKILL.md` + `references/` in the workspace Cline runs in |
| Continue | `.continue/rules/authenticity-check.md` | Keep `.continue/rules/authenticity-check.md` + `SKILL.md` + `references/` in the project |
| Zed | `AGENTS.md` or `.continue/rules/authenticity-check.md` | Zed reads `AGENTS.md` (already present); the Continue rule also applies if used |
| Aider | `CONVENTIONS.md` | `aider --read CONVENTIONS.md`, or set `read: CONVENTIONS.md` in `.aider.conf.yml`; keep `SKILL.md` + `references/` in the repo |

The Cursor rule and the frontmatter `name` are `authenticity-check`, distinct
from humanizer's `humanizer`, so both skills can be installed side by side
without collision. Every adapter points the agent at the same `SKILL.md` and
`references/`, so the workflow is identical across tools. The 13-tool count
includes Zed as a distinct host even though Zed reads adapter files already
present (`AGENTS.md` or the Continue rule); no Zed-specific adapter is needed.

## Usage

Ask, in plain language, whether a text is authentic, whether it reads like AI
or like a person, how human a passage sounds, which parts sound
machine-written, whether your draft still sounds like you, or whether pasted
text contains suspicious invisible Unicode that might carry a provenance
mark. You do not need to say "authenticity check." Oblique cues
("does this sound like a bot," "something about this feels generated")
trigger it too.

For a "does this still sound like me" check, do one of:

- paste a sample of the target writing,
- name a well-known author, or
- keep a `VOICE.md` (schema in `references/voice-matching.md`) or a
  `STYLE-GUIDE.md` in the project; it is discovered automatically.

Every run returns the report: band and score, provenance signals, flagged
spans, what was deliberately not flagged, the score basis, a caveat, and a
next step. It never returns rewritten or cleaned prose.

## Verification

`evals/evals.json` holds the verification cases (AI-heavy text,
voice deviation, restraint, detector-evasion refusal, an oblique trigger, a
diagnose-then-"just fix it" boundary, a relocated signature, a suspicious
Unicode carrier, and a legitimate script joiner). `evals/RESULTS.md`
records the full v1.1.1 prose regression baseline and the focused v1.2.0
provenance forward test. Every recorded run used an isolated diagnosis with no
access to the expected answer. The regression set exists because the hardest
case is the one that matters most: AI prose with the slop vocabulary removed
but the uniform rhythm kept must still read low, while genuine careful human
prose, even when formal and clean, must not be over-flagged. These files are
documentation and verification only; they are not part of the runtime skill.

On short inputs (a single paragraph or two), the internal-consistency pass
(Pass 3) needs at least three comparable chunks and is skipped; Step 0a,
Step 0b, and Passes 1-2 carry the read, with the relocated-signature override
holding short marker-free uniform inputs in the low band.

A drift check (`.github/scripts/check_drift.py`) runs on every pull request
and every push to `main`. It fails when versions, catalog and example counts,
the evals, what each tool adapter mentions, the vendored criteria headers and
sync stamps, file references, the README layout and anchors, or house style
drift apart. Run `python3 .github/scripts/check_drift.py` before you open a
pull request.

## Scope

This skill gives an honest read of how authentically text reads as a person's
work and a read-only report of inspectable text-provenance carriers. It is not
designed or tuned to defeat plagiarism checkers or AI-detection systems, and
it names no detector. Requests framed as getting AI work past a graded or
contractual assessment are reframed toward the honest diagnostic the skill
actually serves. The diagnostic-only boundary is part of that guarantee:
because the skill never rewrites, removes provenance, or carries a score into
a transformation, it cannot be turned into a score-then-rewrite gaming loop.

## Layout

```
SKILL.md                          orchestrator: workflow, guardrails, output contract
AGENTS.md                         cross-tool entry point (Codex, Antigravity, OpenCode, Pi)
GEMINI.md                         Gemini CLI context
.cursor/rules/authenticity-check.mdc  Cursor project rule (named to not collide with humanizer)
.github/copilot-instructions.md   GitHub Copilot instructions
.windsurfrules                    Windsurf rules
.clinerules                       Cline rules
.continue/rules/authenticity-check.md  Continue / Zed rule
CONVENTIONS.md                    Aider conventions
CHANGELOG.md                      release history
references/tell-patterns.md       vendored, synced from humanizer: the 32-pattern catalog (Pass 1)
references/do-not-flag.md         vendored, synced from humanizer: false positives, human markers (Pass 2)
references/voice-matching.md      vendored, synced from humanizer: voice reading (Pass 4)
references/provenance-signals.md  native: Unicode provenance classes, context audit, limits (Step 0a)
references/scoring.md             native: band + 0-100 rubric, internal-consistency heuristics
references/examples.md            native: six worked diagnostic runs
evals/evals.json                  verification cases (not part of the runtime skill)
evals/files/VOICE.md              voice baseline used by the voice-deviation eval
evals/RESULTS.md                  recorded blind verification runs
.github/workflows/drift.yml       CI: runs the drift check on pushes and pull requests
.github/scripts/check_drift.py    the drift check (repo tooling, not part of the skill)
```

## License

MIT. See [LICENSE](LICENSE).
