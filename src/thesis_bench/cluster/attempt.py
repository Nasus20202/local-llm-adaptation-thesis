from __future__ import annotations

from pathlib import Path
from typing import Literal

from ..records import ReasonCode, canonical_json_bytes
from .models import (
    ActionCapture,
    ActionRequest,
    AttemptRecord,
    ClusterPolicy,
    FinalStateResult,
    FinalStateValidator,
    ProcessContainerAdapter,
    ResetEvidence,
    _utc_now,
)


class ClusterAttempt:
    def __init__(
        self,
        *,
        record: AttemptRecord,
        policy: ClusterPolicy,
        adapter: ProcessContainerAdapter,
        validator: FinalStateValidator | None,
        attempt_directory: Path | None = None,
    ) -> None:
        self.record = record
        self.policy = policy
        self.adapter = adapter
        self.validator = validator
        self.attempt_directory = attempt_directory
        self.captures: list[ActionCapture] = []
        self._output_bytes = 0
        self._duration_seconds = 0.0
        self._terminal = False
        self._terminal_reason: ReasonCode | None = None

    @property
    def started(self) -> bool:
        return self.record.started

    @property
    def reset(self) -> ResetEvidence:
        return self.record.reset

    @property
    def reason_code(self) -> ReasonCode:
        return self.record.reason_code

    @property
    def terminal_reason(self) -> ReasonCode | None:
        return self._terminal_reason

    @property
    def terminal_outcome(self) -> Literal["failure"] | None:
        return "failure" if self._terminal_reason is not None else None

    def _capture(
        self,
        request: ActionRequest,
        outcome: Literal["allowed", "denied", "timeout", "error"],
        reason: ReasonCode,
        *,
        output: str = "",
        duration: float = 0.0,
    ) -> ActionCapture:
        capture = ActionCapture(
            schema_version=1,
            sequence=len(self.captures),
            started_at=_utc_now(),
            ended_at=_utc_now(),
            requested_command=request.command,
            normalized_arguments=canonical_json_bytes(
                request.model_dump(exclude={"schema_version"}, mode="json")
            ).decode("utf-8"),
            normalized_permission=request.permission,
            state_changing_resource_id=request.state_resource_id,
            outcome=outcome,
            reason_code=reason,
            output=output[: self.policy.max_output_bytes],
            duration_seconds=duration,
            cumulative_actions=len(self.captures) + 1,
            cumulative_output_bytes=self._output_bytes
            + len(output[: self.policy.max_output_bytes].encode()),
            cumulative_duration_seconds=self._duration_seconds + duration,
        )
        self._output_bytes = capture.cumulative_output_bytes
        self._duration_seconds = capture.cumulative_duration_seconds
        self.captures.append(capture)
        if self.attempt_directory is not None:
            with (self.attempt_directory / "actions.jsonl").open("ab") as stream:
                stream.write(canonical_json_bytes(capture))
                stream.write(b"\n")
        return capture

    def _terminate(self, reason: ReasonCode) -> None:
        self._terminal = True
        self._terminal_reason = reason

    def action(self, request: ActionRequest) -> ActionCapture:
        if not self.started:
            raise ValueError("attempt did not pass reset verification")
        if self._terminal:
            raise ValueError("attempt has terminated")
        if len(self.captures) >= self.policy.max_actions:
            capture = self._capture(request, "denied", ReasonCode.BUDGET_EXHAUSTED)
            self._terminate(ReasonCode.BUDGET_EXHAUSTED)
            return capture
        namespace = request.namespace or self.policy.namespace
        if namespace != self.policy.namespace:
            return self._capture(request, "denied", ReasonCode.DENIED_OPERATION)
        if request.command not in self.policy.allowed_commands:
            return self._capture(request, "denied", ReasonCode.DENIED_OPERATION)
        if request.permission not in self.policy.allowed_permissions:
            return self._capture(request, "denied", ReasonCode.PERMISSION_FAILURE)
        if (
            request.observation is not None
            and request.observation not in self.policy.allowed_observations
        ):
            return self._capture(request, "denied", ReasonCode.DENIED_OPERATION)
        if request.privileged or request.host_mount or request.cluster_scope or request.egress:
            return self._capture(request, "denied", ReasonCode.SAFETY_FAILURE)
        if len(request.output.encode()) > self.policy.max_output_bytes:
            capture = self._capture(request, "denied", ReasonCode.BUDGET_EXHAUSTED)
            self._terminate(ReasonCode.BUDGET_EXHAUSTED)
            return capture
        if self._output_bytes + len(request.output.encode()) > self.policy.max_output_bytes:
            capture = self._capture(request, "denied", ReasonCode.BUDGET_EXHAUSTED)
            self._terminate(ReasonCode.BUDGET_EXHAUSTED)
            return capture
        if self._duration_seconds + request.duration_seconds > self.policy.max_duration_seconds:
            capture = self._capture(request, "denied", ReasonCode.BUDGET_EXHAUSTED)
            self._terminate(ReasonCode.BUDGET_EXHAUSTED)
            return capture
        response = self.adapter.execute(request)
        if len(response.output.encode()) > self.policy.max_output_bytes:
            capture = self._capture(
                request,
                "denied",
                ReasonCode.BUDGET_EXHAUSTED,
                duration=response.duration_seconds,
            )
            self._terminate(ReasonCode.BUDGET_EXHAUSTED)
            return capture
        if self._output_bytes + len(response.output.encode()) > self.policy.max_output_bytes:
            capture = self._capture(
                request,
                "denied",
                ReasonCode.BUDGET_EXHAUSTED,
                duration=response.duration_seconds,
            )
            self._terminate(ReasonCode.BUDGET_EXHAUSTED)
            return capture
        if self._duration_seconds + response.duration_seconds > self.policy.max_duration_seconds:
            capture = self._capture(
                request,
                "timeout",
                ReasonCode.TIMEOUT,
                output=response.output,
                duration=response.duration_seconds,
            )
            self._terminate(ReasonCode.TIMEOUT)
            return capture
        if response.outcome == "timeout":
            capture = self._capture(
                request,
                "timeout",
                ReasonCode.TIMEOUT,
                output=response.output,
                duration=response.duration_seconds,
            )
            self._terminate(ReasonCode.TIMEOUT)
            return capture
        if response.outcome == "error":
            return self._capture(
                request,
                "error",
                ReasonCode.EVALUATED_SYSTEM_FAILURE,
                output=response.output,
                duration=response.duration_seconds,
            )
        return self._capture(
            request,
            "allowed",
            ReasonCode.OK,
            output=response.output,
            duration=response.duration_seconds,
        )

    def final_state(self) -> FinalStateResult:
        if self.validator is None:
            raise ValueError("final-state validator is required")
        prohibited = any(c.reason_code == ReasonCode.SAFETY_FAILURE for c in self.captures)
        evidence = self.adapter.validate_final_state()
        if self.attempt_directory is not None:
            destination = self.attempt_directory / "final-state.json"
            try:
                with destination.open("xb") as stream:
                    stream.write(canonical_json_bytes(evidence))
                    stream.write(b"\n")
            except FileExistsError as exc:
                raise ValueError("append collision") from exc
        result = self.validator.evaluate(
            state_satisfies=evidence.state_satisfies, prohibited_action=prohibited
        )
        if self._terminal_reason in {
            ReasonCode.BUDGET_EXHAUSTED,
            ReasonCode.TIMEOUT,
            ReasonCode.EVALUATED_SYSTEM_TIMEOUT,
        }:
            return FinalStateResult(
                schema_version=1,
                outcome="failure",
                reason_code=self._terminal_reason,
            )
        return result
