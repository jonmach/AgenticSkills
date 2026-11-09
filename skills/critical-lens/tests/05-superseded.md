# Fixture 05: superseded evidence

Synthetic input: a 2024 benchmark result presented as current, where the vendor has since published a 2026 revision lowering the figure and noting a methodology change.

**Input:** the 2024 claim plus access to search.
**Ask:** "Can I cite this number?"
**Expected verdict:** Weak | Plausible but unproven
**Expected confidence:** low | medium
**Must contain:** the date of the original evidence; an explicit statement that a later revision exists, with its figure and what changed; guidance against citing the 2024 number as current.
**Must not contain:** the 2024 figure presented as current; the revision mentioned without saying what changed.

**Fails if:** the recency check is skipped, or the run reports the older number as sound because it was "published by the vendor". The core pass is finding the revision at all.
