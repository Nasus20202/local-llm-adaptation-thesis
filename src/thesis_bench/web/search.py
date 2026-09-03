from __future__ import annotations

from time import perf_counter

from ..records import ReasonCode, content_sha256
from .policy import _denied_url, _redact_provenance, _safe_error_result
from .protocols import AttemptContext
from .records import WebResult


class _SearchOperationsMixin:
    def search(self: AttemptContext, query: str) -> WebResult:
        if (
            self.search_calls >= self.budget.max_search_calls
            or self.tool_calls >= self.budget.max_tool_calls
            or self.wall_seconds >= self.budget.max_wall_seconds
        ):
            _safe_error_result(
                operation="search",
                url=None,
                query=query,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="search budget exhausted",
            )
            raise ValueError("web budget exhausted")
        self._require_policy(operation="search", url=None)
        lowered = query.lower()
        if any(
            marker in lowered
            for marker in ("benchmark", "golden", "nasus20202/local-llm-adaptation-thesis")
        ):
            return _safe_error_result(
                operation="search",
                url=None,
                query=None,
                reason_code=ReasonCode.POLICY_VIOLATION,
                attempt=self,
                error="query denied by web policy",
            )
        self.search_calls += 1
        self.tool_calls += 1
        provider_version = getattr(self.provider, "provider_version", None)
        started = perf_counter()
        try:
            results = tuple(
                result.model_copy(update={"result_rank": rank})
                for rank, result in enumerate(self.provider.search(query))
            )
        except Exception:
            self.wall_seconds += max(0.0, perf_counter() - started)
            return _safe_error_result(
                operation="search",
                url=None,
                query=query,
                reason_code=ReasonCode.PROVIDER_UNAVAILABLE,
                attempt=self,
                error="search provider unavailable",
                provider_version=provider_version,
            )
        self.wall_seconds += max(0.0, perf_counter() - started)
        if self.wall_seconds > self.budget.max_wall_seconds:
            _safe_error_result(
                operation="search",
                url=None,
                query=query,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="web wall-time budget exhausted",
                provider_version=provider_version,
            )
            raise ValueError("web wall-time budget exhausted")
        if len(results) > self.budget.max_results_per_search:
            _safe_error_result(
                operation="search",
                url=None,
                query=query,
                reason_code=ReasonCode.BUDGET_EXHAUSTED,
                attempt=self,
                error="search result budget exhausted",
            )
            raise ValueError("web result budget exhausted")
        if any(
            _denied_url(result.url, self.policy.allowlist)
            or any(
                marker in f"{result.url.lower()} {result.title.lower()}"
                for marker in ("benchmark", "golden", "final-test", "evaluator")
            )
            for result in results
        ):
            _safe_error_result(
                operation="search",
                url=None,
                query=query,
                reason_code=ReasonCode.POLICY_VIOLATION,
                attempt=self,
                error="search result denied by web policy",
            )
            call_provenance = self.records[-1]
            visible = _redact_provenance(call_provenance)
            for result in results:
                result_provenance = call_provenance.model_copy(
                    update={
                        "retrieval_id": f"retrieval-{self._next_retrieval_id}",
                        "result_rank": result.result_rank,
                        "original_url": result.url,
                        "final_url": result.url,
                        "content_sha256": content_sha256(result.model_dump(mode="json")),
                    }
                )
                self._next_retrieval_id += 1
                stored_result = self._record_provenance(result_provenance)
                visible = _redact_provenance(stored_result)
            return WebResult(schema_version=1, provenance=visible)
        provenance_result = _safe_error_result(
            operation="search",
            url=None,
            query=query,
            reason_code=ReasonCode.OK,
            attempt=self,
            response=None,
            provider_version=provider_version,
            persist=False,
        )
        provenance = provenance_result.provenance.model_copy(
            update={
                "content_sha256": content_sha256(
                    [result.model_dump(mode="json") for result in results]
                )
            }
        )
        call_provenance = self._persist_provenance(provenance)
        self.records[-1] = call_provenance
        if not call_provenance.captured:
            return WebResult(schema_version=1, provenance=call_provenance)
        for result in results:
            result_provenance = call_provenance.model_copy(
                update={
                    "retrieval_id": f"retrieval-{self._next_retrieval_id}",
                    "result_rank": result.result_rank,
                    "original_url": result.url,
                    "final_url": result.url,
                    "content_sha256": content_sha256(result.model_dump(mode="json")),
                }
            )
            self._next_retrieval_id += 1
            stored_result = self._record_provenance(result_provenance)
            if not stored_result.captured:
                return WebResult(schema_version=1, provenance=stored_result)
        return WebResult(schema_version=1, provenance=call_provenance, results=results)
