from __future__ import annotations

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    APPROVED_SOURCE_RIGHTS_MANIFEST,
    AcceptedSemanticAlternative,
    AssessmentSource,
    CriterionAssessment,
    CriterionDisposition,
    CriterionRole,
    FrozenSourceIdentity,
    KnowledgeScoreConfiguration,
    Language,
    ProtectedArtifact,
    ProtectedArtifactState,
    ProtectedCriterion,
    ProtectedSemanticContract,
    SemanticCriterion,
    SourceEvidenceReference,
    TaskClass,
)
from thesis_bench.records import ProtectedRootReference


def source_identity() -> FrozenSourceIdentity:
    return FrozenSourceIdentity(
        schema_version=1,
        source_entry_id="source-entry-1",
        source_registry_id=APPROVED_SOURCE_RIGHTS_MANIFEST,
        inventory_id="website-v1.36.4-development-pilot-v1",
        source_kind="website_markdown",
        repository="https://github.com/kubernetes/website",
        release="v1.36.4",
        revision="1de955ebabe7e17da1ebb4f582635491227f4157",
        path_or_selector="content/en/docs/concepts/configuration/configmap.md",
        git_blob_sha1="aa3e6ac3c18b995a2057bd1f8ca19eb6861606e7",
        content_sha256="2" * 64,
        content_index_sha256="ff6e098274f45cf35dd669d0de61e566129e891baad8e0e49d7fe6922c432127",
    )


def evidence(evidence_id: str) -> SourceEvidenceReference:
    return SourceEvidenceReference(
        schema_version=1,
        evidence_id=evidence_id,
        source=source_identity(),
        source_role="construction",
    )


def artifact(label: str = "evaluator-contract", state: str = "frozen") -> ProtectedArtifact:
    digest = "c" * 64
    return ProtectedArtifact(
        schema_version=1,
        artifact_id=f"{label}-1",
        artifact_kind="evaluator-contract",
        revision="v1",
        content_sha256=digest,
        state=ProtectedArtifactState(state),
        root_reference=ProtectedRootReference(
            schema_version=1,
            root_id=APPROVED_PROTECTED_ROOT,
            relative_path=f"{label}/synthetic-1.json",
            content_sha256=digest,
        ),
    )


def knowledge_contract() -> ProtectedSemanticContract:
    criteria = (
        ProtectedCriterion(
            schema_version=1,
            criterion_id="claim-a",
            roles=(CriterionRole.REQUIRED_CLAIM, CriterionRole.SEMANTIC),
            accepted_alternatives=(
                AcceptedSemanticAlternative(
                    schema_version=1,
                    alternative_id="claim-a-alt",
                    criterion_id="claim-a",
                    relation="paraphrase",
                ),
            ),
            evidence_ids=("evidence-a",),
        ),
        ProtectedCriterion(
            schema_version=1,
            criterion_id="claim-b",
            roles=(CriterionRole.REQUIRED_CLAIM, CriterionRole.SEMANTIC),
            evidence_ids=("evidence-b",),
        ),
        ProtectedCriterion(
            schema_version=1,
            criterion_id="unsupported-a",
            roles=(CriterionRole.UNSUPPORTED_OR_CONTRADICTORY, CriterionRole.SEMANTIC),
            evidence_ids=("evidence-u",),
        ),
    )
    return ProtectedSemanticContract(
        schema_version=1,
        artifact=artifact(),
        family_id="synthetic-family-1",
        scenario_input_id="synthetic-input-1",
        scenario_input_sha256="d" * 64,
        task_class=TaskClass.KNOWLEDGE,
        language=Language.EN,
        source_rights_manifest_id=APPROVED_SOURCE_RIGHTS_MANIFEST,
        preauthoring_freeze_id="development-pilot-preauthoring-freeze-v1",
        evaluation_clarification_id="development-pilot-evaluation-clarification-v1",
        evaluator_identity={
            "schema_version": 1,
            "identity_id": "evaluator-contract-1",
            "revision": "v1",
            "content_sha256": "c" * 64,
        },
        criteria=criteria,
        semantic_criteria=(
            SemanticCriterion(schema_version=1, criterion_id="claim-a", anchor_id="anchor-a"),
            SemanticCriterion(schema_version=1, criterion_id="claim-b", anchor_id="anchor-b"),
            SemanticCriterion(
                schema_version=1,
                criterion_id="unsupported-a",
                anchor_id="anchor-unsupported",
                allowed_assessor_modes=("human_adjudication",),
            ),
        ),
        evidence=(evidence("evidence-a"), evidence("evidence-b"), evidence("evidence-u")),
        score_configuration=KnowledgeScoreConfiguration(
            schema_version=1,
            required_criterion_ids=("claim-a", "claim-b"),
            unsupported_criterion_ids=("unsupported-a",),
        ),
    )


def assessment(
    criterion_id: str,
    disposition: CriterionDisposition,
    source: AssessmentSource = AssessmentSource.DETERMINISTIC,
    *,
    judge_config_id: str | None = None,
    review_id: str | None = None,
) -> CriterionAssessment:
    return CriterionAssessment(
        schema_version=1,
        assessment_id=f"assessment-{criterion_id}-{disposition.value}",
        criterion_id=criterion_id,
        disposition=disposition,
        source=source,
        assessor_id="assessor-1",
        judge_config_id=judge_config_id,
        review_id=review_id,
    )


def complete_knowledge_assessments(
    claim_a: CriterionDisposition = CriterionDisposition.SATISFIED,
    claim_b: CriterionDisposition = CriterionDisposition.SATISFIED,
    unsupported: CriterionDisposition = CriterionDisposition.NOT_SATISFIED,
) -> tuple[CriterionAssessment, ...]:
    return (
        assessment("claim-a", claim_a),
        assessment("claim-b", claim_b),
        assessment("unsupported-a", unsupported),
    )
