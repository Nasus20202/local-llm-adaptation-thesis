from __future__ import annotations

from collections.abc import Sequence

from .models import FetchMetadata, FetchResponse, PreparedFetch, SearchResult


class FakeSearchFetchProvider:
    def __init__(
        self,
        *,
        search_results: Sequence[SearchResult] = (),
        fetch_responses: dict[str, FetchResponse] | None = None,
    ) -> None:
        self.search_results = tuple(search_results)
        self.fetch_responses = fetch_responses or {}
        self._search_calls: list[str] = []
        self._prepare_calls: list[str] = []
        self._read_calls: list[str] = []
        self._fetch_calls: list[str] = []
        self._prepared_bodies: dict[str, str] = {}
        self.provider_version = "fake-v1"

    @property
    def search_calls(self) -> tuple[str, ...]:
        return tuple(self._search_calls)

    @property
    def fetch_calls(self) -> tuple[str, ...]:
        return tuple(self._fetch_calls)

    @property
    def prepare_calls(self) -> tuple[str, ...]:
        return tuple(self._prepare_calls)

    @property
    def read_calls(self) -> tuple[str, ...]:
        return tuple(self._read_calls)

    def search(self, query: str) -> Sequence[SearchResult]:
        self._search_calls.append(query)
        return self.search_results

    def fetch(self, url: str) -> FetchResponse:
        self._fetch_calls.append(url)
        prepared = self.prepare_fetch(url)
        metadata = prepared.metadata
        return FetchResponse(
            schema_version=1,
            status=metadata.status,
            final_url=metadata.final_url,
            redirects=metadata.redirects,
            body=self.read_fetch(prepared),
            provider_version=metadata.provider_version,
            token_count=metadata.token_count,
            duration_seconds=metadata.duration_seconds,
        )

    def prepare_fetch(self, url: str) -> PreparedFetch:
        self._prepare_calls.append(url)
        response = self.fetch_responses.get(url)
        if response is None:
            metadata = FetchMetadata(
                schema_version=1,
                status=404,
                final_url=url,
                provider_version=self.provider_version,
            )
            body = ""
        else:
            metadata = FetchMetadata(
                schema_version=1,
                status=response.status,
                final_url=response.final_url,
                redirects=response.redirects,
                provider_version=response.provider_version,
                token_count=response.token_count,
                duration_seconds=response.duration_seconds,
            )
            body = response.body
        handle_id = f"prepared-{len(self._prepare_calls)}"
        self._prepared_bodies[handle_id] = body
        return PreparedFetch(
            schema_version=1,
            handle_id=handle_id,
            request_url=url,
            metadata=metadata,
        )

    def read_fetch(self, prepared: PreparedFetch) -> str:
        self._read_calls.append(prepared.request_url)
        return self._prepared_bodies[prepared.handle_id]
