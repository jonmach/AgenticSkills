#!/usr/bin/env bash
# Run the critical-lens structural and budget checks.
#
# Usage: scripts/check.sh [skill-root]
# Exit 1 means the skill has been trimmed, reordered or partially patched in a
# way that changes behaviour. Read the [FAIL] lines; do not silence them.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="${1:-$(dirname "$here")}"

python3 "$here/check_structure.py" "$root"
