#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_URL="https://github.com/pret/pokeemerald.git"
UPSTREAM_COMMIT="5eff78649e7170a877b961ef0b3da13b81a16038"

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <dedicated-output-directory>" >&2
  exit 2
fi

OUT="$1"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PATCH="$REPO_ROOT/patches/0001-enable-corrected-bugfix-baseline.patch"

if [[ -e "$OUT" && ! -d "$OUT/.git" ]]; then
  echo "refusing to use existing non-git directory: $OUT" >&2
  exit 2
fi

if [[ ! -d "$OUT/.git" ]]; then
  git clone --filter=blob:none --no-checkout "$UPSTREAM_URL" "$OUT"
fi

git -C "$OUT" fetch --depth=1 origin "$UPSTREAM_COMMIT"
git -C "$OUT" checkout --detach "$UPSTREAM_COMMIT"
git -C "$OUT" reset --hard "$UPSTREAM_COMMIT"
git -C "$OUT" clean -ffd

git -C "$OUT" apply --check "$PATCH"
git -C "$OUT" apply "$PATCH"

if ! grep -q '^#define BUGFIX$' "$OUT/include/config.h"; then
  echo "BUGFIX was not enabled" >&2
  exit 1
fi

printf 'Prepared corrected source at %s\n' "$OUT"
printf 'Upstream commit: %s\n' "$UPSTREAM_COMMIT"
printf 'Applied patch: %s\n' "$PATCH"
