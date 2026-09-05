from __future__ import annotations

import pytest

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    AssessmentSource,
    CriterionDisposition,
    JudgeQualification,
    Language,
    QualificationAdjudicationBinding,
    QualificationThresholds,
    QualifiedCriterionAssessment,
    TaskClass,
    qualify_judge_configuration,
    validate_judge_configuration,
    validate_primary_judge_assessment,
)
from thesis_bench.records import DecisionStatus, ProtectedRootReference

from .fixtures import assessment
from .judge_fixtures import judge_configuration, judge_fairness_case, rehash_judge_configuration


def qualification_root_reference(
    label: str = "qualification", digest: str = "0" * 64
) -> ProtectedRootReference:
    return ProtectedRootReference(
        schema_version=1,
        root_id=APPROVED_PROTECTED_ROOT,
        relative_path=f"qualification/{label}.json",
        content_sha256=digest,
    )


def test_judge_configuration_fails_closed_when_thresholds_are_deferred() -> None:
    config = judge_configuration()
    with pytest.raises(ValueError, match="threshold"):
        validate_judge_configuration(config, require_primary_eligibility=True)

    qualification = JudgeQualification(
        schema_version=1,
        qualification_id="judge-qualification-1",
        judge_config_id=config.judge_config_id,
        judge_config_sha256=config.content_sha256,
        qualification_set_id=config.qualification_set_id,
        qualification_set_sha256=config.qualification_set_sha256,
        protected_input_contract_id=config.protected_input_contract_id,
        protected_input_contract_sha256=config.protected_input_contract_sha256,
        criterion_agreement={"claim-a": 1.0},
        confusion_matrix={"claim-a": {"satisfied": {"satisfied": 1}}},
        agreement_statistic=None,
        unresolved_count=0,
        schema_failure_count=0,
        qualification_revision="v1",
        qualification_root_reference=qualification_root_reference("deferred", "a" * 64),
        qualification_adjudications=(),
        malformed_output_count=0,
        state="frozen",
        content_sha256="a" * 64,
        fairness_status=DecisionStatus.STOP_DEFER,
        thresholds_satisfied=False,
        status=DecisionStatus.STOP_DEFER,
    )
    with pytest.raises(ValueError, match="threshold"):
        validate_primary_judge_assessment(
            config,
            qualification,
            assessment(
                "claim-a",
                CriterionDisposition.SATISFIED,
                AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
                judge_config_id=config.judge_config_id,
            ),
            task_class=TaskClass.KNOWLEDGE,
            language=Language.EN,
        )


def test_suspended_judge_configuration_requires_requalification_before_primary_use() -> None:
    config = rehash_judge_configuration(
        judge_configuration(),
        qualification_thresholds=QualificationThresholds(
            schema_version=1,
            threshold_set_id="synthetic-test-thresholds",
            minimum_criterion_agreement=0.0,
            minimum_kappa=None,
            maximum_unresolved_rate=1.0,
        ),
        suspension_state="suspended",
        suspension_reason="configuration-drift",
    )
    with pytest.raises(ValueError, match="requalification"):
        validate_judge_configuration(config, require_primary_eligibility=True)


def test_judge_qualification_requires_frozen_thresholds_and_binds_exact_config() -> None:
    config = rehash_judge_configuration(
        judge_configuration(),
        qualification_thresholds=QualificationThresholds(
            schema_version=1,
            threshold_set_id="synthetic-test-thresholds",
            minimum_criterion_agreement=0.0,
            minimum_kappa=None,
            maximum_unresolved_rate=1.0,
        ),
    )
    qualification = qualify_judge_configuration(
        config,
        criterion_agreement={"claim-a": 1.0},
        confusion_matrix={"claim-a": {"satisfied": {"satisfied": 4}}},
        unresolved_count=0,
        schema_failure_count=0,
        fairness_cases=(judge_fairness_case(config),),
        qualification_revision="v1",
        qualification_root_reference=qualification_root_reference("green"),
        qualification_adjudications=(),
    )
    assert qualification.status == DecisionStatus.GO
    assert qualification.thresholds_satisfied is True
    accepted = validate_primary_judge_assessment(
        config,
        qualification,
        assessment(
            "claim-a",
            CriterionDisposition.SATISFIED,
            AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
            judge_config_id=config.judge_config_id,
        ),
        task_class=TaskClass.KNOWLEDGE,
        language=Language.EN,
    )
    assert isinstance(accepted, QualifiedCriterionAssessment)
    assert accepted.judge_config_sha256 == config.content_sha256
    assert accepted.qualification_id == qualification.qualification_id

    changed = rehash_judge_configuration(config, prompt_template_sha256="9" * 64)
    with pytest.raises(ValueError, match="changed"):
        validate_primary_judge_assessment(
            changed, qualification, accepted, task_class=TaskClass.KNOWLEDGE, language=Language.EN
        )


