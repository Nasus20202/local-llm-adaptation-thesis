from __future__ import annotations

from collections import Counter
from typing import Literal

from ..records import VersionedRecord
from .manifest import PilotManifest
from .models import Language, TaskClass


class CompositionReport(VersionedRecord):
    valid: Literal[True]
    independent_family_count: int
    nested_variant_count: int


def validate_composition(manifest: PilotManifest) -> CompositionReport:
    violations: list[str] = []
    independent_count = len(manifest.families)
    nested_count = len(manifest.variants)
    if independent_count != 24:
        violations.append("independent-family-count must be 24")
    task_counts = Counter(family.task_class.value for family in manifest.families)
    for task_class in TaskClass:
        if task_counts[task_class.value] != 8:
            violations.append(f"task_class allocation for {task_class.value} must be 8")
    for task_class in TaskClass:
        for language in Language:
            count = sum(
                family.task_class == task_class and family.language == language
                for family in manifest.families
            )
            if count != 4:
                violations.append(
                    f"language allocation for {task_class.value}/{language.value} must be 4"
                )
    if any(variant.counts_as_independent for variant in manifest.variants):
        violations.append("nested variants cannot count as independent families")
    if violations:
        raise ValueError("composition validation failed: " + "; ".join(violations))
    return CompositionReport(
        schema_version=1,
        valid=True,
        independent_family_count=independent_count,
        nested_variant_count=nested_count,
    )
