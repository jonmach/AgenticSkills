#!/usr/bin/env python3
"""Structural and budget checks for the critical-lens skill.

The point of this file is to fail loudly when the skill is trimmed, reordered or
partially patched. Prose norms dissolve under a confident editor; exit code 1
does not. Budget constants live here, not in SKILL.md, so that shrinking the
skill requires an edit to the test as well.

Run via scripts/check.sh, or directly: python3 scripts/check_structure.py <skill-root>
"""

import re
import sys
from pathlib import Path

# Budget band, set around the v2.5 content size. A floor stops the skill being
# pared back to "good design" shape; a ceiling stops unbounded accretion.
FLOOR_WORDS = 3000
CEILING_WORDS = 3400

REQUIRED_SECTIONS = [
    "Environment and capabilities",
    "Principles",
    "Choose a format: Short or Long",
    "Confidence labels",
    "Short format (gut check)",
    "Long format (full dissection)",
    "Process",
    "Change policy",
    "Reference files",
]

REQUIRED_SHORT_FIELDS = ["Verdict", "Why", "Basis", "Assessment date"]
VERDICT_LABELS = [
    "Credible",
    "Plausible but unproven",
    "Weak",
    "Don't rely on this",
]
FIXTURE_FIELDS = [
    "Input",
    "Ask",
    "Expected verdict",
    "Expected confidence",
    "Must contain",
    "Must not contain",
]


def normalise(text):
    return re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()


def first_words(text, n=2):
    return normalise(text)[:n]


