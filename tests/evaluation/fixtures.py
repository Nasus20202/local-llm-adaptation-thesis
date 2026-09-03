from __future__ import annotations

from thesis_bench.evaluation import (
    DeterministicFixture,
    EvaluatorIdentity,
    FixtureCategory,
    FixtureResult,
    FixtureSetIdentity,
    InputIdentity,
    OutputIdentity,
)


def identities(
    *, input_hash: str = "a" * 64
) -> tuple[EvaluatorIdentity, FixtureSetIdentity, InputIdentity, OutputIdentity]:
    return (
        EvaluatorIdentity(
            schema_version=1,
            identity_id="evaluator-1",
            revision="v1",
            content_sha256="b" * 64,
        ),
        FixtureSetIdentity(
            schema_version=1,
            identity_id="fixtures-1",
            revision="v1",
            content_sha256="c" * 64,
        ),
        InputIdentity(
            schema_version=1,
            identity_id="input-1",
            revision="v1",
            content_sha256=input_hash,
        ),
        OutputIdentity(
            schema_version=1,
            identity_id="output-1",
            revision="v1",
            content_sha256="e" * 64,
        ),
    )


def fixtures() -> tuple[DeterministicFixture, ...]:
    return tuple(
        DeterministicFixture(
            schema_version=1,
            fixture_id=f"fixture-{category.value}",
            category=category,
            expected_outcome="accepted" if category == FixtureCategory.POSITIVE else "rejected",
            expected_reason="ok" if category == FixtureCategory.POSITIVE else category.value,
        )
        for category in FixtureCategory
    )


def evaluate(fixture: DeterministicFixture) -> FixtureResult:
    return FixtureResult(
        schema_version=1,
        outcome=fixture.expected_outcome,
        reason=fixture.expected_reason,
        substantive=fixture.category != FixtureCategory.AMBIGUOUS,
    )
