from __future__ import annotations

from time import perf_counter

from ..records import ReasonCode
from .models import FetchResponse
from .policy import _denied_url, _safe_error_result
from .protocols import AttemptContext
from .records import WebResult


def _count_extracted_tokens(body: str) -> int:
    return len(body.split())


class _FetchOperationsMixin:
    def fetch(self: AttemptContext, url: str) -> WebResult:
        if (
            self.fetches >= self.budget.max_fetches
            or self.tool_calls >= self.budget.max_tool_calls
            or self.wall_seconds >= self.budget.max_wall_seconds
        ):
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="fetch budget exhausted",
            )
        self._require_policy(operation="fetch", url=url)
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
        preparation_started = perf_counter()
        try:
            prepared = self.provider.prepare_fetch(url)
        except Exception:
            self.wall_seconds += max(0.0, perf_counter() - preparation_started)
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.PROVIDER_UNAVAILABLE,
                attempt=self,
                error="fetch provider unavailable",
            )
        metadata = prepared.metadata
        preparation_duration = max(
            metadata.duration_seconds, max(0.0, perf_counter() - preparation_started)
        )
        self.wall_seconds += preparation_duration
        metadata_response = FetchResponse(
            schema_version=1,
            status=metadata.status,
            final_url=metadata.final_url,
            redirects=metadata.redirects,
            provider_version=metadata.provider_version,
            token_count=0,
            duration_seconds=preparation_duration,
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
        read_started = perf_counter()
        try:
            body = self.provider.read_fetch(prepared)
        except Exception:
            read_duration = max(0.0, perf_counter() - read_started)
            self.wall_seconds += read_duration
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.PROVIDER_UNAVAILABLE,
                attempt=self,
                error="fetch body provider unavailable",
                response=metadata_response.model_copy(
                    update={"duration_seconds": preparation_duration + read_duration}
                ),
            )
        read_duration = max(0.0, perf_counter() - read_started)
        self.wall_seconds += read_duration
        if not isinstance(body, str):
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.PROVIDER_UNAVAILABLE,
                attempt=self,
                error="fetch body was not text",
                response=metadata_response.model_copy(
                    update={"duration_seconds": preparation_duration + read_duration}
                ),
            )
        extracted_tokens = _count_extracted_tokens(body)
        self.context_tokens += extracted_tokens
        response = metadata_response.model_copy(
            update={
                "body": body,
                "token_count": extracted_tokens,
                "duration_seconds": preparation_duration + read_duration,
            }
        )
        if self.context_tokens > self.budget.max_context_tokens:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="context token budget exhausted",
                response=response,
            )
        if self.wall_seconds > self.budget.max_wall_seconds:
            return _safe_error_result(
                operation="fetch",
                url=url,
                query=None,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="tool wall-time budget exhausted",
                response=response,
            )
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
