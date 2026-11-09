# critical-lens: portable skill package (v2.5)

A reusable instruction set that makes an AI agent apply sceptical senior-analyst scrutiny to claims, case studies, statistics, vendor material and reports. It offers two output formats: a **Short** gut check and a **Long** layered report (executive summary on top, full evidence below).

## Contents

| File | Purpose |
|---|---|
| `SKILL.md` | The skill itself: principles, format selection, confidence anchors, process, change policy. Frontmatter (`name`, `version`, `description`) followed by Markdown instructions. |
| `templates/short.md` | Fill-in skeleton and pre-send checklist for the Short format. |
| `templates/long.md` | Fill-in skeleton and pre-send checklist for the Long format. |
| `examples/` | One complete Short output and four excerpts of the moments that vary most between runs. |
| `tests/` | Five fixtures with expected verdict, confidence and content checks. |
| `scripts/check.sh` | Structural and word-budget checks. Run before committing. |
| `CHANGELOG.md` | Version history. |
| `README.md` | This file. |

## Installing in another agentic tool

The package is plain Markdown with no tool-specific syntax in the instructions. How you load it depends on the tool.

1. **Tools that load skill folders** (a directory containing `SKILL.md` with `name` and `description` frontmatter): copy the whole `critical-lens/` folder into the tool's skills location. The `description` field is what tells the tool when to trigger the skill.
2. **Tools that take a single instruction file or custom instructions / system prompt**: paste the body of `SKILL.md` (everything below the frontmatter). If there is a size limit, paste `SKILL.md` alone and leave out `templates/`, `examples/` and `tests/`; the structures are also described inside `SKILL.md`.
3. **Tools with per-project or per-repo rules files**: add the body of `SKILL.md` as a rules file, and keep the `description` text as the trigger note if the tool supports one.

Check your tool's own documentation for exact paths and file names. This package has not been verified against any specific tool's folder layout.

## What the skill needs from the host

| Capability | Required? | If missing |
|---|---|---|
| Ability to follow long Markdown instructions | Yes | n/a |
| Current date in context | Strongly recommended | The skill tells the agent to state the date it is assuming |
| Web search tool | Recommended | Skill falls back to text-only mode: everything external is marked unverified, nothing sourced from memory |
| Page-fetch tool | Recommended | Agent can only use search snippets and must label claims unverified |
| Deeper search mode | Optional | Used for Long format when standard results are thin |
| File or document tool | Optional | Output is delivered in chat as Markdown |
| Table rendering | Optional | Agent uses lists instead of tables |

## Adaptation checklist

- [ ] Confirm the tool's skill or rules file accepts the frontmatter, or strip it and paste the body.
- [ ] If the host's tools have specific names, optionally add a line to the "Environment and capabilities" section mapping "web search tool" and "page-fetch tool" to them.
- [ ] If the host has its own citation format, leave the Citations bullet as is; the skill defers to it.
- [ ] Decide the default format for your users. The skill defaults to Short for a single claim and Long for multiple claims or significant decisions; edit "Selecting the format" if you want a different default.
- [ ] Check the disclosure principle (Principle 10) reads correctly for the assistant in the new tool. It asks the assistant to disclose when the content concerns its own vendor, model or product, or a competitor.

## Testing it

`tests/` holds five fixtures: a vendor claim with a headline number, a claim that should hold up, a text-only run, a format switch, and a superseded finding. Each states the expected verdict, the expected confidence, and what the output must and must not contain. Run them in a fresh conversation each, because verdict drift between runs is the failure they exist to catch. `tests/README.md` has the procedure.

## Keeping the skill honest

This file is deliberately longer than the usual guidance for skill files (~3,200 words, with templates, examples and fixtures loading separately). Every principle corresponds to a failure that was observed. The risk is not that it is too long; it is that someone later trims it to look tidy, deleting the rule that stopped the failure.

Three things guard against that:

- **A budget band, not a ceiling.** `scripts/check.sh` fails if `SKILL.md` drops below 3,000 words or rises above 3,400.
- **Structural checks.** The same script fails on a missing principle, a template that disagrees with the structure in `SKILL.md` (the v2.4 defect this version fixes), a version that disagrees with the CHANGELOG, an unindexed example, or a malformed fixture.
- **A Change policy** in `SKILL.md`: compression is allowed, silent compression is not. A rule removed or weakened needs a version bump and a CHANGELOG entry naming what was traded.

Run `skills/critical-lens/scripts/check.sh` by hand, or enable the hook once with `git config core.hooksPath .githooks`.

## Known limitations

- The five fixtures have not yet been run end-to-end against a real model at v2.5; they are structurally valid and each states a pass condition, but no results are recorded yet. Treat v2.5 output quality as untested until a fixture run is logged in the CHANGELOG.
- Earlier confidence labelling is superseded: assessments produced under v2.4 or below used undefined low/medium/high labels and are not comparable with v2.5 output.
- The Long format's executive summary may exceed one page on complex topics.
- The Short format's 300-word target can still be tight when the content has many claims; the skill's answer is to rank and report only the top concerns.
- The skill improves the process of scrutiny; it cannot make an agent's retrieved sources reliable. Check the verification log.

## Provenance

Developed iteratively through use. The Long format's "write the detail first, then the summary" order came from the observation that checking the detail repeatedly changed the verdict and caught errors in earlier statements.
