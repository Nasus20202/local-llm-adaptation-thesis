## 1. Freeze compatibility and readability checks

- [x] 1.1 Add failing compatibility tests that explicitly inventory every current public name exported by `pilot`, `evaluation`, `cluster`, and `web`, plus the public names consumed from `config` and `provenance`; verify the tests pass against the pre-refactor modules and will fail for a missing facade export.
- [x] 1.2 Add representative pre-move characterization tests for validation, serialized JSON/canonical hashes, redacted errors, append-only collisions, deterministic seeded calculations, and import-time external-effect isolation; verify each test passes without changing an existing expected value.
- [x] 1.3 Review physical line counts for every hand-written Python file under `src/` and `tests/`; record that the 250-line readability target is met without retaining a structure-only test.

## 2. Modularize configuration and provenance

- [x] 2.1 Convert `config.py` into the `config` compatibility package with focused YAML parsing, validation/hashing, path resolution, and assembly modules; verify configuration, example, CLI, and facade-compatibility tests preserve current errors, identities, hashes, and imports.
- [x] 2.2 Split oversized configuration tests by parsing, validation, path resolution, and assembly behavior under `tests/config`, sharing only narrow setup fixtures; verify every resulting test file is at most 250 lines and all original configuration test cases remain collected.
- [x] 2.3 Convert `provenance.py` into the `provenance` compatibility package with focused record, capture, assembly, and serialization modules; verify provenance, lifecycle, CLI, and facade-compatibility tests preserve manifest bytes, hashes, errors, and imports.

## 3. Modularize pilot and evaluation domains

- [x] 3.1 Convert `pilot.py` into the `pilot` compatibility package with separate manifest, contamination, progression, C2 eligibility, and serialization/composition responsibilities; verify the full pilot and integration tests preserve every validator, status, protected-content boundary, and public export.
- [x] 3.2 Split pilot tests by manifest/composition, protected serialization, contamination, progression, and C2 behavior under `tests/pilot`, using behavior-named modules and narrow fixtures; verify every resulting test file is at most 250 lines and the pre-move pilot test inventory remains collected.
- [x] 3.3 Convert `evaluation.py` into the `evaluation` compatibility package with separate identity/fixture, rubric/rating/adjudication, calibration statistics, invalidity/sensitivity, and judge-policy responsibilities; verify evaluation and integration tests preserve exact seeded outputs, thresholds, append-only behavior, and public exports.
- [x] 3.4 Split evaluation tests by fixture qualification, rubric/rating/adjudication, calibration statistics, and invalidity/judge-policy behavior under `tests/evaluation`; verify every resulting test file is at most 250 lines and the pre-move evaluation test inventory remains collected.

## 4. Modularize external-boundary domains

- [x] 4.1 Convert `cluster.py` into the `cluster` compatibility package with separate environment/policy records, adapter/fake, attempt execution/capture, final-state evaluation, and qualification/entry-point responsibilities; verify cluster tests preserve policy hashes, denial outcomes, budgets, append-only capture, qualification, and public exports without starting a real cluster.
- [x] 4.2 Split cluster tests by policy/environment, attempt execution/capture, final-state evaluation, and qualification behavior under `tests/cluster`; verify every resulting test file is at most 250 lines and the pre-move cluster test inventory remains collected.
- [x] 4.3 Convert `web.py` into the `web` compatibility package with separate policy/URL controls, provider/fake, retrieval records/persistence, budgeted attempt execution, and drift/qualification/entry-point responsibilities; verify web tests preserve URL denial, redirect revalidation, budgets, write-before-expose behavior, qualification, and public exports without network access.
- [x] 4.4 Split web tests by policy/URL safety, provider/retrieval capture, budgeted execution, and qualification behavior under `tests/web`; verify every resulting test file is at most 250 lines and the pre-move web test inventory remains collected.

## 5. Verify architecture and behavior preservation

- [x] 5.1 Inspect physical line counts and package dependency direction; verify all hand-written Python files are at most 250 physical lines, facades use explicit exports, and no runtime import cycle or generic utility/framework layer was introduced.
- [x] 5.2 Run `uv run ruff format --check src tests`, `uv run ruff check src tests`, and `uv run mypy src`; verify all formatting, lint, and type checks pass.
- [x] 5.3 Run `uv run coverage run -m pytest -q` and `uv run coverage report`; verify the complete suite passes, all pre-refactor tests remain represented, and no model, network, real cluster, or final-test operation occurs.
- [x] 5.4 Run `uv lock --check`, `uv build`, and `uv run thesis-bench validate-config examples/foundation/experiment.yaml`; verify the lock, package build, installed import paths, CLI behavior, and example identity validation remain unchanged in meaning.
- [x] 5.5 Run `npm ci --ignore-scripts --no-audit --no-fund`, `./node_modules/.bin/renovate-config-validator renovate.json`, and `./node_modules/.bin/openspec validate --all --strict --no-interactive`; verify dependency configuration and every OpenSpec change pass strict validation.
- [x] 5.6 Inspect the complete diff against the public export inventory, approved pilot-foundation requirements, and this design; verify no schema field, default, threshold, serialized form, hash, error redaction, CLI contract, scientific rule, dependency, or opt-in external boundary changed, and record exact verification outcomes in the implementation pull request.
