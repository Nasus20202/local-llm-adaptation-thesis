from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Literal, Protocol

from pydantic import Field, model_validator
from pydantic.types import StrictBool, StrictFloat, StrictInt, StrictStr

from ..records import DecisionStatus, ReasonCode, VersionedRecord, content_sha256
from ..schemas import Identifier, NonBlankStr, Sha256


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


class PinnedEnvironment(VersionedRecord):
    kind_revision: Identifier
    node_image_digest: StrictStr = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    workload_image_digests: tuple[StrictStr, ...] = Field(min_length=1)
    cluster_config_sha256: Sha256
    host_runtime_identity: Identifier
    namespace: Identifier
    reset_policy: Identifier
    validator_version: Identifier

    @model_validator(mode="after")
    def reject_mutable_workload_images(self) -> PinnedEnvironment:
        if any(
            not image.startswith("sha256:")
            or len(image) != 71
            or any(character not in "0123456789abcdef" for character in image[7:])
            for image in self.workload_image_digests
        ):
            raise ValueError("workload images must use immutable digests")
        return self


class ClusterPolicy(VersionedRecord):
    policy_id: Identifier
    namespace: Identifier
    allowed_commands: tuple[Identifier, ...] = Field(min_length=1)
    allowed_permissions: tuple[Identifier, ...] = Field(min_length=1)
    allowed_observations: tuple[Identifier, ...] = Field(min_length=1)
    context_budget: StrictInt = Field(gt=0)
    max_actions: StrictInt = Field(gt=0)
    max_output_bytes: StrictInt = Field(gt=0)
    max_duration_seconds: StrictInt = Field(gt=0)
    allow_privileged: Literal[False]
    allow_host_mounts: Literal[False]
    allow_cluster_scope: Literal[False]
    allow_egress: Literal[False]

    @property
    def policy_hash(self) -> str:
        return content_sha256(self.model_dump(exclude={"schema_version", "policy_id"}))


class ActionRequest(VersionedRecord):
    command: Identifier
    permission: Identifier
    output: StrictStr = ""
    namespace: StrictStr | None = None
    observation: StrictStr | None = None
    privileged: StrictBool = False
    host_mount: StrictBool = False
    cluster_scope: StrictBool = False
    egress: StrictBool = False
    duration_seconds: StrictFloat = Field(default=0.0, ge=0.0)
    state_resource_id: Identifier | None = None


class ResetEvidence(VersionedRecord):
    state_hash: StrictStr
    validator_result: NonBlankStr
    duration_seconds: StrictFloat = Field(ge=0.0)

    @property
    def initial_state_hash(self) -> str:
        return self.state_hash


class ActionResponse(VersionedRecord):
    outcome: Literal["allowed", "timeout", "error"]
    output: StrictStr = ""
    duration_seconds: StrictFloat = Field(default=0.0, ge=0.0)


class ProcessContainerAdapter(Protocol):
    def reset(self) -> ResetEvidence: ...

    def execute(self, request: ActionRequest) -> ActionResponse: ...

    def validate_final_state(self) -> FinalStateObservation: ...


class AttemptRecord(VersionedRecord):
    attempt_id: Identifier
    family_id: Identifier
    variant_id: Identifier
    started: StrictBool
    reason_code: ReasonCode
    reset: ResetEvidence


class ActionCapture(VersionedRecord):
    sequence: StrictInt
    started_at: StrictStr = Field(min_length=1)
    ended_at: StrictStr = Field(min_length=1)
    requested_command: Identifier
    normalized_arguments: StrictStr = Field(min_length=1)
    normalized_permission: Identifier
    state_changing_resource_id: Identifier | None = None
    outcome: Literal["allowed", "denied", "timeout", "error"]
    reason_code: ReasonCode
    output: StrictStr
    duration_seconds: StrictFloat
    cumulative_actions: StrictInt
    cumulative_output_bytes: StrictInt
    cumulative_duration_seconds: StrictFloat


class FinalStateFixture(VersionedRecord):
    fixture_id: Identifier
    category: Literal["positive", "negative", "boundary", "malformed", "ambiguous"]
    expected: StrictBool


class FinalStateObservation(VersionedRecord):
    state_satisfies: StrictBool
    validator_result: NonBlankStr


class FinalStateValidator(VersionedRecord):
    validator_id: Identifier
    version: Identifier
    fixtures: tuple[FinalStateFixture, ...] = Field(min_length=5, max_length=5)

    def qualify(
        self,
        evaluator: Callable[[FinalStateFixture], FinalStateResult] | None = None,
        *,
        repeats: int = 2,
    ) -> DecisionStatus:
        if repeats < 2:
            return DecisionStatus.AMEND
        required = {"positive", "negative", "boundary", "malformed", "ambiguous"}
        categories = {fixture.category for fixture in self.fixtures}
        fixture_ids = [fixture.fixture_id for fixture in self.fixtures]
        if categories != required or len(set(fixture_ids)) != len(fixture_ids):
            return DecisionStatus.AMEND
        if evaluator is None:
            return DecisionStatus.AMEND
        try:
            results = tuple(
                tuple(evaluator(fixture) for _ in range(repeats)) for fixture in self.fixtures
            )
        except Exception:
            return DecisionStatus.AMEND
        for fixture, fixture_results in zip(self.fixtures, results, strict=True):
            first = fixture_results[0]
            if any(result.model_dump() != first.model_dump() for result in fixture_results[1:]):
                return DecisionStatus.AMEND
            expected = "success" if fixture.expected else "failure"
            if first.outcome != expected:
                return DecisionStatus.AMEND
        return DecisionStatus.GO

    def evaluate(
        self, *, state_satisfies: bool, prohibited_action: bool = False
    ) -> FinalStateResult:
        if prohibited_action:
            return FinalStateResult(
                schema_version=1,
                outcome="failure",
                reason_code=ReasonCode.SAFETY_FAILURE,
            )
        return FinalStateResult(
            schema_version=1,
            outcome="success" if state_satisfies else "failure",
            reason_code=ReasonCode.OK if state_satisfies else ReasonCode.EVALUATED_SYSTEM_FAILURE,
        )


class FinalStateResult(VersionedRecord):
    outcome: Literal["success", "failure"]
    reason_code: ReasonCode
