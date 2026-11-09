# Fixture 04: format switching

Synthetic input: the same vendor page as fixture 01, with web access available.

**Input:** the vendor page, then the sequence "gut check this" → "go deeper" → "short version".
**Ask:** the three-request sequence, in one conversation.
**Expected verdict:** the same label in all three outputs.
**Expected confidence:** the same label in all three outputs, unless a Long-only check justified a documented change.
**Must contain:** in the Long output, a verification log and at least one check not present in the Short; in the final Short, the same verdict and top concerns as the Long, compressed.
**Must not contain:** a silently changed verdict; a final Short that introduces a new claim or a new objection absent from the Long; repeated verification work in the Long that the Short had already done.
**Fails if:** verdict or confidence drifts between formats without an explicit statement of what changed and why. Where the drift is stated and evidenced, it is a pass — the rule is no silent disagreement.
