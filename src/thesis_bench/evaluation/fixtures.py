from __future__ import annotations

from collections.abc import Callable, Sequence
from enum import StrEnum

from pydantic.types import StrictBool

from ..records import DecisionStatus, VersionedRecord
from ..schemas import Identifier, NonBlankStr


class FixtureCategory(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    BOUNDARY = "boundary"
    MALFORMED = "malformed"
    AMBIGUOUS = "ambiguous"


class DeterministicFixture(VersionedRecord):
    fixture_id: Identifier
    category: FixtureCategory
    expected_outcome: NonBlankStr
    expected_reason: NonBlankStr


class FixtureResult(VersionedRecord):
    outcome: NonBlankStr
    reason: NonBlankStr
    substantive: StrictBool = True


class FixtureQualification(VersionedRecord):
    status: DecisionStatus
    mismatches: tuple[Identifier, ...] = ()
    rejected_ambiguous: tuple[Identifier, ...] = ()


FixtureEvaluator = Callable[[DeterministicFixture], FixtureResult]


def qualify_deterministic_evaluator(
    fixtures: Sequence[DeterministicFixture],
    evaluator: FixtureEvaluator,
    *,
    repeats: int = 2,
) -> FixtureQualification:
    if repeats < 2:
        raise ValueError("qualification requires repeated fixture execution")
    required = set(FixtureCategory)
    present = {fixture.category for fixture in fixtures}
    mismatches: list[str] = []
    if present != required:
        mismatches.append("missing-fixture-category")
    ambiguous: list[str] = []
    seen: set[str] = set()
    for fixture in fixtures:
        if fixture.fixture_id in seen:
            mismatches.append(fixture.fixture_id)
        seen.add(fixture.fixture_id)
        outcomes = [evaluator(fixture) for _ in range(repeats)]
        first = outcomes[0]
        if any(outcome.model_dump() != first.model_dump() for outcome in outcomes[1:]):
            mismatches.append(fixture.fixture_id)
            continue
        if first.outcome != fixture.expected_outcome or first.reason != fixture.expected_reason:
            mismatches.append(fixture.fixture_id)
        if fixture.category == FixtureCategory.AMBIGUOUS:
            if first.substantive:
                mismatches.append(fixture.fixture_id)
            else:
                ambiguous.append(fixture.fixture_id)
    return FixtureQualification(
        schema_version=1,
        status=DecisionStatus.GO if not mismatches else DecisionStatus.AMEND,
        mismatches=tuple(dict.fromkeys(mismatches)),
        rejected_ambiguous=tuple(ambiguous),
    )
