from __future__ import annotations

from typing import Literal

from pydantic.types import StrictStr

from ..records import VersionedRecord, content_sha256
from ..schemas import Identifier, Sha256


class ArtifactIdentity(VersionedRecord):
    kind: StrictStr = "evaluation-artifact"
    identity_id: Identifier
    revision: Identifier
    content_sha256: Sha256


class EvaluatorIdentity(ArtifactIdentity):
    kind: Literal["evaluator"] = "evaluator"


class FixtureSetIdentity(ArtifactIdentity):
    kind: Literal["fixture-set"] = "fixture-set"


class InputIdentity(ArtifactIdentity):
    kind: Literal["evaluation-input"] = "evaluation-input"


class OutputIdentity(ArtifactIdentity):
    kind: Literal["evaluation-output"] = "evaluation-output"


class EvaluationRecord(VersionedRecord):
    evaluation_id: Identifier
    evaluator_identity: EvaluatorIdentity
    fixture_set_identity: FixtureSetIdentity
    input_identity: InputIdentity
    output_identity: OutputIdentity
    output_sha256: Sha256
    derived_from: Identifier | None = None


def build_evaluation_record(
    evaluator_identity: EvaluatorIdentity,
    fixture_set_identity: FixtureSetIdentity,
    input_identity: InputIdentity,
    output_identity: OutputIdentity,
    *,
    derived_from: str | None = None,
) -> EvaluationRecord:
    source = {
        "evaluator": evaluator_identity.model_dump(mode="json"),
        "fixtures": fixture_set_identity.model_dump(mode="json"),
        "input": input_identity.model_dump(mode="json"),
        "output": output_identity.model_dump(mode="json"),
    }
    return EvaluationRecord(
        schema_version=1,
        evaluation_id=f"evaluation-{content_sha256(source)[:24]}",
        evaluator_identity=evaluator_identity,
        fixture_set_identity=fixture_set_identity,
        input_identity=input_identity,
        output_identity=output_identity,
        output_sha256=output_identity.content_sha256,
        derived_from=derived_from,
    )
