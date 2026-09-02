#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

title_page='thesis/inputs/title-page.pdf'
workflow='.github/workflows/thesis-build.yml'
upstream='thesis/upstream/weti-2026'

for required_file in \
  _formatting.cls \
  _bibliography.bib \
  fonts/arial.ttf \
  fonts/arialbd.ttf \
  fonts/ariali.ttf \
  fonts/arialbi.ttf \
  pages/2_statement.pdf
do
  test -s "$upstream/$required_file" \
    || fail "missing committed upstream template file: $upstream/$required_file"
done

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
grep -Fq 'runs-on: ubuntu-latest' "$workflow" \
  || fail 'workflow does not use the standard GitHub-hosted runner'
if grep -Fq 'self-hosted' "$workflow"; then
  fail 'workflow still requires a self-hosted runner'
fi
grep -Fq 'thesis/upstream/weti-2026' "$workflow" \
  || fail 'workflow does not stage the committed upstream template'

printf 'build contract: ok\n'
