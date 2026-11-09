# Fixtures

Five inputs with expected verdict, confidence and content checks. They are prose by necessity — the skill's output is judgement — but each states a pass condition specific enough that two reviewers will agree whether a run passed.

These are read by `scripts/check.sh` for structural validity (every fixture has the six required fields). Running them means executing the skill against each input and comparing the output to the expectations by hand or by a grader.

## Running them

1. For each fixture, start a fresh conversation with the skill loaded. Fresh matters: verdict drift between runs is the failure these catch.
2. Paste the input and the ask exactly. Do not add hints about what to look for.
3. Compare the output against `Expected verdict`, `Expected confidence`, `Must contain` and `Must not contain`. Where a field allows two values, either is a pass; a third value is a fail.
4. Record the date and which fixtures passed in the CHANGELOG entry for the version you are testing.

## Adding one

Add a fixture only for a failure that was actually observed, and name the failure in `Fails if`. A fixture that no real run has failed is a wish, and it inflates confidence in the suite.