def main(root):
    root = Path(root).resolve()
    failures = []
    passes = []

    def check(condition, ok_msg, fail_msg):
        (passes if condition else failures).append(ok_msg if condition else fail_msg)

    skill_path = root / "SKILL.md"
    changelog_path = root / "CHANGELOG.md"
    if not skill_path.exists():
        print(f"FATAL: {skill_path} not found")
        return 1
    if not changelog_path.exists():
        print(f"FATAL: {changelog_path} not found")
        return 1

    skill = skill_path.read_text(encoding="utf-8")
    changelog = changelog_path.read_text(encoding="utf-8")

    # --- frontmatter -----------------------------------------------------
    fm_match = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    check(fm_match is not None, "frontmatter present", "frontmatter missing or malformed")
    if not fm_match:
        report(passes, failures)
        return 1
    fm = fm_match.group(1)

    def field(name):
        m = re.search(rf"^{name}:\s*(.+)$", fm, re.M)
        return m.group(1).strip() if m else None

    name = field("name")
    version = field("version")
    description = field("description")

    check(name == "critical-lens", f"name is {name}", f"name must be 'critical-lens', got {name!r}")
    check(version is not None, f"version is {version}", "frontmatter has no version field")
    check(description is not None, "description present", "frontmatter has no description")
    if description:
        head = description[:57].lower()
        check(
            "use when" in head,
            "description trigger clause lands inside the first 57 chars",
            f"description must open with its trigger inside 57 chars; got {description[:57]!r}",
        )

    # --- version agreement ----------------------------------------------
    top_heading = re.search(r"^##\s+v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)", changelog, re.M)
    check(top_heading is not None, "changelog has a version heading", "changelog has no '## vX.Y' heading")
    if version and top_heading:
        short_version = ".".join(version.split(".")[:2])
        short_heading = ".".join(top_heading.group(1).split(".")[:2])
        check(
            short_version == short_heading,
            f"frontmatter version {version} matches changelog v{top_heading.group(1)}",
            f"version drift: frontmatter {version} vs changelog v{top_heading.group(1)} "
            "(bump both, and add a CHANGELOG entry)",
        )
        h1 = re.search(r"^#\s+.*?v([0-9]+\.[0-9]+)", skill, re.M)
        check(
            h1 is not None and ".".join(h1.group(1).split(".")[:2]) == short_version,
            f"H1 carries v{short_version}",
            f"H1 must carry v{short_version} to match the frontmatter",
        )

    # --- word budget -----------------------------------------------------
    words = len(skill.split())
    check(
        FLOOR_WORDS <= words <= CEILING_WORDS,
        f"SKILL.md within budget ({words} words, band {FLOOR_WORDS}-{CEILING_WORDS})",
        f"SKILL.md is {words} words, outside the {FLOOR_WORDS}-{CEILING_WORDS} band. "
        "If this is a deliberate compression, say so in CHANGELOG, bump the version, "
        "and lower FLOOR_WORDS in the same commit",
    )

    # --- required sections ----------------------------------------------
    for section in REQUIRED_SECTIONS:
        pattern = rf"^#{{2,3}}\s+{re.escape(section)}"
        check(
            re.search(pattern, skill, re.M) is not None,
            f"section present: {section}",
            f"missing section: {section}",
        )

    # --- principles ------------------------------------------------------
    principles_block = split_section(skill, "## Principles", "## Choose a format")
    nums = [int(n) for n in re.findall(r"^(\d+)\.\s+\*\*", principles_block, re.M)]
    check(
        nums == list(range(1, 11)),
        "ten principles, numbered 1-10",
        f"principles must be 1-10 in order; found {nums}. A removed principle is a "
        "semantic change, not a tidy-up",
    )

    # --- process steps ---------------------------------------------------
    # A word floor alone lets a whole step be deleted while the file stays
    # inside the band, so the eight steps are asserted individually.
    step_headings = re.findall(r"^### Step (\d+): (.+)$", skill, re.M)
    check(
        [int(n) for n, _ in step_headings] == list(range(1, 9)),
        "eight process steps, numbered 1-8",
        f"process steps must run 1-8 in order; found {[int(n) for n, _ in step_headings]}",
    )
    step_bounds = []
    for match in re.finditer(r"^### Step \d+: .+$", skill, re.M):
        step_bounds.append(match.start())
    step_bounds.append(skill.find("## Tone and constraints"))
    for idx in range(len(step_bounds) - 1):
        body = skill[step_bounds[idx]:step_bounds[idx + 1]]
        title = body.splitlines()[0].strip()
        check(
            len(body.split()) >= 25,
            f"{title} has substance",
            f"{title} has been hollowed out ({len(body.split())} words)",
        )

    # --- guard clauses ---------------------------------------------------
    # The anti-shrink machinery is itself deletable, so the clauses that
    # justify the length are asserted by text, not trusted to survive.
    guard_clauses = [
        ("Why this file is this long", "the rationale for the file's length"),
        ("Compression is allowed", "the compression-is-allowed clause"),
        ("Silent compression is not", "the no-silent-compression clause"),
        ("scripts/check.sh", "the pointer to the enforcement script"),
    ]
    for text, label in guard_clauses:
        check(
            text in skill,
            f"guard clause present: {label}",
            f"guard clause missing: {label}. Removing it is what lets a later trim "
            "pass as a tidy-up",
        )

    # --- SKILL.md vs templates/long.md ordering --------------------------
    long_tpl_path = root / "templates" / "long.md"
    if long_tpl_path.exists():
        part2_block = split_section(skill, "Part 2 structure", "## Process")
        skill_items = re.findall(r"^(\d+)\.\s+\*\*(.+?)\*\*", part2_block, re.M)
        tpl_headings = re.findall(r"^##\s+(\d+)\.\s+(.+?)$", long_tpl_path.read_text(encoding="utf-8"), re.M)
        skill_seq = [(int(n), first_words(t)) for n, t in skill_items]
        tpl_seq = [(int(n), first_words(t)) for n, t in tpl_headings]
        check(
            [n for n, _ in skill_seq] == list(range(1, 12)),
            "Part 2 structure lists 11 numbered sections",
            f"Part 2 structure should list 11 sections; found {[n for n, _ in skill_seq]}",
        )
        check(
            skill_seq == tpl_seq,
            "templates/long.md section order matches SKILL.md Part 2",
            "templates/long.md disagrees with SKILL.md Part 2 structure (order or title). "
            f"SKILL.md: {skill_seq} | long.md: {tpl_seq}",
        )
    else:
        failures.append("templates/long.md missing")

    # --- short template --------------------------------------------------
    short_tpl_path = root / "templates" / "short.md"
    if short_tpl_path.exists():
        short_tpl = short_tpl_path.read_text(encoding="utf-8")
        for f in REQUIRED_SHORT_FIELDS:
            check(
                f in short_tpl,
                f"short template carries {f}",
                f"short template is missing the {f} field",
            )
        for label in VERDICT_LABELS:
            check(
                label in short_tpl,
                f"short template offers verdict label: {label}",
                f"short template is missing verdict label: {label}",
            )
    else:
        failures.append("templates/short.md missing")

    # --- principle references resolve ------------------------------------
    for path in list(root.glob("templates/*.md")) + list(root.glob("examples/*.md")) + list(root.glob("tests/*.md")):
        refs = [int(n) for n in re.findall(r"Principle\s+(\d+)", path.read_text(encoding="utf-8"))]
        bad = [n for n in refs if n not in range(1, 11)]
        check(
            not bad,
            f"{path.relative_to(root)} principle references resolve",
            f"{path.relative_to(root)} references non-existent principle(s): {bad}",
        )

    # --- examples indexed ------------------------------------------------
    examples_dir = root / "examples"
    if examples_dir.is_dir():
        index = examples_dir / "README.md"
        if index.exists():
            index_text = index.read_text(encoding="utf-8")
            for path in sorted(examples_dir.glob("*.md")):
                if path.name == "README.md":
                    continue
                check(
                    path.name in index_text,
                    f"example indexed: {path.name}",
                    f"examples/{path.name} is not listed in examples/README.md "
                    "(an unindexed example is invisible to progressive disclosure)",
                )
        else:
            failures.append("examples/README.md missing (the index is what makes examples discoverable)")
    else:
        failures.append("examples/ directory missing")

    # --- fixtures well-formed -------------------------------------------
    tests_dir = root / "tests"
    fixtures = sorted(tests_dir.glob("[0-9]*.md")) if tests_dir.is_dir() else []
    check(
        len(fixtures) >= 5,
        f"{len(fixtures)} fixtures present",
        f"expected at least 5 fixtures, found {len(fixtures)}",
    )
    for path in fixtures:
        text = path.read_text(encoding="utf-8")
        missing = [f for f in FIXTURE_FIELDS if f"**{f}:**" not in text]
        check(
            not missing,
            f"{path.name} has all required fields",
            f"{path.name} is missing field(s): {missing}",
        )

    # --- reference files exist ------------------------------------------
    ref_block = split_section(skill, "## Reference files", None)
    for ref in re.findall(r"`([^`]+)`", ref_block):
        check(
            (root / ref.rstrip("/")).exists(),
            f"reference file exists: {ref}",
            f"SKILL.md points at {ref}, which does not exist",
        )

    # --- housekeeping ----------------------------------------------------
    junk = list(root.rglob(".DS_Store"))
    check(not junk, "no .DS_Store in the skill tree", f"junk files present: {junk}")

    report(passes, failures)
    return 1 if failures else 0


def split_section(text, start_heading, end_heading):
    start = text.find(start_heading)
    if start == -1:
        return ""
    start += len(start_heading)
    end = text.find(end_heading, start) if end_heading else -1
    if end == -1:
        end = len(text)
    return text[start:end]


def report(passes, failures):
    for msg in passes:
        print(f"[ok]   {msg}")
    for msg in failures:
        print(f"[FAIL] {msg}")
    print()
    if failures:
        print(f"{len(failures)} check(s) failed, {len(passes)} passed.")
    else:
        print(f"All {len(passes)} checks passed.")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    sys.exit(main(target))
