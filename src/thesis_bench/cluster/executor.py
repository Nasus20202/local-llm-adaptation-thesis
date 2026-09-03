from __future__ import annotations

from pathlib import Path

from ..records import ReasonCode, canonical_json_bytes
from .attempt import ClusterAttempt
from .models import (
    AttemptRecord,
    ClusterPolicy,
    FinalStateValidator,
    PinnedEnvironment,
    ProcessContainerAdapter,
)


class ClusterExecutor:
    def __init__(
        self,
        *,
        root: Path | None,
        environment: PinnedEnvironment,
        policy: ClusterPolicy,
        adapter: ProcessContainerAdapter,
        validator: FinalStateValidator | None,
        initial_state_hash: str,
        initial_validator_result: str,
    ) -> None:
        if environment.namespace != policy.namespace:
            raise ValueError("environment and policy namespace mismatch")
        self.root = root
        self.environment = environment
        self.policy = policy
        self.adapter = adapter
        self.validator = validator
        self.initial_state_hash = initial_state_hash
        self.initial_validator_result = initial_validator_result
        self._attempts = 0

    def start_attempt(self, family_id: str, variant_id: str) -> ClusterAttempt:
        self._attempts += 1
        reset = self.adapter.reset()
        matches = (
            reset.state_hash == self.initial_state_hash
            and reset.validator_result == self.initial_validator_result
        )
        record = AttemptRecord(
            schema_version=1,
            attempt_id=f"attempt-{self._attempts}",
            family_id=family_id,
            variant_id=variant_id,
            started=matches,
            reason_code=ReasonCode.OK if matches else ReasonCode.INFRASTRUCTURE_FAILURE,
            reset=reset,
        )
        if self.root is not None:
            attempt_directory = self._write_attempt(record)
        else:
            attempt_directory = None
        return ClusterAttempt(
            record=record,
            policy=self.policy,
            adapter=self.adapter,
            validator=self.validator,
            attempt_directory=attempt_directory,
        )

    def _write_attempt(self, record: AttemptRecord) -> Path:
        if self.root is None:
            raise RuntimeError("attempt root is required")
        self.root.mkdir(parents=True, exist_ok=True)
        destination = self.root / record.attempt_id
        try:
            destination.mkdir()
            with (destination / "record.json").open("xb") as stream:
                stream.write(canonical_json_bytes(record))
                stream.write(b"\n")
        except FileExistsError as exc:
            raise ValueError("append collision") from exc
        return destination
