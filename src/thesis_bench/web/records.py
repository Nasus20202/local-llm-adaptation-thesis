from __future__ import annotations

from typing import Literal

from pydantic import Field
from pydantic.types import StrictBool, StrictFloat, StrictInt, StrictStr

from ..records import ReasonCode, VersionedRecord
from ..schemas import Identifier, NonBlankStr, Sha256
from .models import SearchResult


class RetrievalProvenance(VersionedRecord):
    retrieval_id: Identifier
    operation: Literal["search", "fetch"]
    query: StrictStr | None = None
    result_rank: StrictInt | None = None
    original_url: StrictStr | None = None
    final_url: StrictStr | None = None
    redirects: tuple[NonBlankStr, ...] = ()
    retrieved_at: StrictStr
    response_status: StrictInt | None = None
    provider_version: NonBlankStr
    extracted_token_count: StrictInt = Field(default=0, ge=0)
    cumulative_tool_calls: StrictInt = Field(ge=0)
    cumulative_search_calls: StrictInt = Field(ge=0)
    cumulative_fetches: StrictInt = Field(ge=0)
    cumulative_context_tokens: StrictInt = Field(ge=0)
    cumulative_wall_seconds: StrictFloat = Field(ge=0.0)
    content_sha256: Sha256 | None = None
    captured: StrictBool
    reason_code: ReasonCode
    error: StrictStr | None = None


class WebResult(VersionedRecord):
    provenance: RetrievalProvenance
    exposed_text: StrictStr | None = None
    results: tuple[SearchResult, ...] = ()
