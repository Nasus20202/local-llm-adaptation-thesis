# Thesis Workspace

The academic thesis is written in Polish. Engineering instructions in this README remain in English.

## WETI 2026 template boundary

The official WETI diploma page is <https://eti.pg.edu.pl/studenci/dyplomy>. At retrieval on 2026-09-02 it linked the Polish archive `Thesis_Template_PL_26.zip` through:

<https://files.pg.edu.pl/api/v1/file/preview?path=eti%2FDokumenty+WETI%2FSzablonyPD%2FThesis_Template_PL_26.zip>

The archive's `main.tex` identifies format version 3.0, dated 2025-11-25, and contains an internal-use notice. The notice permits use, copying, and modification only for WETI students and employees for internal educational and organizational purposes. It prohibits public repositories, websites, public Overleaf projects, cloud services, and transfer to third parties without permission from the rights holder.

Consequently, this repository does not redistribute the archive or any extracted upstream file, including `_formatting.cls`, fonts, sample title/declaration PDFs, examples, or upstream chapter files. The checksum, manifest, source, retrieval procedure, and rights decision are recorded in [`docs/research-log/2026-09-02-weti-template.md`](../docs/research-log/2026-09-02-weti-template.md). Obtain the archive through the official page and keep the extracted tree outside Git. Do not modify that tree.

Project-owned thesis content is kept separately in [`thesis/overlay/`](overlay/). The overlay is copied over an unchanged local template only in a temporary build directory. The title page and declaration remain local PDFs supplied through Moja PG or the official template's local working copy; this repository does not reconstruct or replace them.

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
export WETI_TEMPLATE_DIR=/absolute/path/to/extracted/Thesis_Template_PL_26
build_dir="$(mktemp -d)"
cp -a "$WETI_TEMPLATE_DIR"/. "$build_dir"/
cp -a thesis/overlay/. "$build_dir"/
(cd "$build_dir" && latexmk -C && latexmk -lualatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex)
pdfinfo "$build_dir/main.pdf"
pdftotext "$build_dir/main.pdf" "$build_dir/main.txt"
pdftoppm -png "$build_dir/main.pdf" "$build_dir/page"
```

The copied staging directory is disposable. Do not run the overlay by editing the extracted upstream tree, and do not commit the generated PDF or rendered pages.

The expected reproducible path is:

`results/raw` → versioned processing/statistics → `results/tables` and `results/figures` → Polish thesis references.

Do not manually copy measured numbers when a generated table, figure, or analysis artifact can supply them. The final title page must come from Moja PG, and GenAI use must be disclosed according to current university guidance.
