# Thesis Workspace

The academic thesis is written in Polish. Engineering instructions in this README remain in English.

## WETI 2026 template boundary

The official WETI diploma page is <https://eti.pg.edu.pl/studenci/dyplomy>. At retrieval on 2026-09-02 it linked the Polish archive `Thesis_Template_PL_26.zip` through:

<https://files.pg.edu.pl/api/v1/file/preview?path=eti%2FDokumenty+WETI%2FSzablonyPD%2FThesis_Template_PL_26.zip>

The archive's `main.tex` identifies format version 3.0, dated 2025-11-25, and contains an internal-use notice. The notice permits use, copying, and modification only for WETI students and employees for internal educational and organizational purposes. It prohibits public repositories, websites, public Overleaf projects, cloud services, and transfer to third parties without permission from the rights holder.

This repository is private and is used for the author's WETI thesis. At the project owner's direction, the exact retrieved extraction is versioned under [`thesis/upstream/weti-2026/`](upstream/weti-2026/), without edits or relicensing. Keep the repository private; this project decision is not permission for public redistribution or transfer to third parties. The checksum, manifest, source, retrieval procedure, and rights decision are recorded in [`docs/research-log/2026-09-02-weti-template.md`](../docs/research-log/2026-09-02-weti-template.md).

**GitHub-hosted CI: ALLOWED for this private repository only.** The project owner accepts the interpretation that a private GitHub Actions job, triggered from this private repository and producing a permission-restricted artifact, is internal project processing for the WETI student rather than public sharing or transfer to third parties. This is a project-level operating decision, not a public redistribution license. The upstream notice explicitly names cloud services, so residual uncertainty remains about whether the rights holder would treat hosted CI infrastructure as prohibited cloud use; if that interpretation is rejected, disable this workflow and use the documented local build.

Project-owned thesis content is kept separately in [`thesis/overlay/`](overlay/). The supplied Moja PG title page is stored at [`thesis/inputs/title-page.pdf`](inputs/title-page.pdf) and is included without modification. The overlay is copied over the committed upstream tree only in a temporary build directory; upstream files remain unchanged.

## Local build

The upstream template requires LuaLaTeX and states a TeX Live version of at least 2022. The build also requires:

- `latexmk` for the clean build orchestration;
- `biber` for the `biblatex` bibliography;
- Pygments (`pygmentize`) because the upstream class loads `minted`;
- Poppler (`pdfinfo`, `pdftotext`, and `pdftoppm`) for verification and visual rendering.

If the upstream example chapter is used unchanged, also provide `epstopdf` for its EPS
illustration conversion. The project overlay's layout fixture intentionally uses a
vector-free placeholder and does not depend on that example asset.

The upstream class enables `-shell-escape` for `minted`. Use it only while building trusted local sources. A clean build that preserves the upstream directory is:

```bash
build_dir="$(mktemp -d)"
cp -a thesis/upstream/weti-2026/. "$build_dir"/
cp -a thesis/overlay/. "$build_dir"/
mkdir -p "$build_dir/inputs"
cp thesis/inputs/title-page.pdf "$build_dir/inputs/title-page.pdf"
(cd "$build_dir" && latexmk -C && latexmk -lualatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex)
pdfinfo "$build_dir/main.pdf"
pdftotext "$build_dir/main.pdf" "$build_dir/main.txt"
pdftoppm -png "$build_dir/main.pdf" "$build_dir/page"
```

The copied staging directory is disposable. Do not run the overlay by editing the extracted upstream tree, and do not commit the generated PDF or rendered pages.

## Continuous integration

`.github/workflows/thesis-build.yml` runs for changes under `thesis/**` or to the workflow itself on the standard GitHub-hosted `ubuntu-24.04` runner. It stages the committed upstream template, project overlay and title page, then uses the SHA-pinned `xu-cheng/latex-action` action with a TeX Live 2024 container, LuaLaTeX, shell-escape and Pygments support. It uploads `main.pdf` as the `thesis-pdf` workflow artifact. The upstream directory is never edited during the build.

The expected reproducible path is:

`results/raw` → versioned processing/statistics → `results/tables` and `results/figures` → Polish thesis references.

Do not manually copy measured numbers when a generated table, figure, or analysis artifact can supply them. The final title page must come from Moja PG, and GenAI use must be disclosed according to current university guidance.
