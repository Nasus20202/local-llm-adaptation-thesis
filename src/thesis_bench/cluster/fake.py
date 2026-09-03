from __future__ import annotations

from .models import ActionRequest, ActionResponse, FinalStateObservation, ResetEvidence


class FakeCluster:
    def __init__(
        self,
        *,
        initial_state_hash: str,
        validator_result: str,
        responses: dict[str, ActionResponse] | None = None,
        final_state_satisfies: bool = True,
        final_state_validator_result: str = "final-state-ok",
    ) -> None:
        self.initial_state_hash = initial_state_hash
        self.validator_result = validator_result
        self.responses = responses or {}
        self.final_state_satisfies = final_state_satisfies
        self.final_state_validator_result = final_state_validator_result
        self._actions: list[ActionRequest] = []

    @property
    def actions(self) -> tuple[ActionRequest, ...]:
        return tuple(self._actions)

    def reset(self) -> ResetEvidence:
        return ResetEvidence(
            schema_version=1,
            state_hash=self.initial_state_hash,
            validator_result=self.validator_result,
            duration_seconds=0.0,
        )

    def execute(self, request: ActionRequest) -> ActionResponse:
        self._actions.append(request)
        return self.responses.get(
            request.command,
            ActionResponse(schema_version=1, outcome="allowed", output=request.output),
        )

    def validate_final_state(self) -> FinalStateObservation:
        return FinalStateObservation(
            schema_version=1,
            state_satisfies=self.final_state_satisfies,
            validator_result=self.final_state_validator_result,
        )
