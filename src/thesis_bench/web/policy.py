from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

from ..records import ReasonCode

if TYPE_CHECKING:
    from .protocols import AttemptContext
import hashlib
import ipaddress
from urllib.parse import unquote, urlparse

from .models import AllowlistEntry, FetchResponse
from .records import RetrievalProvenance, WebResult


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _denied_url(url: str, allowlist: Sequence[AllowlistEntry]) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return True
    if parsed.username is not None or parsed.password is not None:
        return True
    host = parsed.hostname.lower().rstrip(".")
    if host in {"localhost", "ip6-localhost"} or host.endswith(".local"):
        return True
    if not any(character.isalpha() for character in host):
        return True
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_unspecified
    ):
        return True
    decoded_path = unquote(parsed.path)
    if any(part in {".", ".."} for part in decoded_path.split("/")):
        return True
    lowered_path = decoded_path.lower()
    if "nasus20202/local-llm-adaptation-thesis" in f"{host}{lowered_path}":
        return True
    if any(marker in lowered_path for marker in ("benchmark", "golden", "final-test", "evaluator")):
        return True
    return not any(
        host == entry.host and decoded_path.startswith(entry.path_prefix) for entry in allowlist
    )


def _safe_error_result(
    *,
    operation: Literal["search", "fetch"],
    url: str | None,
    query: str | None,
    reason_code: ReasonCode,
    attempt: AttemptContext,
    error: str | None = None,
    response: FetchResponse | None = None,
    captured: bool = True,
    provider_version: str | None = None,
    persist: bool = True,
) -> WebResult:
    redact_targets = reason_code == ReasonCode.POLICY_VIOLATION
    body_hash = (
        None
        if response is None or not response.body
        else hashlib.sha256(response.body.encode()).hexdigest()
    )
    provenance = RetrievalProvenance(
        schema_version=1,
        retrieval_id=f"retrieval-{attempt._next_retrieval_id}",
        operation=operation,
        query=query,
        original_url=url,
        final_url=response.final_url if response is not None else url,
        redirects=response.redirects if response is not None else (),
        retrieved_at=_utc_now(),
        response_status=response.status if response is not None else None,
        provider_version=(provider_version or response.provider_version or "not_exposed")
        if response is not None
        else (provider_version or "not_exposed"),
        extracted_token_count=response.token_count if response is not None else 0,
        cumulative_tool_calls=attempt.tool_calls,
        cumulative_search_calls=attempt.search_calls,
        cumulative_fetches=attempt.fetches,
        cumulative_context_tokens=attempt.context_tokens,
        cumulative_wall_seconds=attempt.wall_seconds,
        content_sha256=body_hash,
        captured=captured,
        reason_code=reason_code,
        error=error,
    )
    attempt._next_retrieval_id += 1
    stored = attempt._record_provenance(provenance, persist=persist)
    visible = _redact_provenance(stored) if redact_targets else stored
    return WebResult(schema_version=1, provenance=visible)


def _redact_provenance(provenance: RetrievalProvenance) -> RetrievalProvenance:
    return provenance.model_copy(
        update={
            "query": None,
            "original_url": None,
            "final_url": None,
            "redirects": (),
        }
    )
