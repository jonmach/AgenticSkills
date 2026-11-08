# critical-lens: portable skill package (v2.4)

A reusable instruction set that makes an AI agent apply sceptical senior-analyst scrutiny to claims, case studies, statistics, vendor material and reports. It offers two output formats: a **Short** gut check and a **Long** layered report (executive summary on top, full evidence below).

## Contents

| File | Purpose |
|---|---|
| `SKILL.md` | The skill itself: principles, format selection, process, tone. Frontmatter (`name`, `description`) followed by Markdown instructions. |
| `templates/short.md` | Fill-in skeleton and pre-send checklist for the Short format. |
| `templates/long.md` | Fill-in skeleton and pre-send checklist for the Long format. |
| `CHANGELOG.md` | Version history. |
| `README.md` | This file. |

## Installing in another agentic tool

The package is plain Markdown with no tool-specific syntax in the instructions. How you load it depends on the tool.

1. **Tools that load skill folders** (a directory containing `SKILL.md` with `name` and `description` frontmatter): copy the whole `critical-lens/` folder into the tool's skills location. The `description` field is what tells the tool when to trigger the skill.
2. **Tools that take a single instruction file or custom instructions / system prompt**: paste the body of `SKILL.md` (everything below the frontmatter). If there is a size limit, paste `SKILL.md` alone and omit the templates; the structures are also described inside `SKILL.md`.
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

## Suggested tests

Run these before relying on the skill in a new tool.

1. **Vendor claim with a headline number.** Paste or link a vendor case study with a "X% improvement" claim. Expected: Short gives a verdict, 2-3 flags and a basis line; Long includes an internal-consistency check, an affiliation check and a verification log.
2. **A claim that should hold up.** Use a well-evidenced, independently replicated finding. Expected: a "Credible" or "Plausible" verdict with no manufactured objections.
3. **Pasted claim, no links, no web access.** Expected: text-only mode, everything external marked unverified, explicit offer of what to check, no invented sources.
4. **Format switching.** Ask for a Short, then "go deeper", then "short version". Expected: the verdict never changes silently between formats, and the Long version reuses earlier checks.
5. **Superseded evidence.** Use a study that its own authors have since revised. Expected: the recency check finds the update and the summary says so.

## Known limitations

- Versions 2.2 and 2.3 have only been exercised on one worked example (AI coding productivity studies). Treat results on other domains as untested.
- The Long format's executive summary may exceed one page on complex topics.
- The Short format's 300-word target can still be tight when the content has many claims; the skill's answer is to rank and report only the top concerns.
- The skill improves the process of scrutiny; it cannot make an agent's retrieved sources reliable. Check the verification log.

## Provenance

Developed iteratively through use. The Long format's "write the detail first, then the summary" order came from the observation that checking the detail repeatedly changed the verdict and caught errors in earlier statements.
