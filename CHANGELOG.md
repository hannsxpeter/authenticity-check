# Changelog

All notable changes to this skill are documented here. This project adheres
to semantic versioning.

## [Unreleased]

### Added

- A drift check, `.github/scripts/check_drift.py`, adapted from humanizer's,
  and a GitHub Actions workflow that runs it on every pull request and every
  push to `main`. It fails when versions, catalog and example counts, the
  evals, what each tool adapter mentions, the vendored criteria headers and
  sync stamps, file references, the README layout and anchors, or house style
  drift apart, and it annotates the offending lines in pull requests.
- A README status badge for the check, Layout entries for its files and for
  `CHANGELOG.md` and `evals/RESULTS.md`, and a note on running it locally.
- Version links at the end of this changelog.

### Fixed

- `AGENTS.md` now names `references/provenance-signals.md` for the Step 0a
  context audit, as the other adapters do.
- The Cursor rule's method paragraph is rewrapped within 80 columns.

## [1.2.2] - 2026-10-07

Criteria re-sync patch with two documentation fixes. The vendored detection
criteria now match humanizer 1.3.1. No change to the scoring method, the band
logic, or the diagnostic-only boundary.

### Changed

- Re-vendored `references/tell-patterns.md`, `references/do-not-flag.md`,
  and `references/voice-matching.md` from humanizer v1.3.1 (`09bf76d`); sync
  stamps bumped to `2026-10-07 / 09bf76d`. `do-not-flag.md` is byte-identical
  to the prior `9632cf1` sync (header stamp only). `tell-patterns.md` renames
  pattern 29 to "Knowledge-cutoff and capability disclaimers", notes that a
  pattern's After line assumes writer-supplied facts, and rewords its
  house-style note on em dashes. `voice-matching.md` now ranks explicit input
  in the request (a pasted sample or a named author) above a discovered
  profile file, and the explicit request wins a conflict.
- `SKILL.md` Step 0b names pattern 29 by its new title. Step 0 needs no
  change: it lists profile files in priority order and states no precedence
  that contradicts the new voice-source order.
- `SKILL.md` `metadata.version` and the `README.md` version badge bumped to
  1.2.2; the README sync stamp updated.
- README: the Scriveno pointer names the published npm package `scriveno`
  (`scriveno-cli` was unpublished in May 2026), and Pi Coder is now called Pi
  in the README and `AGENTS.md`, as humanizer renamed it.

### Verification

- The three vendored bodies are byte-identical to humanizer's files at
  `09bf76d`, and the catalog keeps its 32 patterns in six families.
- `evals/RESULTS.md` is left as the point-in-time record of the battery run
  against criteria from `9632cf1`. None of its cases depends on the changed
  material: the pattern 29 change is a title, the After-line and em dash
  notes are rewrite-side and house-style guidance, and eval 2's voice source
  is the VOICE.md the user names, so no source conflict arises. That file's
  own rule still calls for a re-run when the vendored criteria change, and
  none was done for this patch.

## [1.2.1] - 2026-08-15

Documentation-only patch clarifying the exact relationship between the
v1.2.0 provenance preflight and `watermarks-remover`. Skill behavior is
unchanged.

### Changed

- Added an included-versus-excluded feature table to the README.
- Replaced broad watermark language with the precise capability: read-only
  inspection of suspicious Unicode carrier candidates exposed in supplied
  text.
- Documented that the v1.2.0 work adapted only the Unicode carrier taxonomy
  and context guardrails from upstream v0.4.0 at commit `28eca2d91fd4`.
- Made clear that this repository is not a port, wrapper, or integration of
  the upstream project and does not promise ongoing feature parity.
- Explicitly excluded upstream executable code and services, content
  mutation, binary and metadata handling, statistical token-watermark
  handling, and image-watermark handling.
- Bumped the skill metadata and README badge to 1.2.1.

### Verification

- Documentation claims were checked against `SKILL.md`,
  `references/provenance-signals.md`, the repository surface, and the v1.2.0
  focused provenance eval record.
- No runtime instructions, scoring behavior, dependencies, tools, or eval
  outcomes changed, so the existing v1.2.0 behavior checks remain applicable.

## [1.2.0] - 2026-08-14

Version 1.2.0 adds a read-only, pure-prompt Unicode carrier preflight adapted
only at the taxonomy and context-guardrail level from the MIT-licensed
`watermarks-remover` project. It classifies and reports inspectable carrier
candidates in supplied text without crossing the skill's diagnostic-only
boundary.

### Added

- Step 0a provenance preflight for suspicious invisible and format Unicode,
  including zero-width controls, bidi controls, tag characters, variation
  selectors, unusual spaces, and other format characters.
- `references/provenance-signals.md` with carrier classes, escaped-codepoint
  reporting, a mandatory multilingual and visible-sequence context audit,
  confidence labels, and coverage limits.
- A required `Provenance signals` report section kept separate from the prose
  authenticity score.
