from __future__ import annotations

from typing import Literal

from pydantic import Field
from pydantic.types import StrictBool

from ..records import VersionedRecord
from ..schemas import Identifier
from .calibration import CalibrationStatus


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
