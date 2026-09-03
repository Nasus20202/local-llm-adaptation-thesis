from __future__ import annotations

from thesis_bench.web import (
    FakeSearchFetchProvider,
    FetchResponse,
    SearchResult,
)


def provider(*, url: str = "https://kubernetes.io/docs/synthetic-page") -> FakeSearchFetchProvider:
    return FakeSearchFetchProvider(
        search_results=(
            SearchResult(schema_version=1, result_id="result-1", url=url, title="synthetic"),
        ),
        fetch_responses={
            url: FetchResponse(
                schema_version=1,
                status=200,
                final_url=url,
                redirects=(),
                body="synthetic-official-source-body",
                provider_version="fake-v1",
                token_count=3,
                duration_seconds=0.0,
            )
        },
    )
