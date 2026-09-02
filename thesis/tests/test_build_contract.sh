#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

title_page='thesis/inputs/title-page.pdf'
workflow='.github/workflows/thesis-build.yml'
upstream='thesis/upstream/weti-2026'
rights_log='docs/research-log/2026-09-02-weti-template.md'

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
test -s "$rights_log" || fail "missing template rights decision: $rights_log"
grep -Fq 'GitHub-hosted CI: ALLOWED' "$rights_log" \
  || fail 'rights decision does not explicitly allow GitHub-hosted CI for this private repository'
grep -Fq 'residual uncertainty' "$rights_log" \
  || fail 'rights decision does not record residual uncertainty'

test -s "$workflow" || fail "missing thesis build workflow: $workflow"
grep -Fq 'thesis/**' "$workflow" \
  || fail 'workflow is not scoped to thesis changes'
grep -Fq 'latexmk' "$workflow" \
  || fail 'workflow does not invoke latexmk'
grep -Fq 'upload-artifact' "$workflow" \
  || fail 'workflow does not upload a PDF artifact'
grep -Fq 'main.pdf' "$workflow" \
  || fail 'workflow does not identify main.pdf as its artifact'
grep -Fq 'runs-on: ubuntu-24.04' "$workflow" \
  || fail 'workflow does not use the pinned standard GitHub-hosted runner'
if ! awk '
  /^  push:/ { in_push=1; next }
  /^  [[:alnum:]_-]+:/ { in_push=0 }
  in_push && /^    branches:/ { branches=1; next }
  in_push && branches && /^      - main$/ { found=1 }
  END { exit(found ? 0 : 1) }
' "$workflow"; then
  fail 'workflow does not limit push builds to main'
fi
if grep -Fq 'self-hosted' "$workflow"; then
  fail 'workflow still requires a self-hosted runner'
fi
grep -Fq 'thesis/upstream/weti-2026' "$workflow" \
  || fail 'workflow does not stage the committed upstream template'
for action in actions/checkout xu-cheng/latex-action actions/upload-artifact; do
  grep -Eq "uses: ${action}@[0-9a-f]{40}( +# .*)?$" "$workflow" \
    || fail "workflow does not pin ${action} to a full commit SHA"
done
if grep -Eq 'uses: (actions/checkout|xu-cheng/latex-action|actions/upload-artifact)@v[0-9]' "$workflow"; then
  fail 'workflow still uses a mutable action tag'
fi
grep -Fq 'latexmk_use_lualatex: true' "$workflow" \
  || fail 'workflow does not request LuaLaTeX'
grep -Fq 'latexmk_shell_escape: true' "$workflow" \
  || fail 'workflow does not enable shell-escape for minted'
if grep -Fq 'apt-get' "$workflow"; then
  fail 'workflow performs slow host-side TeX package installation'
fi

printf 'build contract: ok\n'
