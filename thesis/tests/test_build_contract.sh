#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

title_page='thesis/inputs/title-page.pdf'
workflow='.github/workflows/thesis-build.yml'

test -s "$title_page" || fail "missing project-owned title page: $title_page"
grep -Fq 'inputs/title-page.pdf' thesis/overlay/main.tex \
  || fail 'overlay does not include the project-owned title page'

test -s "$workflow" || fail "missing thesis build workflow: $workflow"
grep -Fq 'thesis/**' "$workflow" \
  || fail 'workflow is not scoped to thesis changes'
grep -Fq 'latexmk' "$workflow" \
  || fail 'workflow does not invoke latexmk'
grep -Fq 'upload-artifact' "$workflow" \
  || fail 'workflow does not upload a PDF artifact'
grep -Fq 'main.pdf' "$workflow" \
  || fail 'workflow does not identify main.pdf as its artifact'

printf 'build contract: ok\n'
