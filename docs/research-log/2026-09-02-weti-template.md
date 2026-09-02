# Research Log: WETI 2026 Polish LaTeX Template

- **Issue:** [#3](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/3)
- **Retrieved:** 2026-09-02 (UTC)
- **Status:** Retrieved, locally verified, and committed unchanged under `thesis/upstream/weti-2026/` for this private WETI thesis repository.

## Source provenance

- **Official WETI page:** <https://eti.pg.edu.pl/studenci/dyplomy>
- **Official file endpoint:** <https://files.pg.edu.pl/api/v1/file/preview?path=eti%2FDokumenty+WETI%2FSzablonyPD%2FThesis_Template_PL_26.zip>
- **Upstream filename:** `Thesis_Template_PL_26.zip`
- **Embedded format version:** `3.0`
- **Embedded release date:** `2025-11-25`
- **Archive size:** `3,755,168` bytes
- **Archive SHA-256:** `c85e5e59897f34e631d28dcdb734c6b43eefae1d19b0d4628deef43bbc93e0d5`

The endpoint was resolved from the WETI diploma page on the retrieval date. The checksum applies to the downloaded ZIP bytes, before extraction.

## Archive manifest

The archive contains the following 21 files. Their paths and sizes are recorded to make a later retrieval auditable:

```text
_bibliography.bib                         1862
_formatting.cls                           6442
appendices/_formatting.tex                1063
appendices/A_appendix.tex                 1822
chapters/1_introduction.tex               3419
chapters/2_methodology.tex                2656
chapters/3_results.tex                    6713
chapters/4_summary.tex                    1916
fonts/arial.ttf                         1047208
fonts/arialbd.ttf                        991572
fonts/arialbi.ttf                        731964
fonts/ariali.ttf                         728308
img/sin.eps                              15031
main.tex                                  3139
other/sin.py                              1816
pages/1_title.pdf                       380802
pages/2_statement.pdf                   489630
pages/3_abstract_PL.tex                   3782
pages/4_abstract_ENG.tex                  3574
pages/5_symbols.tex                       2750
Thesis_Template_PL.pdf                 1089231
```

The archive itself contains no separate `LICENSE`, `COPYING`, `NOTICE`, or `README` file. The rights notice is embedded at the beginning of `main.tex`.

## Redistribution decision

The embedded notice states that the template and accompanying materials may be used, copied, and modified only for educational and organizational purposes of WETI by WETI students and employees. It expressly prohibits public sharing, including public repositories, websites, public Overleaf projects, and cloud services, and prohibits transfer to third parties without the rights holder's permission. It says that attribution is not required for internal WETI use.

The repository is private and is used by the WETI student who owns this thesis project. At the project owner's direction, the exact extracted upstream tree—including the class, fonts, sample title and declaration PDFs, examples, and upstream PDF—is committed under `thesis/upstream/weti-2026/` without edits or relicensing. This records project-level authorization for this private repository; it is not a claim that the rights notice permits public redistribution. The repository must remain private and the upstream subtree must not be published, transferred, or moved to public Overleaf/cloud projects without rights-holder permission.

The project-owned overlay under `thesis/overlay/` is not a copy of the template. It is assembled over the unchanged committed upstream tree in a disposable staging directory. The supplied Moja PG title page is stored as `thesis/inputs/title-page.pdf`; its SHA-256 is `a530e3b58bfdee39c4be4e6e7bcf6d8ddc04fde09ac5d12cf8ff6b55bf7b95cd`. The declaration is retained from the upstream tree and is not reconstructed here.

## Guidance checks

The current editorial guidance checked for this skeleton is Rector's Ordinance No. 45/2024, effective from 2024-12-02:

- source: <https://cdn.files.pg.edu.pl/eti/Dziekanat/regulaminy/ZR%2045-2024.pdf>;
- the title page is downloaded from Moja PG and has no visible page number;
- a Polish summary and an English abstract are required;
- the contents should include the thesis sections and page numbers;
- a list of important symbols and abbreviations may be included;
- table titles belong directly above tables and figure titles directly below figures;
- every table and figure must be referred to in the text;
- the bibliography contains only sources used in the thesis and follows one consistent citation method, with PN-ISO 690:2012 given as the guidance;
- the general guidance does not impose a formal page count.

The ordinance also says that high-intervention GenAI content must be included in the bibliography according to the applicable university guidance. This skeleton makes no substantive GenAI-generated thesis claim and does not treat the template as thesis authorship.

## Local build verification

The upstream template declares LuaLaTeX, TeX Live 2022 or later, and `-shell-escape` for `minted`. The project overlay additionally uses Biber through the upstream `biblatex` configuration. A clean build command and dependency list are maintained in [`thesis/README.md`](../../thesis/README.md).

The overlay build was intentionally staged from the committed upstream tree so that the upstream files remained unchanged. The generated PDF and rendered PNG pages are disposable verification artifacts and are not committed.

The final clean staging command completed successfully with LuaLaTeX, latexmk, Biber,
Pygments, and Poppler. The output was a 13-page, A4, unencrypted PDF. `pdftotext`
confirmed the Polish `Streszczenie`, English `Abstract`, `Spis treści`, chapter headings,
caption text, `Wykaz literatury`, `Wykaz rysunków`, and `Wykaz tabel`. The final pass had
no unresolved citations or references. The disposable runtime emitted only the expected
environment-specific warning that Polish hyphenation patterns were not registered in
its temporary TeX configuration; this does not occur in a normal registered TeX Live
installation and did not prevent rendering.

The repository CI workflow runs the build-contract check and the same staged build on
GitHub's standard `ubuntu-latest` runner. It installs the documented TeX dependencies,
uses the committed upstream tree, and produces a downloadable `thesis-pdf` artifact for
thesis changes.

Visual checks of the rendered pages found:

- page 1 is the supplied Moja PG title page, with no visible page number;
- page 2 remains the unchanged declaration PDF from the committed upstream tree;
- pages 3–4 contain one-page Polish and English abstracts;
- page 6 contains the resolved contents and page numbers;
- page 9 places the table title directly above the table and the figure title directly
  below the figure, with both elements referenced in the prose;
- page 11 contains the cited bibliography entry, and pages 12–13 contain the figure and
  table lists.

The title page was independently inspected before integration: one page, A4, unencrypted,
with the WETI identity, student/programme details, Polish and English titles, and supervisor.

## Limitations

The archive notice is a rights-holder statement, not a legal opinion. The repository must remain private under the project-level decision recorded above; permission should be requested before any public or third-party redistribution. Faculty- or supervisor-specific requirements may add constraints beyond the university-wide ordinance and must be checked before submission.
