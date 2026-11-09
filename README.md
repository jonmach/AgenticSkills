# AgenticSkills

A collection of reusable skills for AI agents such as Claude Code. Each skill is a self-contained package of instructions (and any supporting scripts or references) that teaches an agent how to perform a particular kind of task.

## Layout

```
skills/
  <skill-name>/
    SKILL.md      # name, description, and instructions
    ...           # optional scripts, references, assets
```

## Skills

| Skill | Description |
|---|---|
| [critical-lens](skills/critical-lens/) | Sceptical senior-analyst scrutiny of claims, case studies and reports, as a short gut check or a long layered report. |

## Adding a skill

1. Create `skills/<skill-name>/`.
2. Add a `SKILL.md` with frontmatter (`name`, `version`, `description`) followed by the instructions.
3. Include any supporting files the skill needs alongside it: `templates/` for skeletons, `examples/` for worked output, `tests/` for fixtures, `scripts/` for checks.

## Checks

Skills may ship a check script. Run it before committing, or enable the shared hooks once:

```
git config core.hooksPath .githooks
```

The hook runs `skills/<name>/scripts/check.sh` for any skill touched by the commit. `critical-lens` uses its checks to hold a word budget and section structure, so the skill cannot be silently trimmed to suit a shorter-is-better norm; its `SKILL.md` "Change policy" section explains what counts as a safe edit.


## License

MIT. See [LICENSE](LICENSE).
