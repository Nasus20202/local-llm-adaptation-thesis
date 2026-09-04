# Benchmark Design

## Decision status

This document records the Issue #2 benchmark policy accepted at Human Gate A on 2026-09-02. The approval authorizes preparation of the Issue #4 pilot and evaluator-calibration protocol; it does not authorize item construction. No final item, answer key, or test payload is created by this decision.

## Purpose and intended use

The benchmark measures how adaptation strategies change the performance of locally executed language models on one specialized technical domain. It is not a Kubernetes certification exam or a general model leaderboard.

The intended user is an intermediate application or platform engineer who must interpret upstream documentation, configure Kubernetes application workloads, and diagnose bounded configuration failures.

## Selected domain

The selected domain is **Kubernetes application-workload configuration and troubleshooting** against one version-pinned upstream documentation and API snapshot.

In scope:

- Pods and workload controllers, including Deployments, Jobs, CronJobs, DaemonSets, and bounded StatefulSet behavior;
- Services, labels, selectors, probes, resource requests and limits, ConfigMap and Secret references, scheduling primitives, rollouts, and workload debugging;
- factual interpretation, offline-verifiable configuration or repair, and mixed evidence-plus-artifact tasks;
- canonical upstream concepts, task pages, references, and matching API schemas.

Out of scope:

- cluster installation, distribution-specific administration, cloud-provider behavior, and third-party controllers;
- storage or network-plugin internals, production incident response, destructive operations, and live credentials;
- tasks whose correctness depends on an uncontrolled live cluster, internet access, or a vendor service;
- Kubernetes trivia that does not test an adaptation mechanism or intended-user task.

The exact supported Kubernetes release, website commit, API-schema revision, included paths, and exclusions are frozen before pilot construction. All source components must describe the same compatible release window.

## Alternatives considered

| Alternative                               | Benefit                                                                                         | Methodological cost                                                                                  | Decision                                                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| One Kubernetes workload domain            | Supports knowledge, procedural, and mixed tasks with shared terminology and versionable sources | Limits generalization to one technical domain                                                        | Selected for internal validity and feasible curation                                                       |
| Kubernetes plus a second technical domain | Broader external validity                                                                       | Confounds domain with task class, doubles source and annotation work, and weakens paired comparisons | Rejected for the main benchmark                                                                            |
| Fully synthetic technical world           | Strong leakage control and deterministic grading                                                | Weak ecological validity and uncertain transfer to real technical work                               | Rejected as the main domain; controlled synthetic configurations remain allowed inside the selected domain |

## Source and corpus policy

Primary source material is limited to the official `kubernetes/website` repository and matching artifacts from `kubernetes/kubernetes` when API schemas or executable examples are needed. Documentation is available under CC BY 4.0; Kubernetes source and API artifacts are available under Apache-2.0. Every included source is reviewed for path-level exceptions before redistribution.

The source manifest records repository, full commit ID, release relationship, path, retrieval date, content hash, license, attribution, modification status, redistribution status, and intended role. Canonical English upstream documentation is the primary RAG corpus for both language strata so document identity does not vary by benchmark language. A translated or localization-augmented corpus would be a separate sensitivity condition, not an undocumented substitution.

## Task classes and applicability

### Knowledge

Knowledge tasks require facts or evidence synthesis from the bounded source snapshot. They include direct facts, cross-document synthesis, negative or absent-answer cases, and distractor-heavy cases. Core applicable conditions are B0, P1, R1, and F1.

### Procedural

Procedural tasks require a verifiable configuration, repair, or ordered action plan under explicit constraints. They must not depend mainly on obscure recall. Core applicable conditions are B0, P1, H1, and S1. F1 is applicable only if the approved training target includes the same procedural capability.

### Mixed

Mixed tasks require both source-grounded interpretation and a verifiable artifact or procedure. They are reserved for pre-selected combined-condition tests after the simple components have interpretable evidence.

An inapplicable method is omitted rather than scored as a failure.

## Language policy

Independent item families are allocated **50% Polish and 50% English**, stratified by task class. Technical identifiers, commands, and configuration keys remain canonical.

Polish items are written natively or human-adapted from the pinned sources by a technically competent Polish speaker. Unreviewed machine translation is prohibited for frozen items, evidence mappings, answers, and rubrics. A machine translation may be used only as a draft whose semantic and technical equivalence is then reviewed and recorded.

A small, predeclared subset may contain semantically equivalent Polish and English variants for language-sensitivity analysis. Variants share one family ID, remain in the same split, and are nested observations rather than additional independent items.

## Construction policy

Items use researcher-authored, source-transformed scenarios and controlled Kubernetes configurations. Verbatim public questions and public benchmark answers are avoided. Synthetic manifests or cluster states are allowed when they follow the pinned API and preserve a realistic intended-user task.

GenAI may assist brainstorming or language review only under the project GenAI policy. It cannot be the sole author or verifier of a frozen item, golden answer, evidence mapping, deterministic check, or rubric. Final technical validity and licensing decisions remain human responsibilities.

## Independent unit and item contract

The principal independent unit is the **scenario/item family**. Repeated generations, prompt paraphrases, and language variants are nested observations.

Every item records:

- stable item ID, family ID, language, task class, and subtype;
- source and license/provenance references;
- split and embargo status;
- input, permitted context and tools, and prohibited information;
- expected answer form and deterministic gates;
- protected evidence, answer, rubric, and adjudication notes;
- difficulty and failure-mode tags;
- contamination review status.

## Answer forms

The answer form is fixed per item and identical across compared conditions:

- knowledge: concise prose or atomic claims with requested evidence references;
- procedural: Kubernetes YAML/JSON, a patch, a bounded command/action sequence, or a structured diagnosis;
- mixed: an evidence-grounded decision plus a verifiable artifact or procedure.

No universal response envelope is frozen before the pilot. Each selected form must allow deterministic validation where possible and a versioned rubric where semantic judgment remains necessary.

## Split and custody policy

Semantic families, translated variants, and near-duplicates are grouped before splitting. Training material is visible only to F1; development material supports all method and evaluator decisions; final-test inputs and goldens are immutable after freeze.

The human researcher is the final-test custodian. Before formal execution, final-test payloads and goldens remain outside the normal checkout and AI-accessible workspaces. A committed manifest may expose identifiers and cryptographic hashes but not protected content. At execution, the runner receives only test inputs and permitted context; the evaluator receives goldens through a separate boundary. Prompts, RAG indexes, training data, harnesses, skills, external services, and model-facing logs never receive goldens.

## Contamination controls and limits

Construction performs exact, normalized, and semantic-family checks across all splits and scans prompts, RAG chunks, skills, harness content, tool outputs, and training material for item or answer overlap. Source snapshots and transformations are versioned.

Public Kubernetes documentation may already be present in model pretraining. Exact or semantic scans cannot establish absence from opaque training corpora, and paraphrase or translation can evade overlap detection. The benchmark therefore uses fresh scenarios, version-specific source grounding, negative cases, and controlled configurations, but reports residual parametric contamination as a limitation. It never claims to be contamination-free.

External web search is not an allowed primary condition. Any future search-enabled sensitivity condition requires its own contamination and provenance policy.

## Pilot-only unknowns

Issue #4 must resolve the final item counts, task subtype proportions, paired-language subset size, annotation and adjudication thresholds, deterministic validator coverage, corpus evidence-coverage threshold, ambiguity and ceiling/floor rules, smallest effects of interest, and repetition counts. Pilot work uses development-only items and cannot inspect final-test outcomes.