- Eval cases for a suspicious U+200B carrier and a legitimate Persian U+200C
  script joiner.
- A focused blind forward test of those two cases, recorded as 2/2 PASS in
  `evals/RESULTS.md`.

### Changed

- Skill and adapter triggers now include hidden AI watermark, invisible
  Unicode, and text-provenance questions.
- The output contract now has seven sections. Existing examples record a
  clean provenance preflight, and a new worked example demonstrates a carrier
  finding without lowering an otherwise human prose score.
- The host compatibility list moved under `metadata` so the skill frontmatter
  conforms to the current validator schema without losing the information.
- The README release badge now follows the current GitHub owner, and its
  verification section distinguishes the v1.1.1 baseline from the focused
  v1.2.0 provenance test.
- `SKILL.md` metadata and the README badge moved to 1.2.0.

### Source relationship and boundaries

- Only the Unicode carrier taxonomy and context guardrails were adapted from
  `watermarks-remover` v0.4.0 at source commit `28eca2d91fd4`. No deterministic
  Python scripts, services, or other upstream executable code were imported.
- No content removal, normalization, substitution, rewriting, or re-saving
  was added. The skill remains read-only and pure-prompt, with no dependencies
  or network access.
- Binary-file inspection and C2PA, EXIF, XMP, and document-metadata inspection
  or stripping remain outside the skill.
- Statistical token-watermark detection or removal, image-watermark scoring or
  removal, pixel-domain marks, audio, and video remain outside the skill.
- A carrier is not treated as proof of AI authorship, and its presence or
  absence does not move the authenticity score by itself.

## [1.1.1] - 2026-05-29

Audit-and-fix patch. Re-vendor verification against humanizer current main
plus documentation-drift fixes surfaced by a full markdown audit. No change
to skill behavior, the band logic, or the diagnostic-only boundary.

### Changed

- Re-vendored `references/tell-patterns.md`, `references/do-not-flag.md`,
  and `references/voice-matching.md` from humanizer current main; sync
  stamps bumped to `2026-05-29 / 9632cf1`. Bodies of the first two are
  byte-identical to the prior `e9404c9` sync (header stamp only);
  `voice-matching.md` picks up the upstream "Scriven" -> "Scriveno"
  rename.
- `references/examples.md` Example 2 header: `Scrutiny: standard` ->
  `Scrutiny: medium`, matching the SKILL.md output contract which accepts
  `low | medium | high`. ("Standard scrutiny" was the description of the
  medium-density tier in Step 0b; "medium" is the value to report.)
- `evals/RESULTS.md`: `Skill version` 1.0.0 -> 1.1.1; sync-stamp references
  updated to current.
- `SKILL.md` `metadata.version` and `README.md` version badge bumped to
  1.1.1.

### Audit checklist (all green after fixes)

Verified consistent across all 18 tracked markdown / adapter files:
versions, "13 AI coding tools" claim, Step 0 / 0b / Pass 1-4 naming, scrutiny
level values, sync stamps, output-contract section names and order, repo
URLs, AGENTS.md tool enumeration, CHANGELOG date entries, file paths in the
README Layout block. No `Step 0c` leakage from humanizer, no stale "8 tools"
references, no version/badge mismatch.

## [1.1.0] - 2026-05-29

Version-alignment release with the paired `humanizer` skill, which moved to
`v1.1.0` after vendoring the same five additional tool adapters (Windsurf,
Cline, Continue, Zed, Aider). `authenticity-check` shipped those adapters
in its `v1.0.0`, so there is no new functional change here over `v1.0.1`;
this bump exists so the diagnose/rewrite pair carries the same minor
version. Consumers tracking either repo can pin both at `^1.1.0`.

### Changed

- `SKILL.md` `metadata.version` and the `README.md` version badge bumped
  from `1.0.1` to `1.1.0`.

## [1.0.1] - 2026-05-29

Post-release polish and verification hardening. No change to the band logic
or the diagnostic-only boundary; this release clarifies precedence, adds a
worked example and an eval case for the relocated-signature property, and
documents known limitations.

### Added

- Fifth worked example in `references/examples.md` for the
  relocated-signature case (clean vocabulary, uniform rhythm, no human
  markers): the canonical "laundered AI slop" demonstration, paired with
  Example 3 (restraint on careful human prose) so the two failure
  directions are visible side by side.
- Seventh case in `evals/evals.json` formalizing the relocated-signature
  regression in the runtime eval set (previously only in
  `evals/RESULTS.md` prose).
- Anaphora precedence note in `references/scoring.md` Part 1: a single
  anaphora is still a human rhetorical choice per `do-not-flag.md`, but
  anaphora used as the structural skeleton of a marker-free uniform
  passage is the template, and the Step 0b relocated-signature override
  governs.
- Regression-pass criteria and a "Known untested edge cases" section in
  `evals/RESULTS.md` (voice-deviation mode interacting with the override).

### Changed

