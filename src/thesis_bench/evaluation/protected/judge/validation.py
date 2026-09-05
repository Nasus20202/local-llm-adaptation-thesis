"""Compatibility facade for protected judge validation."""

from .configuration import validate_judge_configuration, validate_judge_successor
from .eligibility import (
    validate_judge_qualification,
    validate_judge_qualification_successor,
    validate_primary_judge_assessment,
)
from .fairness import check_copying_neutral_fairness, validate_fairness_coverage
from .qualification import qualify_judge_configuration

__all__ = [
    "check_copying_neutral_fairness",
    "qualify_judge_configuration",
    "validate_fairness_coverage",
    "validate_judge_configuration",
    "validate_judge_qualification",
    "validate_judge_qualification_successor",
    "validate_judge_successor",
    "validate_primary_judge_assessment",
]
