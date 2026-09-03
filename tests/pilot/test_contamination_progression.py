from __future__ import annotations

import pytest

from tests.pilot.progress import valid_progress_observations
from thesis_bench.pilot import (
    AuditMethod,
    AuditOutcome,
    ContaminationAudit,
    ContaminationEvidence,
    FairnessEvidence,
    HeadroomEvidence,
    HeadroomStratumEvidence,
    HumanCalibrationEvidence,
    KindEvidence,
    ProgressCriterion,
    ProgressEvidence,
    ProgressObservation,
    SolvabilityEvidence,
    W1Evidence,
    derive_progression,
)
from thesis_bench.records import DecisionStatus, ReasonCode


def test_contamination_records_derive_red_amend_and_reject_pretraining_probability() -> None:
    direct = ContaminationAudit(
        schema_version=1,
        audit_id="audit-direct",
        method=AuditMethod.EXACT,
        detector_version="detector-v1",
        artifact_pair=("development-1", "training-1"),
        threshold="exact",
        outcome=AuditOutcome.MATCH,
        exposure_layer="direct-item",
        adjudication="confirmed",
    )
    semantic = direct.model_copy(
        update={
            "audit_id": "audit-semantic",
            "method": AuditMethod.SEMANTIC,
            "outcome": AuditOutcome.UNRESOLVED,
            "exposure_layer": "semantic-pattern",
            "adjudication": "pending",
        }
    )

    assert direct.progression_status() == DecisionStatus.STOP_DEFER
    assert semantic.progression_status() == DecisionStatus.AMEND
    pending_match = semantic.model_copy(
        update={"outcome": AuditOutcome.MATCH, "audit_id": "audit-semantic-match"}
    )
    assert pending_match.progression_status() == DecisionStatus.AMEND
    assert direct.parametric_exposure == "unknown"
    assert ReasonCode.FAMILY_OVERLAP.value not in direct.model_dump_json()

    with pytest.raises(ValueError):
        ContaminationAudit(
            schema_version=1,
            audit_id="audit-probability",
            method=AuditMethod.EXACT,
            detector_version="detector-v1",
            artifact_pair=("a", "b"),
            threshold="exact",
            outcome=AuditOutcome.NO_MATCH,
            exposure_layer="source-domain",
            adjudication="not_applicable",
            pretraining_probability=0.1,
        )


def test_progression_preserves_criteria_and_safety_red_governs() -> None:
    observations = (
        ProgressObservation(
            schema_version=1,
            criterion=ProgressCriterion.SOLVABILITY,
            status=DecisionStatus.GO,
            reason_codes=(ReasonCode.INVALID_CONFIGURATION,),
            observation="synthetic observation",
            evidence=ProgressEvidence(
                schema_version=1,
                solvability=SolvabilityEvidence(
                    schema_version=1, solvable_rate=0.79, complete_evidence_mapping=True
                ),
            ),
        ),
        ProgressObservation(
            schema_version=1,
            criterion=ProgressCriterion.CONTAMINATION,
            status=DecisionStatus.STOP_DEFER,
            reason_codes=(ReasonCode.PROTECTED_PAYLOAD,),
            observation="synthetic safety observation",
            evidence=ProgressEvidence(
                schema_version=1,
                contamination=ContaminationEvidence(
                    schema_version=1, direct_match=True, pending_semantic_match=False
                ),
            ),
        ),
    )
    with pytest.raises(ValueError, match="approved feasibility criteria"):
        derive_progression(observations)


def test_progression_derives_status_from_frozen_thresholds_not_caller_labels() -> None:
    observations = list(valid_progress_observations())
    observations[2] = observations[2].model_copy(
        update={
            "evidence": ProgressEvidence(
                schema_version=1,
                solvability=SolvabilityEvidence(
                    schema_version=1, solvable_rate=0.01, complete_evidence_mapping=True
                ),
            )
        }
    )
    report = derive_progression(tuple(observations))

    assert report.status == DecisionStatus.STOP_DEFER
    assert report.observations[2].status == DecisionStatus.STOP_DEFER


@pytest.mark.parametrize(
    ("criterion", "expected_reason"),
    [
        (ProgressCriterion.W1, ReasonCode.MISSING_PROVENANCE),
        (ProgressCriterion.KIND, ReasonCode.PERMISSION_FAILURE),
        (ProgressCriterion.FAIRNESS, ReasonCode.POLICY_VIOLATION),
    ],
)
def test_progression_preserves_mandatory_criterion_specific_red_conditions(
    criterion: ProgressCriterion, expected_reason: ReasonCode
) -> None:
    observations = list(valid_progress_observations())
    updates = {
        ProgressCriterion.W1: ProgressEvidence(
            schema_version=1,
            w1=W1Evidence(
                schema_version=1,
                provenance_complete=False,
                access_safe=True,
                redirects_safe=True,
                completion_rate=1.0,
            ),
        ),
        ProgressCriterion.KIND: ProgressEvidence(
            schema_version=1,
            kind=KindEvidence(
                schema_version=1,
                isolation_safe=True,
                privilege_safe=True,
                egress_safe=True,
                permission_safe=False,
            ),
        ),
        ProgressCriterion.FAIRNESS: ProgressEvidence(
            schema_version=1,
            fairness=FairnessEvidence(
                schema_version=1,
                provenance_complete=True,
                matched_permissions=True,
                hidden_information=True,
                unequal_permissions=False,
                uncaptured_mutation=False,
            ),
        ),
    }
    index = tuple(ProgressCriterion).index(criterion)
    observations[index] = observations[index].model_copy(update={"evidence": updates[criterion]})

    report = derive_progression(tuple(observations))

    assert report.observations[index].status == DecisionStatus.STOP_DEFER
    assert expected_reason in report.observations[index].reason_codes


def test_progression_treats_systematic_critical_disagreement_as_red() -> None:
    observations = list(valid_progress_observations())
    observations[1] = observations[1].model_copy(
        update={
            "evidence": ProgressEvidence(
                schema_version=1,
                human=HumanCalibrationEvidence(
                    schema_version=1,
                    alpha=1.0,
                    lower_bound=1.0,
                    critical_exact_min=0.0,
                    systematic_critical_disagreement=True,
                    qualification_attempt=1,
                ),
            )
        }
    )

    report = derive_progression(tuple(observations))

    assert report.observations[1].status == DecisionStatus.STOP_DEFER


def test_progression_requires_success_and_failure_in_every_headroom_stratum() -> None:
    observations = list(valid_progress_observations())
    observations[3] = observations[3].model_copy(
        update={
            "evidence": ProgressEvidence(
                schema_version=1,
                headroom=HeadroomEvidence(
                    schema_version=1,
                    target_stratum_ids=("stratum-a", "stratum-b"),
                    strata=(
                        HeadroomStratumEvidence(
                            schema_version=1,
                            stratum_id="stratum-a",
                            success_rate=0.5,
                            has_success=True,
                            has_failure=False,
                        ),
                        HeadroomStratumEvidence(
                            schema_version=1,
                            stratum_id="stratum-b",
                            success_rate=0.5,
                            has_success=True,
                            has_failure=True,
                        ),
                    ),
                    construct_mismatch=False,
                ),
            )
        }
    )

    report = derive_progression(tuple(observations))

    assert report.observations[3].status == DecisionStatus.AMEND
