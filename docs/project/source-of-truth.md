# Source-of-Truth Policy

## Hierarchy

| Artifact | Question answered | Authority |
|---|---|---|
| `docs/project/charter.md` and governance | Why the project exists and which rules are immutable | Highest project-level authority |
| `docs/research/` | Why the study is designed this way | Scientific methodology authority |
| `openspec/specs/` and approved active changes | What the research software must do | Normative behavior authority |
| `docs/adr/` | Why a consequential decision was selected | Decision rationale and status |
| GitHub Issues and Milestones | What work is queued and its status | Work-management authority only |
| Source code and tests | How approved behavior is implemented and verified | Implementation evidence |
| `results/raw/` | What was observed | Immutable observation authority |
| `results/processed/` and analysis code | What was derived from observations | Reproducible analysis authority |
| `thesis/` | How validated work is explained academically in Polish | Narrative, not numerical authority |

## Conflict handling

1. Stop if an implementation task conflicts with an approved OpenSpec requirement.
2. Stop if a software specification would change scientific intent in `docs/research/`.
3. Create or amend an ADR when a consequential decision changes.
4. Obtain human approval before changing frozen experiment inputs or methodology.
5. Version the affected artifact and run a new experiment; never revise historical raw results.

## Duplication policy

Issues link to specifications and do not copy full designs. ADRs explain choices rather than restating requirements. The thesis cites or generates from analysis artifacts rather than maintaining independent numerical tables. Short summaries may be duplicated only when the owner document and link are explicit.

## Freeze semantics

An input becomes frozen only through a versioned freeze manifest approved for an experiment campaign. “Current” files remain mutable during discovery; frozen identifiers and hashes do not.
