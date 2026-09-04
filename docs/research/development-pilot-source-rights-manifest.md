# Development-only Pilot Source and Rights Manifest

## Gate status

- **Manifest ID:** `development-pilot-source-rights-v1`
- **Decision state:** proposed for human review; not frozen
- **Scope:** source and rights selection required by Issue [#35](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/35) before development-only family construction
- **Review date:** 2026-09-04

This manifest records a concrete selection within the approved benchmark methodology. It does not construct a family, item, fixture, expected answer, evidence map, rubric, golden, training record, or final-test artifact. It authorizes no model, real-cluster, live-web, or formal experimental execution.

The selection becomes frozen only after the human researcher approves this exact manifest and the reviewed change is merged. Any content change, path expansion, release substitution, or rights-condition change requires a successor manifest and human review before affected material is used.

## Proposed decision

Use one supported Kubernetes line and one exact patch release:

- **Kubernetes release:** `v1.36.4`
- **Documentation snapshot:** `kubernetes/website` commit `1de955ebabe7e17da1ebb4f582635491227f4157`
- **API snapshot:** `kubernetes/kubernetes` commit `bb826b1d48562f110659e64e8ec444327433db95`, reached by annotated tag `v1.36.4`
- **Included material:** the 44 English Markdown files listed below and `api/openapi-spec/swagger.json` only

This is the smallest source set judged capable of supporting the approved workload-configuration and troubleshooting scope across knowledge, procedural, and mixed families. Kubernetes 1.36 remains supported, has received multiple patch releases, and the frozen documentation commit explicitly maps its `v1.36` documentation to Kubernetes `v1.36.4`. The newly released 1.37 line is not needed for the pilot, and older lines provide no methodological benefit.

## Verified upstream facts

| Fact | Verification |
|---|---|
| The `v1.36.4` annotated tag object is `b16731bd963a0f0b4ca934ffbd7e56cef33df20e` and points to commit `bb826b1d48562f110659e64e8ec444327433db95`. | [Annotated tag](https://github.com/kubernetes/kubernetes/releases/tag/v1.36.4) and [commit](https://github.com/kubernetes/kubernetes/commit/bb826b1d48562f110659e64e8ec444327433db95) inspected on 2026-09-04. The GitHub release was published at `2026-08-20T11:48:16Z`; the tagger and release commit timestamps are `2026-08-20T03:06:27Z`. |
| The frozen website commit is on `release-1.36`, was committed at `2026-08-26T17:35:38Z`, and has tree `08ecfe55ac70f4c19ab581990e5b2718b1668abc`. | [Website commit](https://github.com/kubernetes/website/commit/1de955ebabe7e17da1ebb4f582635491227f4157). |
| At that commit, `hugo.toml` declares `version = "v1.36"`, `githubbranch = "v1.36.4"`, and `docsbranch = "release-1.36"`. | [`hugo.toml`](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/hugo.toml), Git blob `8c574d7dea65fb152943691b7bb2bdc365999143`, SHA-256 `4540b5bb0d536ce62315414eb591d57ab81ac4c79bf185b352ea2af4f9ac22ad`. |
| The `kubernetes/website` root license is Creative Commons Attribution 4.0 International. | [`LICENSE`](https://github.com/kubernetes/website/blob/1de955ebabe7e17da1ebb4f582635491227f4157/LICENSE), Git blob `da6ab6cc8f333d7e89a99812866df8f24374d47c`, SHA-256 `9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411`. |
| The `kubernetes/kubernetes` root license is Apache License 2.0. | [`LICENSE`](https://github.com/kubernetes/kubernetes/blob/bb826b1d48562f110659e64e8ec444327433db95/LICENSE), Git blob `d645695673349e3947e8e5ae42332d0ac3164cd7`, SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`. |
| No path-local `LICENSE`, `NOTICE`, `COPYING`, or `AUTHORS` file occurs in the selected 44-file website allowlist. The selected Kubernetes source revision has no root `NOTICE` file and the selected OpenAPI path has no local legal marker. | Complete Git trees at the immutable commits were inspected on 2026-09-04. This finding is limited to the selected paths and their repository-level legal files. |

The tag and branch names are explanatory aliases. Full commit IDs, file paths, and hashes are the controlling identities because upstream aliases can move.

## Exact source inventory

### `website-v1.36.4-development-pilot-v1`

| Field | Frozen value |
|---|---|
| Repository | `https://github.com/kubernetes/website` |
| Commit | `1de955ebabe7e17da1ebb4f582635491227f4157` |
| Tree | `08ecfe55ac70f4c19ab581990e5b2718b1668abc` |
| Release relationship | `release-1.36` documentation declaring Kubernetes `v1.36.4` in `hugo.toml` |
| Retrieval/review date | 2026-09-04 UTC |
| Included form | Literal UTF-8 bytes of the 44 allowlisted Markdown files; no rendered-site expansion |
| File count / byte count | 44 files / 1,792,346 bytes |
| Content-index SHA-256 | `ff6e098274f45cf35dd669d0de61e566129e891baad8e0e49d7fe6922c432127` |
| License | CC BY 4.0 |
| Intended role | Human construction evidence and the canonical English closed-corpus source for both language strata; later R1 use still requires its normal execution gate |

The content-index digest is SHA-256 over the bytewise path-sorted index whose line format is `<file-SHA-256><two spaces><repository-relative path><LF>`. Each file hash is calculated over the exact Git blob content. Reproduction must obtain all files from the frozen commit, regenerate the index, and require an exact digest match before use.

Exact allowlist:

```text
content/en/docs/concepts/overview/working-with-objects/labels.md
content/en/docs/concepts/configuration/configmap.md
content/en/docs/concepts/configuration/secret.md
content/en/docs/concepts/configuration/manage-resources-containers.md
content/en/docs/concepts/scheduling-eviction/assign-pod-node.md
content/en/docs/concepts/scheduling-eviction/taint-and-toleration.md
content/en/docs/concepts/scheduling-eviction/topology-spread-constraints.md
content/en/docs/concepts/scheduling-eviction/pod-priority-preemption.md
content/en/docs/concepts/workloads/controllers/deployment.md
content/en/docs/concepts/workloads/controllers/job.md
content/en/docs/concepts/workloads/controllers/cron-jobs.md
content/en/docs/concepts/workloads/controllers/daemonset.md
content/en/docs/concepts/workloads/controllers/statefulset.md
content/en/docs/concepts/workloads/pods/pod-lifecycle.md
content/en/docs/concepts/workloads/pods/probes.md
content/en/docs/concepts/workloads/pods/init-containers.md
content/en/docs/concepts/workloads/pods/pod-qos.md
content/en/docs/concepts/services-networking/service.md
content/en/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes.md
content/en/docs/tasks/configure-pod-container/configure-pod-configmap.md
content/en/docs/tasks/configure-pod-container/assign-cpu-resource.md
content/en/docs/tasks/configure-pod-container/assign-memory-resource.md
content/en/docs/tasks/configure-pod-container/assign-pods-nodes.md
content/en/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity.md
content/en/docs/tasks/configmap-secret/managing-secret-using-config-file.md
content/en/docs/tasks/debug/debug-application/debug-init-containers.md
content/en/docs/tasks/debug/debug-application/debug-pods.md
content/en/docs/tasks/debug/debug-application/debug-service.md
content/en/docs/tasks/debug/debug-application/debug-statefulset.md
content/en/docs/tasks/debug/debug-application/determine-reason-pod-failure.md
content/en/docs/tasks/run-application/run-stateless-application-deployment.md
content/en/docs/tasks/run-application/scale-deployment.md
content/en/docs/tasks/run-application/update-deployment-rolling.md
content/en/docs/tasks/job/automated-tasks-with-cron-jobs.md
content/en/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch.md
content/en/docs/reference/kubernetes-api/core/pod-v1.md
content/en/docs/reference/kubernetes-api/core/service-v1.md
content/en/docs/reference/kubernetes-api/core/config-map-v1.md
content/en/docs/reference/kubernetes-api/core/secret-v1.md
content/en/docs/reference/kubernetes-api/apps/deployment-v1.md
content/en/docs/reference/kubernetes-api/apps/daemon-set-v1.md
content/en/docs/reference/kubernetes-api/apps/stateful-set-v1.md
content/en/docs/reference/kubernetes-api/batch/job-v1.md
content/en/docs/reference/kubernetes-api/batch/cron-job-v1.md
```

All other website paths are excluded, including localizations, blogs, tutorials outside the allowlist, images, generated assets, and third-party material reached through hyperlinks. Hugo shortcodes, file references, and external links in an included Markdown file do not expand the source boundary: acquisition may preserve or deterministically remove their literal markup, but it may not resolve or fetch referenced content unless a successor rights manifest approves that exact path or source.

### `openapi-v1.36.4-development-pilot-v1`

| Field | Frozen value |
|---|---|
| Repository | `https://github.com/kubernetes/kubernetes` |
| Release/tag | `v1.36.4`; annotated tag object `b16731bd963a0f0b4ca934ffbd7e56cef33df20e` |
| Commit | `bb826b1d48562f110659e64e8ec444327433db95` |
| Tree | `fc33f1c27e7da2f11ad2d9fe5a9dbe86395f0ca4` |
| Included path | `api/openapi-spec/swagger.json` only |
| Git blob / byte count | `fe0a7b9b1da4e54e43c4d77be20f257c10bc9c34` / 4,108,739 bytes |
| Content SHA-256 | `dcede2063da1d7ad62ecb5af8adb6d7fabd0b52385a7fa0048afb491dac90450` |
| Retrieval/review date | 2026-09-04 UTC |
| License | Apache-2.0 |
| Intended role | Machine-readable API/schema reference for deterministic validation and human evidence checking; not model-facing by default |

All other `kubernetes/kubernetes` paths are excluded, including vendored dependencies, examples, test data, binaries, and source-controlled fixtures. Adding an executable example or another schema requires a successor path-level review. The OpenAPI file may enter a later model-facing R1 corpus only if its role is explicitly changed in a reviewed permitted-context manifest before execution.

## Rights and attribution decision

This is a conservative project rights assessment, not legal advice.

| Material | Verified permission | Conditions adopted by this project | Private-repository decision | Publication implication |
|---|---|---|---|---|
| Selected `kubernetes/website` Markdown | CC BY 4.0 permits reproduction, sharing, and adaptation. | Identify Kubernetes Contributors and the exact source, link CC BY 4.0, indicate modification/adaptation, preserve supplied notices, avoid endorsement, and impose no downstream restriction on the licensed material. | Fresh development inputs may be committed after human technical/licensing review and item-level provenance. Raw upstream copies and generated RAG artifacts remain outside Git and are reconstructed from this manifest. | Source-derived text or adaptations may be published only with the adopted attribution and modification notice. The public package must not apply terms that prevent recipients from exercising CC BY 4.0 rights in included licensed material. |
| Selected Kubernetes OpenAPI file | Apache-2.0 permits reproduction, derivative works, and distribution, subject to its conditions. | Supply the Apache-2.0 license when distributing the selected file or a derivative; mark modified files; retain applicable copyright, patent, trademark, and attribution notices. The frozen upstream revision has no root `NOTICE` to propagate, but a future source change must recheck this. | The raw OpenAPI file remains outside Git and is reconstructed by commit/path/hash. Derived development validators may be committed if they carry the required provenance and any applicable license/notice treatment. | Publication is permissible in principle under Apache-2.0 compliance. No trademark right or Kubernetes endorsement is claimed. |
| Researcher-authored development scenarios | Original expression is project-authored; some material may be an adaptation of upstream documentation or schema. | Avoid verbatim public questions/answers; use fresh source-transformed scenarios; record source-role references. Conservatively treat any materially adapted CC BY text as carrying CC BY attribution obligations rather than relying on an unreviewed originality conclusion. | May be committed only in the approved model-facing development root after source, rights, technical, language, and custody review. | Publication remains blocked until Issue [#36](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/36) defines the repository-wide license/notices and protected-material exclusions. |
| Protected evaluator material | Upstream rights do not override the approved scientific custody boundary. | Keep expected results, evidence maps, answer-revealing rubrics, adjudication records, and protected fixtures outside the normal repository and every model-facing context. | Must not be committed to the normal repository. Only approved IDs, relative protected references, and hashes may appear. | Must not be published through this decision. A later publication review may release only material whose rights and scientific leakage risk are separately approved. |

Minimum attribution text for any distributed website-derived material:

> Based on Kubernetes documentation by the Kubernetes Contributors, frozen at `kubernetes/website@1de955ebabe7e17da1ebb4f582635491227f4157`, licensed under CC BY 4.0. Changes and selection were made for this research benchmark. No endorsement is implied.

For any distributed OpenAPI copy or derivative, accompany the material with the Apache License 2.0 text, the exact upstream commit/path, and a prominent modification statement when changed.

Private storage does not waive the provenance record. Public redistribution is technically permitted by the identified upstream licenses when their conditions are met, but this manifest does not authorize making the thesis repository public. Issue #36 remains the authority for the repository-wide licensing and publication package.

## Provenance and custody controls

- Acquisition resolves only the full commits and exact paths above. Branch heads, moving tags, current documentation pages, search results, and mirrors are not substitutes.
- The source-acquisition record must capture retrieval timestamp, repository, commit, path, observed Git blob identity, SHA-256, license identity, role, and transformation identity before a selected source is used.
- A missing path, content-index mismatch, file-hash mismatch, license mismatch, or compatibility-evidence mismatch is `STOP/DEFER`; construction does not fall back to a current page.
- Any cleaning, front-matter removal, shortcode removal, or chunking is a deterministic derived transformation with its own version, configuration hash, input hash, and output hash. It cannot fetch or transclude excluded content.
- Canonical English documentation is used for both Polish and English strata. Polish family prose may be natively authored or human-adapted, but no localized website corpus is silently added.
- Source bytes and lawful derived corpus artifacts remain separate from the model-facing development manifest and protected evaluator root. Only a later approved execution configuration may expose the permitted R1 corpus to a model.
- Source/domain exposure is recorded as expected; semantic-pattern exposure is audited; direct-item exposure is controlled by private development custody; parametric exposure remains unknown.
- No final-test path, payload, hash, family, or placeholder is created or inspected. No training material is selected.

## Compatibility with Issue #35

| Issue #35 control | Assessment |
|---|---|
| Development-only use | Compatible. The manifest supplies authoring evidence and a future closed-corpus source only for development material. |
| No final-test material | Compatible. The selection contains public upstream sources only and creates no final-test artifact or reference. |
| Protected split leakage | Compatible if acquisition and transformations remain in the declared source role. Protected evaluator and future training/final roots cannot feed the corpus. |
| Custody and provenance | Compatible. Immutable commits, exact paths, Git identities, SHA-256 identities, roles, and fail-closed acquisition rules are recorded. |
| Contamination audit | Compatible. Public-source exposure is expected and labeled; later source chunks participate in all required detector pair classes without making a contamination-free claim. |
| Evaluation validity | Compatible. One release relationship and one English source set hold document identity constant across languages and conditions. No method outcome informed selection. |
| Optional `kind` and W1 | No authorization. The source release may later anchor their separate manifests, but real `kind` and live W1 remain deferred. |
| Approved thresholds and semantics | Unchanged. This manifest adds no threshold, comparator, C2, statistical, evaluator, or experimental rule. |

## OpenSpec assessment

No OpenSpec change is required. The canonical specifications already require source/provenance identity, protected-content separation, contamination records, and fail-closed boundaries. This manifest supplies concrete governed values without changing observable software behavior. It creates no active OpenSpec package and does not alter the synchronized specifications.

## Assumptions and unresolved risks

### Assumptions adopted for this decision

- The repository-level license applies to each selected file because no path-local legal override was found in the immutable selected paths.
- The website repository's explicit `hugo.toml` mapping is sufficient evidence that its frozen `v1.36` documentation snapshot is compatible with the exact `v1.36.4` API snapshot.
- The 44-file allowlist has enough conceptual, task, troubleshooting, and API-reference coverage for the fixed 24-family pilot. This is a pre-outcome coverage judgment, not evidence of family solvability.

### Residual risks

- Upstream license statements cannot eliminate every third-party-rights claim. External links and non-allowlisted/transcluded files are therefore excluded, and any discovered exception triggers amendment before use.
- Whether a future scenario is legally an adaptation is fact-specific. The project adopts CC BY attribution conservatively, and Issue #36 must review the final publication package.
- Public Kubernetes material may be present in model pretraining. Freezing a recent release and authoring fresh scenarios reduces direct reuse but cannot prove absence of parametric or semantic exposure.
- The website branch can move and the GitHub release object is not the immutable scientific identity. Only the full commits, exact paths, and verified hashes above control reproduction.
- If authoring reveals a necessary topic outside the allowlist, work stops for a successor manifest; the source set is not silently expanded to complete a preferred family.

None of these residual risks blocks private development-only construction under the stated controls. They do block any claim that the source is contamination-free or that repository-wide publication has already been cleared.

## Human decision

**Recommendation: APPROVE.** The source relationship is exact and reproducible, the licenses permit the intended private development and later conditional redistribution, the source set is deliberately bounded, and the remaining uncertainties are controlled without changing the approved methodology.

Approval may be recorded as:

> I approve `development-pilot-source-rights-v1` exactly as proposed. This freezes Kubernetes `v1.36.4`, `kubernetes/website@1de955ebabe7e17da1ebb4f582635491227f4157`, `kubernetes/kubernetes@bb826b1d48562f110659e64e8ec444327433db95`, the exact included paths and hashes, and the stated rights/custody controls. It does not authorize model execution, final-test material or access, training material, a real `kind` cluster, live W1, formal experiments, publication, or any change to approved methodology.
