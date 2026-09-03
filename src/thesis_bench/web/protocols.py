from __future__ import annotations

from collections.abc import Callable
from typing import Literal, Protocol

from .models import SearchFetchProvider, W1Budget, W1Policy
from .records import RetrievalProvenance


class AttemptContext(Protocol):
    policy: W1Policy
    provider: SearchFetchProvider
    budget: W1Budget
    protected_context: bool
    search_calls: int
    fetches: int
    tool_calls: int
    context_tokens: int
    wall_seconds: float
    records: list[RetrievalProvenance]
    persist_provenance: Callable[[RetrievalProvenance], bool]
    _next_retrieval_id: int

    def _persist_provenance(self, provenance: RetrievalProvenance) -> RetrievalProvenance: ...

    def _record_provenance(
        self, provenance: RetrievalProvenance, *, persist: bool = True
    ) -> RetrievalProvenance: ...

    def _require_policy(
        self, *, operation: Literal["search", "fetch"], url: str | None
    ) -> None: ...
