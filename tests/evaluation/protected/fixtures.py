from __future__ import annotations

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    APPROVED_SOURCE_RIGHTS_MANIFEST,
    AcceptedSemanticAlternative,
    CriterionRole,
    DeterministicPredicate,
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
    approved_input_registry,
)
from thesis_bench.records import ProtectedRootReference

from .assessment_fixtures import assessment, complete_knowledge_assessments

__all__ = [
    "assessment",
    "complete_knowledge_assessments",
    "artifact",
    "evidence",
    "input_binding",
    "knowledge_contract",
    "semantic_knowledge_contract",
    "source_identity",
]


def source_identity() -> FrozenSourceIdentity:
    return FrozenSourceIdentity(
        schema_version=1,
        source_entry_id="source-entry-1",
        source_registry_id=APPROVED_SOURCE_RIGHTS_MANIFEST,
        inventory_id="openapi-v1.36.4-development-pilot-v1",
        source_kind="openapi_schema",
        repository="https://github.com/kubernetes/kubernetes",
        release="v1.36.4",
        revision="bb826b1d48562f110659e64e8ec444327433db95",
        path_or_selector="api/openapi-spec/swagger.json",
        git_blob_sha1="fe0a7b9b1da4e54e43c4d77be20f257c10bc9c34",
        content_sha256="dcede2063da1d7ad62ecb5af8adb6d7fabd0b52385a7fa0048afb491dac90450",
    )


def input_binding(task_class: TaskClass):
    return next(
        entry
        for entry in approved_input_registry().entries
        if entry.task_class == task_class and entry.language == Language.EN
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
    binding = input_binding(TaskClass.KNOWLEDGE)
    criteria = (
        ProtectedCriterion(
            schema_version=1,
            criterion_id="claim-a",
            roles=(
                CriterionRole.REQUIRED_CLAIM,
                CriterionRole.SEMANTIC,
                CriterionRole.DETERMINISTIC,
            ),
            deterministic_predicate_id="predicate-claim-a",
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
            roles=(
                CriterionRole.REQUIRED_CLAIM,
                CriterionRole.SEMANTIC,
                CriterionRole.DETERMINISTIC,
            ),
            deterministic_predicate_id="predicate-claim-b",
            evidence_ids=("evidence-b",),
        ),
        ProtectedCriterion(
            schema_version=1,
            criterion_id="unsupported-a",
            roles=(
                CriterionRole.UNSUPPORTED_OR_CONTRADICTORY,
                CriterionRole.SEMANTIC,
                CriterionRole.DETERMINISTIC,
            ),
            deterministic_predicate_id="predicate-unsupported-a",
            evidence_ids=("evidence-u",),
        ),
    )
    return ProtectedSemanticContract(
        schema_version=1,
        artifact=artifact(),
        family_id=binding.family_id,
        scenario_input_id=binding.scenario_input_id,
        scenario_input_sha256=binding.input_sha256,
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
        predicates=(
            DeterministicPredicate(
                schema_version=1,
                predicate_id="predicate-claim-a",
                criterion_id="claim-a",
                predicate_kind="custom",
                predicate_version="predicate-v1",
            ),
            DeterministicPredicate(
                schema_version=1,
                predicate_id="predicate-claim-b",
                criterion_id="claim-b",
                predicate_kind="custom",
                predicate_version="predicate-v1",
            ),
            DeterministicPredicate(
                schema_version=1,
                predicate_id="predicate-unsupported-a",
                criterion_id="unsupported-a",
                predicate_kind="custom",
                predicate_version="predicate-v1",
            ),
        ),
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


def semantic_knowledge_contract() -> ProtectedSemanticContract:
    contract = knowledge_contract()
    criteria = tuple(
        criterion.model_copy(
            update={
                "roles": tuple(
                    role for role in criterion.roles if role != CriterionRole.DETERMINISTIC
                ),
                "deterministic_predicate_id": None,
            }
        )
        for criterion in contract.criteria
    )
    return ProtectedSemanticContract.model_validate(
        contract.model_copy(update={"criteria": criteria, "predicates": ()}).model_dump(
            mode="python"
        )
    )
