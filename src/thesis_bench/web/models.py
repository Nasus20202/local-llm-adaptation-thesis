from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from pydantic import Field
from pydantic.types import StrictBool, StrictFloat, StrictInt, StrictStr

from ..records import VersionedRecord
from ..schemas import Identifier, NonBlankStr


class AllowlistEntry(VersionedRecord):
    host: Identifier
    path_prefix: StrictStr = Field(min_length=1)


class W1Policy(VersionedRecord):
    condition_id: NonBlankStr
    policy_version: Identifier
    combined_condition: StrictBool = False
    allowlist: tuple[AllowlistEntry, ...] = (
        AllowlistEntry(schema_version=1, host="kubernetes.io", path_prefix="/docs/"),
        AllowlistEntry(schema_version=1, host="github.com", path_prefix="/kubernetes/website/"),
        AllowlistEntry(schema_version=1, host="github.com", path_prefix="/kubernetes/kubernetes/"),
    )


class W1Budget(VersionedRecord):
    max_search_calls: StrictInt = 3
    max_results_per_search: StrictInt = 5
    max_fetches: StrictInt = 2
    max_tool_calls: StrictInt = 5
    max_context_tokens: StrictInt = 4000
    max_wall_seconds: StrictFloat = 120.0


_APPROVED_COMBINED_CONDITIONS: frozenset[str] = frozenset()


class SearchResult(VersionedRecord):
    result_id: Identifier
    result_rank: StrictInt = Field(default=0, ge=0)
    url: NonBlankStr
    title: NonBlankStr


class FetchResponse(VersionedRecord):
    status: StrictInt
    final_url: NonBlankStr
    redirects: tuple[NonBlankStr, ...] = ()
    body: StrictStr = ""
    provider_version: StrictStr | None = None
    token_count: StrictInt = Field(default=0, ge=0)
    duration_seconds: StrictFloat = Field(default=0.0, ge=0.0)


class FetchMetadata(VersionedRecord):
    status: StrictInt
    final_url: NonBlankStr
    redirects: tuple[NonBlankStr, ...] = ()
    provider_version: StrictStr | None = None
    token_count: StrictInt = Field(default=0, ge=0)
    duration_seconds: StrictFloat = Field(default=0.0, ge=0.0)


class PreparedFetch(VersionedRecord):
    handle_id: Identifier
    request_url: NonBlankStr
    metadata: FetchMetadata


class SearchFetchProvider(Protocol):
    def search(self, query: str) -> Sequence[SearchResult]: ...

    def prepare_fetch(self, url: str) -> PreparedFetch: ...

    def read_fetch(self, prepared: PreparedFetch) -> str: ...
