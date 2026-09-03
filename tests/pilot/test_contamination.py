from __future__ import annotations

import pytest

from tests.pilot.progress import clean_contamination_audits
from thesis_bench.pilot import (
    AuditMethod,
    AuditOutcome,
    ContaminationAudit,
    ContaminationEvidence,
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


def test_contamination_evidence_requires_the_complete_detector_set() -> None:
    with pytest.raises(ValueError, match="detector"):
        ContaminationEvidence(
            schema_version=1,
            direct_match=False,
            pending_semantic_match=False,
        )


def test_contamination_evidence_derives_pending_semantic_matches_from_audits() -> None:
    audits = list(clean_contamination_audits())
    semantic_index = next(
        index for index, audit in enumerate(audits) if audit.method == AuditMethod.SEMANTIC
    )
    audits[semantic_index] = audits[semantic_index].model_copy(
        update={
            "outcome": AuditOutcome.UNRESOLVED,
            "exposure_layer": "semantic-pattern",
            "adjudication": "not_applicable",
        }
    )

    evidence = ContaminationEvidence(
        schema_version=1,
        direct_match=False,
        pending_semantic_match=True,
        audits=tuple(audits),
    )

    assert evidence.pending_semantic_match is True
