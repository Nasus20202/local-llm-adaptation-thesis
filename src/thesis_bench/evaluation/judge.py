"""Compatibility facade for judge policy and protected semantic qualification."""

from typing import Literal

from pydantic import Field
from pydantic.types import StrictBool

from ..records import VersionedRecord
from ..schemas import Identifier
from .calibration import CalibrationStatus
from .protected.judge.records import (
    AuditPolicy,
    DecodingPolicy,
    FairnessQualification,
    JudgeConfiguration,
    JudgeFairnessCase,
    JudgeQualification,
    JudgeResponseSchema,
    JudgeScope,
    MetamorphicFixtureGroup,
    MetamorphicVariant,
    MetamorphicVariantKind,
    QualificationThresholds,
)
from .protected.judge.validation import (
    check_copying_neutral_fairness,
    qualify_judge_configuration,
    validate_fairness_coverage,
    validate_judge_configuration,
    validate_judge_successor,
    validate_primary_judge_assessment,
)


class JudgePolicy(VersionedRecord):
    judge_id: Identifier
    model_revision: Identifier
    prompt_revision: Identifier
    languages: tuple[Literal["en", "pl"], ...] = Field(min_length=2)
    calibrated: StrictBool
    primary: StrictBool


class JudgeValidation(VersionedRecord):
    status: CalibrationStatus
    supplemental_only: Literal[True]


def validate_judge_policy(policy: JudgePolicy) -> JudgeValidation:
    if policy.primary:
        raise ValueError("LLM judge cannot be primary")
    if not policy.calibrated:
        raise ValueError("LLM judge is not calibrated")
    if set(policy.languages) != {"en", "pl"}:
        raise ValueError("LLM judge must be calibrated in both languages")
    return JudgeValidation(schema_version=1, status=CalibrationStatus.GO, supplemental_only=True)


__all__ = [
    "AuditPolicy",
    "DecodingPolicy",
    "FairnessQualification",
    "JudgeConfiguration",
    "JudgeFairnessCase",
    "JudgePolicy",
    "JudgeQualification",
    "JudgeResponseSchema",
    "JudgeScope",
    "JudgeValidation",
    "MetamorphicFixtureGroup",
    "MetamorphicVariant",
    "MetamorphicVariantKind",
    "QualificationThresholds",
    "check_copying_neutral_fairness",
    "qualify_judge_configuration",
    "validate_fairness_coverage",
    "validate_judge_configuration",
    "validate_judge_policy",
    "validate_judge_successor",
    "validate_primary_judge_assessment",
]
