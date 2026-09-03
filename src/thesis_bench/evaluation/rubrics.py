from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import Field, ValidationError, field_validator, model_validator
from pydantic.types import StrictBool, StrictInt, StrictStr

from ..records import VersionedRecord, canonical_json_bytes
from ..schemas import Identifier, NonBlankStr


class RubricCriterion(VersionedRecord):
    criterion_id: Identifier
    kind: Literal["ordinal", "binary"]
    anchors: dict[StrictInt, NonBlankStr] = Field(min_length=2)
    critical: StrictBool
    atomic: StrictBool

    @model_validator(mode="after")
    def require_critical_binary(self) -> RubricCriterion:
        if self.critical and self.kind != "binary":
            raise ValueError("critical criteria must be binary")
        return self


def validate_rubric(criteria: Sequence[RubricCriterion]) -> tuple[RubricCriterion, ...]:
    if not criteria:
        raise ValueError("rubric must declare criteria")
    identifiers = [criterion.criterion_id for criterion in criteria]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("rubric criterion identifiers must be unique")
    for criterion in criteria:
        if criterion.criterion_id in {"quality", "overall", "overall-quality"}:
            raise ValueError("universal quality criteria are not allowed")
        if not criterion.atomic:
            raise ValueError("rubric criteria must be atomic")
        if criterion.critical and criterion.kind != "binary":
            raise ValueError("critical criteria must be binary")
        if criterion.kind == "ordinal" and set(criterion.anchors) != {0, 1, 2}:
            raise ValueError("ordinal criteria require three anchored levels")
        if criterion.kind == "binary" and set(criterion.anchors) != {0, 1}:
            raise ValueError("binary criteria require separate yes/no anchors")
    return tuple(criteria)


class RatingRecord(VersionedRecord):
    rating_id: Identifier
    rater_pseudonym: Identifier
    randomized_response_id: Identifier
    criterion_id: Identifier
    value: StrictInt
    rubric_version: Identifier
    rated_at: StrictStr
    independent: Literal[True]
    blinded: Literal[True]

    @field_validator("rated_at")
    @classmethod
    def require_utc_timestamp(cls, value: str) -> str:
        try:
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("timestamp must be ISO-8601 UTC") from exc
        if timestamp.tzinfo is None or timestamp.utcoffset() != UTC.utcoffset(timestamp):
            raise ValueError("timestamp must be ISO-8601 UTC")
        return value


def import_rating(
    raw: dict[str, object], *, rubric: Sequence[RubricCriterion] | None = None
) -> RatingRecord:
    forbidden = {"method", "model", "prompt", "seed", "condition_label", "experimental_condition"}
    if forbidden & raw.keys():
        raise ValueError("qualification rating contains condition information")
    try:
        rating = RatingRecord.model_validate(raw)
    except (ValidationError, TypeError) as exc:
        raise ValueError("rating is incomplete or not blinded and independent") from exc
    if rubric is not None:
        criteria = {criterion.criterion_id: criterion for criterion in validate_rubric(rubric)}
        criterion = criteria.get(rating.criterion_id)
        if criterion is None or rating.value not in criterion.anchors:
            raise ValueError("rating value is not in the frozen rubric anchors")
    return rating


class AdjudicationRecord(VersionedRecord):
    adjudication_id: Identifier
    randomized_response_id: Identifier
    criterion_id: Identifier
    source_rating_ids: tuple[Identifier, ...] = Field(min_length=2)
    labels: tuple[StrictInt, ...] = Field(min_length=2)
    resolved: StrictBool
    adjudicated_value: StrictInt | None = None
    adjudicator_pseudonyms: tuple[Identifier, ...] = ()
    rationale: NonBlankStr | None = None
    sensitivity_flag: StrictBool

    @model_validator(mode="after")
    def validate_resolution(self) -> AdjudicationRecord:
        disagreement = len(set(self.labels)) > 1
        if self.resolved and disagreement:
            if self.adjudicated_value is None:
                raise ValueError("resolved disagreement requires an adjudicated value")
            if self.rationale is None:
                raise ValueError("resolved disagreement requires written rationale")
            if not self.adjudicator_pseudonyms:
                raise ValueError("resolved disagreement requires adjudicator identity")
        if not self.resolved and self.adjudicated_value is not None:
            raise ValueError("unresolved disagreement cannot contain an adjudicated value")
        if len(set(self.adjudicator_pseudonyms)) != len(self.adjudicator_pseudonyms):
            raise ValueError("adjudicator identities must be unique")
        if self.sensitivity_flag != (disagreement and not self.resolved):
            raise ValueError("sensitivity flag must reflect unresolved disagreement")
        return self


