from __future__ import annotations

from thesis_bench.pilot import (
    ContaminationEvidence,
    DeterministicEvaluationEvidence,
    FairnessEvidence,
    HeadroomEvidence,
    HeadroomStratumEvidence,
    HumanCalibrationEvidence,
    InvalidityEvidence,
    KindEvidence,
    ProgressCriterion,
    ProgressEvidence,
    ProgressObservation,
    ResearcherFeasibilityEvidence,
    SolvabilityEvidence,
    W1Evidence,
)
from thesis_bench.records import DecisionStatus, ReasonCode


def valid_progress_observations() -> tuple[ProgressObservation, ...]:
    evidence = {
        ProgressCriterion.DETERMINISTIC_EVALUATION: ProgressEvidence(
            schema_version=1,
            deterministic=DeterministicEvaluationEvidence(
                schema_version=1, agreement=1.0, idempotent=True
            ),
        ),
        ProgressCriterion.HUMAN_CALIBRATION: ProgressEvidence(
            schema_version=1,
            human=HumanCalibrationEvidence(
                schema_version=1,
                alpha=0.9,
                lower_bound=0.8,
                critical_exact_min=1.0,
                systematic_critical_disagreement=False,
                qualification_attempt=1,
            ),
        ),
        ProgressCriterion.SOLVABILITY: ProgressEvidence(
            schema_version=1,
            solvability=SolvabilityEvidence(
                schema_version=1, solvable_rate=0.9, complete_evidence_mapping=True
            ),
        ),
        ProgressCriterion.HEADROOM: ProgressEvidence(
            schema_version=1,
            headroom=HeadroomEvidence(
                schema_version=1,
                target_stratum_ids=("synthetic-stratum",),
                strata=(
                    HeadroomStratumEvidence(
                        schema_version=1,
                        stratum_id="synthetic-stratum",
                        success_rate=0.5,
                        has_success=True,
                        has_failure=True,
                    ),
                ),
                construct_mismatch=False,
            ),
        ),
        ProgressCriterion.INVALIDITY: ProgressEvidence(
            schema_version=1, invalidity=InvalidityEvidence(schema_version=1, invalidity_rate=0.0)
        ),
        ProgressCriterion.FAIRNESS: ProgressEvidence(
            schema_version=1,
            fairness=FairnessEvidence(
                schema_version=1,
                provenance_complete=True,
                matched_permissions=True,
                hidden_information=False,
                unequal_permissions=False,
                uncaptured_mutation=False,
            ),
        ),
        ProgressCriterion.CONTAMINATION: ProgressEvidence(
            schema_version=1,
            contamination=ContaminationEvidence(
                schema_version=1, direct_match=False, pending_semantic_match=False
            ),
        ),
        ProgressCriterion.KIND: ProgressEvidence(
            schema_version=1,
            kind=KindEvidence(
                schema_version=1,
                isolation_safe=True,
                privilege_safe=True,
                egress_safe=True,
                permission_safe=True,
            ),
        ),
        ProgressCriterion.W1: ProgressEvidence(
            schema_version=1,
            w1=W1Evidence(
                schema_version=1,
                provenance_complete=True,
                access_safe=True,
                redirects_safe=True,
                completion_rate=1.0,
            ),
        ),
        ProgressCriterion.RESEARCHER_FEASIBILITY: ProgressEvidence(
            schema_version=1,
            researcher_feasibility=ResearcherFeasibilityEvidence(schema_version=1, feasible=True),
        ),
    }
    return tuple(
        ProgressObservation(
            schema_version=1,
            criterion=criterion,
            status=DecisionStatus.GO,
            reason_codes=(ReasonCode.OK,),
            observation=f"synthetic {criterion.value}",
            evidence=evidence[criterion],
        )
        for criterion in ProgressCriterion
    )
