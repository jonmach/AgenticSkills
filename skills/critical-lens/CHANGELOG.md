# Changelog

Versioning follows the Change policy in `SKILL.md`: patch for wording, minor for anything that changes behaviour, and any compression is labelled.

## v2.5.0

Behaviour changes:

- **Confidence anchors added.** High / medium / low are now defined, and both formats name the fact that drives the label. Previously the labels were required but undefined, so the same evidence could be labelled differently on different runs.
- **Section order fixed.** In SKILL.md, Part 2 section 5 is now "Where evidence conflicts" and section 6 "Step-by-step findings", matching `templates/long.md`. The two sources had disagreed since v2.2, so every Long run contradicted one of them.
- **Material vs minor claims reconciled.** The Long rule "do not skip claims because they seem minor" is now paired with Principle 3: every claim is assessed, but material claims get a full block and minor ones get a line.
- **Short format carries an assessment date**, in the basis line and in the template, as the Long format already did.

Structural changes:

- `version:` added to the frontmatter, kept in step with this file by `scripts/check.sh`.
- `description` rewritten so the trigger clause sits inside the first 57 characters, where truncating hosts still show it.
- `examples/` added: one complete Short output and four excerpts covering a holds-up verdict, a steelman, a genuine conflict, and a confidence downgrade after a blocked fetch.
- `tests/` added: the five suggested tests, rewritten as fixtures with expected verdict, expected confidence, must-contain and must-not-contain fields.
- `scripts/check.sh` added: enforces the word budget, the ten principles, section presence, SKILL.md/template order agreement, version agreement with this file, indexed examples, well-formed fixtures and resolvable principle references. `.githooks/pre-commit` runs it.
- Word budget band set at 3,000-3,400 for SKILL.md, which is 3,166 words at this version. The floor exists so that calibration material cannot be edited away to suit a shorter-is-better norm; lower it only alongside a CHANGELOG entry that says what behaviour was traded.

## v2.4
- Short format word target raised from 150 to 300.
- Disclosure (Principle 10) now sits first in both formats and both templates, matching "up front".
- Short format may add a one-line recency check.
- README wording made neutral.

## v2.3 (portable edition)
- Added "Environment and capabilities" section: date handling, tool-agnostic wording, text-only fallback when no web access, citation and formatting guidance.
- Added Principle 10: disclose the assistant's own stake when the content concerns its vendor, product or a competitor.
- Replaced tool-specific wording ("extended search mode", fetch-tool behaviour) with generic equivalents.
- Step 4: also check whether the original authors have since revised or retracted the finding.
- Step 5: self-report note changed from "runs high" to "unreliable, and not always in the same direction".
- Added `templates/short.md` and `templates/long.md` with pre-send checklists.
- Added README with install notes, capability requirements, adaptation checklist and suggested tests.

## v2.2
- Long format restructured as a layered document: Part 1 executive summary, Part 2 detailed evidence.
- Work order: write Part 2 first, Part 1 last, place Part 1 at the top, then cross-check.
- Part 1 includes bottom line, highlights, ranked concerns, areas of confidence and low confidence, implications, corrections, basis.

## v2.1
- Replaced quick and full modes with user-selectable Short (gut check) and Long (full dissection) formats.
- Added format selection rules and switching behaviour (Short and Long must not silently disagree).

## v2.0
- Added internal-consistency step, recency step, quick and full modes, search-then-fetch rule, affiliation chains, scrutiny of critics, inference labelling, pre-send audit, "holds up" verdict, and limits statement.

## v1.0
- Initial draft: source and incentive check, number checks, scope, assumptions, consequences, output format.
