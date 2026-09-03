from __future__ import annotations

from ..records import ReasonCode
from .models import FetchResponse
from .policy import _denied_url, _safe_error_result
from .protocols import AttemptContext
from .records import WebResult


class _FetchOperationsMixin:
    def fetch(self: AttemptContext, url: str) -> WebResult:
        self._require_policy(operation="fetch", url=url)
        if self.fetches >= self.budget.max_fetches or self.tool_calls >= self.budget.max_tool_calls:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="fetch budget exhausted",
            )
        if _denied_url(url, self.policy.allowlist):
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.POLICY_VIOLATION,
                attempt=self,
                error="URL denied by web policy",
            )
        self.fetches += 1
        self.tool_calls += 1
        try:
            prepared = self.provider.prepare_fetch(url)
        except Exception:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.PROVIDER_UNAVAILABLE,
                attempt=self,
                error="fetch provider unavailable",
            )
        metadata = prepared.metadata
        self.wall_seconds += metadata.duration_seconds
        self.context_tokens += metadata.token_count
        metadata_response = FetchResponse(
            schema_version=1,
            status=metadata.status,
            final_url=metadata.final_url,
            redirects=metadata.redirects,
            provider_version=metadata.provider_version,
            token_count=metadata.token_count,
            duration_seconds=metadata.duration_seconds,
        )
        safe_redirects = not any(
            _denied_url(target, self.policy.allowlist) for target in metadata.redirects
        )
        safe_final = not _denied_url(metadata.final_url, self.policy.allowlist)
        if not safe_redirects or not safe_final:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.POLICY_VIOLATION,
                attempt=self,
                error="redirect denied by web policy",
                response=metadata_response,
            )
        if not 200 <= metadata.status < 300:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.PROVIDER_UNAVAILABLE,
                attempt=self,
                error="fetch provider returned an unsuccessful response",
                response=metadata_response,
            )
        if self.context_tokens > self.budget.max_context_tokens:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="context token budget exhausted",
                response=metadata_response,
            )
        if self.wall_seconds > self.budget.max_wall_seconds:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="tool wall-time budget exhausted",
                response=metadata_response,
            )
        try:
            body = self.provider.read_fetch(prepared)
        except Exception:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.PROVIDER_UNAVAILABLE,
                attempt=self,
                error="fetch body provider unavailable",
                response=metadata_response,
            )
        if not isinstance(body, str):
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.PROVIDER_UNAVAILABLE,
                attempt=self,
                error="fetch body was not text",
                response=metadata_response,
            )
        response = metadata_response.model_copy(update={"body": body})
        result = _safe_error_result(
            operation="fetch",
            url=url,
            query=None,
            reason_code=ReasonCode.OK,
            attempt=self,
            response=response,
        )
        provenance = result.provenance
        if not provenance.captured:
            return result
        return WebResult(schema_version=1, provenance=provenance, exposed_text=response.body)
