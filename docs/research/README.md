# Research Documentation

This folder explains the scientific design in human-readable form. OpenSpec defines software behavior; these pages explain the research questions, methods, measurements, and validity choices.

## Core reading

Read these first:

1. [Research questions](research-questions.md) — what the study asks.
2. [Experimental design](experimental-design.md) — which adaptation methods and comparisons are planned.
3. [Evaluation strategy](evaluation.md) — how open answers, structured tasks, RAG, stability, and efficiency are assessed.
4. [Statistics](statistics.md) — how effects and uncertainty are analysed.
5. [Validity threats](validity-threats.md) — contamination, bias, confounding, and other threats to interpretation.
6. [Benchmark design](benchmark-design.md) — domain, task classes, languages, and dataset boundaries.

Definitions of methods, metrics, and technologies are kept in the project [glossary](../glossary.md).

## Current development pilot

For the work currently awaiting human review, use:

- [Scenario review](development-pilot-scenario-review.md) — all 24 questions, one-sentence reviewer-only expected answers, and exact frozen Kubernetes source links.
- [Scenario-input construction notes](development-pilot-scenario-inputs.md) — custody and construction details.
- [Source and rights manifest](development-pilot-source-rights-manifest.md) — exact Kubernetes releases, files, hashes, licences, and attribution.

The reviewer-only expected-answer notes are not goldens or evaluator inputs and must not be reused as model, retrieval, training, calibration, or final-test material.

## Reference and audit material

The longer pilot protocol, authorization, pre-authoring freeze, feasibility review, and versioned JSON manifests exist to make decisions reproducible and auditable. They are reference material; they are **not required front-to-back reading** for ordinary project navigation.

Use [Project Status](../project/status.md) to determine which reference artifact is currently relevant.