- Split the dense Step 0b relocated-signature override paragraph in
  `SKILL.md` into three short paragraphs (trigger, rationale, action) for
  readability.
- Added Zed to the `AGENTS.md` enumeration of tools that read the file.
- `README.md`: footnote on the 13-tool count (Zed shares files with
  `AGENTS.md` / the Continue rule); short note that Pass 3 mostly engages
  on multi-paragraph inputs; clarification that the vendored-criteria sync
  stamp records the last criteria sync, not every humanizer commit.

## [1.0.0] - 2026-05-15

First stable release.

### Added

- Pure-prompt `authenticity-check` skill: `SKILL.md` plus on-demand
  reference files. No scripts, no dependencies, no network access. Tools are
  read-only (Read, Glob, Grep); the skill never edits.
- Diagnostic-only design: scores and flags, never rewrites. The rewrite is
  the separate `humanizer` skill's job. The split is deliberate: a combined
  score-then-rewrite loop is detector-gaming, which humanizer refuses, so
  diagnosis and transformation are kept as a human-judged pair, never merged.
- Output contract: an authenticity band (Reads human / Mixed signals / Reads
  AI-generated), a 0-100 authenticity score, span-level flags with reasons, a
  required "Reads as human" section, a score basis, a caveat, and a next
  step. No rewritten prose is ever returned.
- Multi-pass diagnostic: catalog scan (Pass 1), mandatory false-positive
  audit with veto power (Pass 2), read-only internal-consistency heuristics
  for stylometric-inconsistency and semantic-drift span detection (Pass 3),
  and voice-deviation analysis in voice-deviation mode (Pass 4).
- Density pre-check (Step 0b) that scales scrutiny to evidence so human-first
  text is not over-flagged, with chat-UI contamination as a decisive
  override.
- Native scoring rubric (`references/scoring.md`): the band vocabulary,
  the 0-100 forces, the do-not-flag demotion-and-credit asymmetry, and the
  read-only internal-consistency heuristic definitions.
- Native worked examples (`references/examples.md`): generic AI-heavy text,
  voice-deviation, a restraint case, and a reframed detector-evasion request.
- Vendored detection criteria, synced from the canonical `humanizer` repo:
  `references/tell-patterns.md`, `references/do-not-flag.md`, and
  `references/voice-matching.md`. Each carries a header stamp. Last synced
  2026-05-15 from humanizer commit `e9404c9`.
- **Vendored-criteria sync obligation (recorded here as a standing
  commitment):** the three vendored files are synced copies, not the source
  of truth. When humanizer's criteria change they must be re-synced; they
  must not be edited in this repo independently, or the diagnose/rewrite pair
  will drift. These copies and humanizer's originals are to be reconciled
  into a single shared source of truth when the `voiceprint` product
  (humanizer + authenticity-check, bundled) is built.
- voiceprint composability: no assumption this is the only skill installed,
  clean separation of the skill from its criteria, and non-colliding names
  (skill name, Cursor rule filename, and frontmatter `name` are all
  `authenticity-check`).
- Multi-tool support: Claude Code, Cursor, Codex, Antigravity, Gemini CLI,
  Pi Coder, OpenCode, GitHub Copilot, Windsurf, Cline, Continue, Zed, and
  Aider, via `SKILL.md`, `AGENTS.md`, `.cursor/rules/authenticity-check.mdc`,
  `GEMINI.md`, `.github/copilot-instructions.md`, `.windsurfrules`,
  `.clinerules`, `.continue/rules/authenticity-check.md`, and
  `CONVENTIONS.md`. Every adapter points the agent at the same `SKILL.md`
  and `references/`, so the workflow is identical across tools.
- Relocated-signature hardening. Step 0b carries a second density override
  (alongside the chat-UI-contamination override): clean, marker-free prose
  with uniform or templated rhythm is treated at high scrutiny rather than
  biased toward a high score, because absent slop vocabulary is the
  laundering, not evidence of a person. `references/scoring.md` makes the
  human-marker test decisive (Part 1: Mixed signals requires credited markers
  or a genuinely inserted region; uniform marker-free prose is Reads
  AI-generated even when vocabulary is clean), enforces band/number
  consistency (Part 2), and adds a symmetric restraint guard (Part 4) so
  genuine careful human prose is still not scored low.
- Verification eval set (`evals/evals.json`) plus a recorded blind
  verification battery (`evals/RESULTS.md`): the six suite cases, a
  known-vs-non-known battery, and the relocated-signature regression set, all
  run as blind isolated diagnoses. MIT license.

[Unreleased]: https://github.com/hannsxpeter/authenticity-check/compare/v1.2.2...HEAD
[1.2.2]: https://github.com/hannsxpeter/authenticity-check/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/hannsxpeter/authenticity-check/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/hannsxpeter/authenticity-check/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/hannsxpeter/authenticity-check/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/hannsxpeter/authenticity-check/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/hannsxpeter/authenticity-check/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/hannsxpeter/authenticity-check/releases/tag/v1.0.0