def adjudicate_ratings(
    ratings: Sequence[RatingRecord],
    *,
    criterion_kind: Literal["ordinal", "binary"],
    rationale: str | None,
    rubric: Sequence[RubricCriterion] | None = None,
    adjudicated_value: int | None = None,
    adjudicator_pseudonyms: Sequence[str] = (),
    adjudication_id: str = "adjudication-1",
) -> AdjudicationRecord:
    if len(ratings) < 2:
        raise ValueError("adjudication requires independent ratings")
    if len({rating.randomized_response_id for rating in ratings}) != 1:
        raise ValueError("ratings must reference one randomized response")
    if len({rating.criterion_id for rating in ratings}) != 1:
        raise ValueError("ratings must reference one criterion")
    if len({rating.rater_pseudonym for rating in ratings}) != len(ratings):
        raise ValueError("adjudication requires distinct raters")
    if len({rating.rating_id for rating in ratings}) != len(ratings):
        raise ValueError("adjudication requires distinct rating identities")
    if len({rating.rubric_version for rating in ratings}) != 1:
        raise ValueError("adjudication requires one frozen rubric version")
    if criterion_kind not in {"ordinal", "binary"}:
        raise ValueError("unknown criterion kind")
    labels = tuple(rating.value for rating in ratings)
    disagreement = len(set(labels)) > 1
    resolved = not disagreement or rationale is not None
    if resolved and disagreement:
        if not rationale:
            raise ValueError("resolved adjudication requires written rationale")
        if adjudicated_value is None:
            raise ValueError("resolved disagreement requires an adjudicated value")
        if not adjudicator_pseudonyms:
            raise ValueError("resolved disagreement requires adjudicator identity")
        if rubric is None:
            raise ValueError("resolved disagreement requires the frozen rubric")
        criteria = {criterion.criterion_id: criterion for criterion in validate_rubric(rubric)}
        criterion = criteria.get(ratings[0].criterion_id)
        if criterion is None or criterion.kind != criterion_kind:
            raise ValueError("adjudication criterion does not match the frozen rubric")
        if adjudicated_value not in criterion.anchors:
            raise ValueError("adjudicated value is not in the frozen rubric anchors")
    elif adjudicated_value is not None or adjudicator_pseudonyms:
        raise ValueError("adjudicator details require a resolved disagreement")
    return AdjudicationRecord(
        schema_version=1,
        adjudication_id=adjudication_id,
        randomized_response_id=ratings[0].randomized_response_id,
        criterion_id=ratings[0].criterion_id,
        source_rating_ids=tuple(rating.rating_id for rating in ratings),
        labels=labels,
        resolved=resolved,
        adjudicated_value=adjudicated_value,
        adjudicator_pseudonyms=tuple(adjudicator_pseudonyms),
        rationale=rationale,
        sensitivity_flag=disagreement and not resolved,
    )


class AppendOnlyAdjudicationStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    def append(self, adjudication: AdjudicationRecord) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        destination = self.root / f"{adjudication.adjudication_id}.json"
        try:
            with destination.open("xb") as stream:
                stream.write(canonical_json_bytes(adjudication))
                stream.write(b"\n")
        except FileExistsError as exc:
            raise ValueError("append collision") from exc
        return destination

    def overwrite(self, adjudication: AdjudicationRecord) -> None:
        del adjudication
        raise ValueError("overwrite attempt")
