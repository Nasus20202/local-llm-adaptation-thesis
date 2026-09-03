from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from ..records import ReasonCode
from .models import _APPROVED_COMBINED_CONDITIONS, SearchFetchProvider, W1Budget, W1Policy
from .policy import _safe_error_result
from .protocols import AttemptContext
from .records import RetrievalProvenance


class _W1AttemptState:
    def __init__(
        self,
        *,
        policy: W1Policy,
        provider: SearchFetchProvider,
        budget: W1Budget | None = None,
        persist_provenance: Callable[[RetrievalProvenance], bool] | None = None,
        protected_context: bool = False,
    ) -> None:
        self.policy = policy
        self.provider = provider
        self.budget = budget or W1Budget(schema_version=1)
        self.persist_provenance = persist_provenance or (lambda _: True)
        self.protected_context = protected_context
        self.search_calls = 0
        self.fetches = 0
        self.tool_calls = 0
        self.context_tokens = 0
        self.wall_seconds = 0.0
        self.records: list[RetrievalProvenance] = []
        self._next_retrieval_id = 1

    def _persist_provenance(self, provenance: RetrievalProvenance) -> RetrievalProvenance:
        stored = provenance
        try:
            captured = self.persist_provenance(provenance)
        except Exception:
            captured = False
        if not captured:
            stored = provenance.model_copy(
                update={
                    "captured": False,
                    "reason_code": ReasonCode.INFRASTRUCTURE_FAILURE,
                }
            )
        return stored

    def _record_provenance(
        self, provenance: RetrievalProvenance, *, persist: bool = True
    ) -> RetrievalProvenance:
        stored = self._persist_provenance(provenance) if persist else provenance
        self.records.append(stored)
        return stored

    def _require_policy(
        self: AttemptContext,
        *,
        operation: Literal["search", "fetch"],
        url: str | None,
    ) -> None:
        try:
            if self.policy.condition_id != "W1" and not (
                self.policy.combined_condition
                and self.policy.condition_id in _APPROVED_COMBINED_CONDITIONS
            ):
                raise ValueError
            if self.protected_context:
                raise ValueError
        except ValueError as exc:
            _safe_error_result(
                operation=operation,
                url=url,
                query=None,
                reason_code=ReasonCode.POLICY_VIOLATION,
                attempt=self,
                error="web policy denied request",
            )
            raise ValueError("web policy denied request") from exc
