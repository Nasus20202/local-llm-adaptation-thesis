from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Sequence
from enum import StrEnum
from typing import Literal

from pydantic import Field
from pydantic.types import StrictBool, StrictInt

from ..records import VersionedRecord
from ..schemas import Identifier
from .statistics import adjacent_agreement, exact_agreement


class CalibrationStatus(StrEnum):
    GO = "GO"
    AMEND = "AMEND"
    STOP_DEFER = "STOP/DEFER"


class CalibrationSummary(VersionedRecord):
    summary_id: Identifier
    status: CalibrationStatus
    exact_by_criterion: dict[Identifier, float]
    adjacent_by_criterion: dict[Identifier, float]
    confusion_tables: dict[Identifier, dict[str, dict[str, int]]]
    alpha: float
    interval: tuple[float, float]
    critical_exact: dict[Identifier, float]
    systematic_critical_disagreement: StrictBool
    qualification_attempt: StrictInt = Field(default=1, ge=1)


def calibration_summary(
    observations: Sequence[tuple[str, str, int, int]],
    *,
    critical_criteria: Iterable[str] = (),
    primary_criteria: Iterable[str] | None = None,
    level: Literal["nominal", "ordinal"] = "ordinal",
    seed: int = 1,
    draws: int = 10_000,
    summary_id: str = "calibration-1",
    qualification_attempt: int = 1,
) -> CalibrationSummary:
    # Resolve patchable public collaborators at call time for compatibility
    # with callers that replace the facade functions in deterministic tests.
    from . import family_clustered_interval, krippendorff_alpha

    if not observations:
        raise ValueError("calibration requires observations")
    if qualification_attempt < 1:
        raise ValueError("qualification attempt must be positive")
    critical_set = set(critical_criteria)
    by_criterion: dict[str, list[tuple[int, int]]] = defaultdict(list)
    grouped: dict[str, list[tuple[str, tuple[int, int]]]] = defaultdict(list)
    tables: dict[str, dict[str, dict[str, int]]] = {}
    for family_id, criterion_id, left, right in observations:
        by_criterion[criterion_id].append((left, right))
        grouped[criterion_id].append((family_id, (left, right)))
        table = tables.setdefault(criterion_id, defaultdict(dict))
        row = table.setdefault(str(left), {})
        row[str(right)] = row.get(str(right), 0) + 1
    exact = {criterion: exact_agreement(pairs) for criterion, pairs in by_criterion.items()}
    adjacent = {criterion: adjacent_agreement(pairs) for criterion, pairs in by_criterion.items()}
    missing_critical = critical_set - set(by_criterion)
    if missing_critical:
        raise ValueError("declared critical criteria are missing from observations")
    primary_set = (
        set(by_criterion) - critical_set if primary_criteria is None else set(primary_criteria)
    )
    if not primary_set or not primary_set <= set(by_criterion):
        raise ValueError("primary rubric criteria are missing from observations")
    units = tuple(
        (left, right) for _, criterion, left, right in observations if criterion in primary_set
    )
    alpha = krippendorff_alpha(units, level=level)
    all_grouped = tuple(
        (family_id, pair)
        for criterion, criterion_rows in grouped.items()
        if criterion in primary_set
        for family_id, pair in criterion_rows
    )
    interval = family_clustered_interval(
        all_grouped,
        lambda rows: krippendorff_alpha(tuple(value for _, value in rows), level=level),
        seed=seed,
        draws=draws,
    )
    critical = {criterion: exact[criterion] for criterion in critical_set}
    # A fully disagreeing critical binary label is the frozen operational
    # definition of systematic critical disagreement for pilot progression.
    systematic_critical_disagreement = any(value == 0.0 for value in critical.values())
    critical_ok = all(value >= 0.90 for value in critical.values())
    if systematic_critical_disagreement:
        status = CalibrationStatus.STOP_DEFER
    elif alpha >= 0.80 and interval[0] >= 0.67 and critical_ok:
        status = CalibrationStatus.GO
    elif alpha < 0.67:
        status = CalibrationStatus.STOP_DEFER
    else:
        status = CalibrationStatus.AMEND
    if qualification_attempt > 1 and status != CalibrationStatus.GO:
        status = CalibrationStatus.STOP_DEFER
    normalized_tables = {
        criterion: {row: dict(columns) for row, columns in table.items()}
        for criterion, table in tables.items()
    }
    return CalibrationSummary(
        schema_version=1,
        summary_id=summary_id,
        status=status,
        exact_by_criterion=exact,
        adjacent_by_criterion=adjacent,
        confusion_tables=normalized_tables,
        alpha=alpha,
        interval=interval,
        critical_exact=critical,
        systematic_critical_disagreement=systematic_critical_disagreement,
        qualification_attempt=qualification_attempt,
    )
