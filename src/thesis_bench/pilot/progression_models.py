from __future__ import annotations

from enum import StrEnum

from pydantic import Field, model_validator
from pydantic.types import StrictBool, StrictFloat, StrictInt

from ..records import DecisionStatus, ReasonCode, VersionedRecord
from ..schemas import Identifier, NonBlankStr


class ProgressCriterion(StrEnum):
    DETERMINISTIC_EVALUATION = "deterministic_evaluation"
    HUMAN_CALIBRATION = "human_calibration"
    SOLVABILITY = "solvability"
    HEADROOM = "headroom"
    INVALIDITY = "invalidity"
    FAIRNESS = "condition_fidelity_fairness"
    CONTAMINATION = "contamination"
    KIND = "kind"
    W1 = "w1"
    RESEARCHER_FEASIBILITY = "researcher_feasibility"


class DeterministicEvaluationEvidence(VersionedRecord):
    agreement: StrictFloat = Field(ge=0.0, le=1.0)
    idempotent: StrictBool


class HumanCalibrationEvidence(VersionedRecord):
    alpha: StrictFloat = Field(ge=-1.0, le=1.0)
    lower_bound: StrictFloat = Field(ge=-1.0, le=1.0)
    critical_exact_min: StrictFloat = Field(ge=0.0, le=1.0)
    systematic_critical_disagreement: StrictBool
    qualification_attempt: StrictInt = Field(ge=1)


class SolvabilityEvidence(VersionedRecord):
    solvable_rate: StrictFloat = Field(ge=0.0, le=1.0)
    complete_evidence_mapping: StrictBool


class HeadroomStratumEvidence(VersionedRecord):
    stratum_id: Identifier
    success_rate: StrictFloat = Field(ge=0.0, le=1.0)
    has_success: StrictBool
    has_failure: StrictBool


class HeadroomEvidence(VersionedRecord):
    target_stratum_ids: tuple[Identifier, ...] = Field(min_length=1)
    strata: tuple[HeadroomStratumEvidence, ...] = Field(min_length=1)
    construct_mismatch: StrictBool

    @model_validator(mode="after")
    def require_unique_strata(self) -> HeadroomEvidence:
        identifiers = [stratum.stratum_id for stratum in self.strata]
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("headroom strata must be unique")
        if set(identifiers) != set(self.target_stratum_ids):
            raise ValueError("headroom evidence must cover every declared target stratum")
        return self


class InvalidityEvidence(VersionedRecord):
    invalidity_rate: StrictFloat = Field(ge=0.0, le=1.0)


class FairnessEvidence(VersionedRecord):
    provenance_complete: StrictBool
    matched_permissions: StrictBool
    hidden_information: StrictBool
    unequal_permissions: StrictBool
    uncaptured_mutation: StrictBool


class ContaminationEvidence(VersionedRecord):
    direct_match: StrictBool
    pending_semantic_match: StrictBool


class KindEvidence(VersionedRecord):
    isolation_safe: StrictBool
    privilege_safe: StrictBool
    egress_safe: StrictBool
    permission_safe: StrictBool


class W1Evidence(VersionedRecord):
    provenance_complete: StrictBool
    access_safe: StrictBool
    redirects_safe: StrictBool
    completion_rate: StrictFloat = Field(ge=0.0, le=1.0)


class ResearcherFeasibilityEvidence(VersionedRecord):
    feasible: StrictBool


class ProgressEvidence(VersionedRecord):
    deterministic: DeterministicEvaluationEvidence | None = None
    human: HumanCalibrationEvidence | None = None
    solvability: SolvabilityEvidence | None = None
    headroom: HeadroomEvidence | None = None
    invalidity: InvalidityEvidence | None = None
    fairness: FairnessEvidence | None = None
    contamination: ContaminationEvidence | None = None
    kind: KindEvidence | None = None
    w1: W1Evidence | None = None
    researcher_feasibility: ResearcherFeasibilityEvidence | None = None

    @model_validator(mode="after")
    def require_one_typed_summary(self) -> ProgressEvidence:
        if (
            sum(
                value is not None
                for value in (
                    self.deterministic,
                    self.human,
                    self.solvability,
                    self.headroom,
                    self.invalidity,
                    self.fairness,
                    self.contamination,
                    self.kind,
                    self.w1,
                    self.researcher_feasibility,
                )
            )
            != 1
        ):
            raise ValueError("progress evidence must contain exactly one typed summary")
        return self


_PROGRESS_EVIDENCE_FIELDS = {
    ProgressCriterion.DETERMINISTIC_EVALUATION: "deterministic",
    ProgressCriterion.HUMAN_CALIBRATION: "human",
    ProgressCriterion.SOLVABILITY: "solvability",
    ProgressCriterion.HEADROOM: "headroom",
    ProgressCriterion.INVALIDITY: "invalidity",
    ProgressCriterion.FAIRNESS: "fairness",
    ProgressCriterion.CONTAMINATION: "contamination",
    ProgressCriterion.KIND: "kind",
    ProgressCriterion.W1: "w1",
    ProgressCriterion.RESEARCHER_FEASIBILITY: "researcher_feasibility",
}


class ProgressObservation(VersionedRecord):
    criterion: ProgressCriterion
    status: DecisionStatus
    reason_codes: tuple[ReasonCode, ...] = Field(min_length=1)
    observation: NonBlankStr
    evidence: ProgressEvidence
    threshold_version: Identifier = "pilot-thresholds-v1"
    outcome_derived: StrictBool = False

    @model_validator(mode="after")
    def reject_outcome_progression_inputs(self) -> ProgressObservation:
        if self.threshold_version != "pilot-thresholds-v1":
            raise ValueError("unknown progression threshold version")
        expected_field = _PROGRESS_EVIDENCE_FIELDS[self.criterion]
        if getattr(self.evidence, expected_field) is None:
            raise ValueError("progress evidence does not match its criterion")
        lowered = self.observation.lower()
        if self.outcome_derived or any(
            marker in lowered
            for marker in (
                "final-test",
                "final_test",
                "method win",
                "method-win",
                "method_win",
                "best-performing",
                "best_performing",
            )
        ):
            raise ValueError("progression cannot use outcome-derived evidence")
        return self


class ProgressionReport(VersionedRecord):
    report_id: Identifier
    status: DecisionStatus
    observations: tuple[ProgressObservation, ...] = Field(min_length=1)