def test_judge_configuration_hash_covers_score_affecting_configuration() -> None:
    config = judge_configuration()
    changed = config.model_copy(update={"prompt_template_sha256": "invalid"})
    with pytest.raises(ValueError):
        validate_judge_configuration(changed)


def test_forged_green_qualification_cannot_authorize_a_judge() -> None:
    config = rehash_judge_configuration(
        judge_configuration(),
        qualification_thresholds=QualificationThresholds(
            schema_version=1,
            threshold_set_id="synthetic-test-thresholds",
            minimum_criterion_agreement=0.0,
            minimum_kappa=None,
            maximum_unresolved_rate=1.0,
        ),
    )
    forged = JudgeQualification(
        schema_version=1,
        qualification_id="forged-qualification",
        judge_config_id=config.judge_config_id,
        judge_config_sha256=config.content_sha256,
        qualification_set_id=config.qualification_set_id,
        qualification_set_sha256=config.qualification_set_sha256,
        protected_input_contract_id=config.protected_input_contract_id,
        protected_input_contract_sha256=config.protected_input_contract_sha256,
        criterion_agreement={"unrelated-criterion": 1.0},
        confusion_matrix={"unrelated-criterion": {"satisfied": {"satisfied": 1}}},
        unresolved_count=0,
        schema_failure_count=0,
        qualification_revision="v1",
        qualification_root_reference=qualification_root_reference("forged", "a" * 64),
        qualification_adjudications=(),
        malformed_output_count=0,
        state="frozen",
        content_sha256="a" * 64,
        fairness_status=DecisionStatus.GO,
        fairness_scope_status={"knowledge-en": DecisionStatus.GO},
        thresholds_satisfied=True,
        status=DecisionStatus.GO,
    )
    with pytest.raises(ValueError):
        validate_primary_judge_assessment(
            config,
            forged,
            assessment(
                "claim-a",
                CriterionDisposition.SATISFIED,
                AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
                judge_config_id=config.judge_config_id,
            ),
            task_class=TaskClass.KNOWLEDGE,
            language=Language.EN,
        )


def test_judge_qualification_requires_nonempty_bound_confusion_evidence() -> None:
    config = rehash_judge_configuration(
        judge_configuration(),
        qualification_thresholds=QualificationThresholds(
            schema_version=1,
            threshold_set_id="synthetic-test-thresholds",
            minimum_criterion_agreement=0.0,
            minimum_kappa=None,
            maximum_unresolved_rate=1.0,
        ),
    )
    qualification = qualify_judge_configuration(
        config,
        criterion_agreement={"claim-a": 1.0},
        confusion_matrix={},
        unresolved_count=0,
        schema_failure_count=0,
        fairness_cases=(judge_fairness_case(config),),
        qualification_revision="v1",
        qualification_root_reference=qualification_root_reference("empty"),
        qualification_adjudications=(),
    )
    assert qualification.status == DecisionStatus.AMEND
    assert qualification.thresholds_satisfied is False


def test_qualification_adjudication_binding_requires_matching_protected_hash() -> None:
    with pytest.raises(ValueError, match="hash"):
        QualificationAdjudicationBinding(
            schema_version=1,
            adjudication_id="adjudication-1",
            content_sha256="a" * 64,
            root_reference=qualification_root_reference("adjudication", "b" * 64),
        )
