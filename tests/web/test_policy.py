from __future__ import annotations

import pytest

from tests.web.fixtures import provider
from thesis_bench.records import ReasonCode
from thesis_bench.web import (
    FakeSearchFetchProvider,
    FetchResponse,
    SearchResult,
    W1Attempt,
    W1Policy,
)


def test_w1_fetches_only_allowlisted_official_sources_and_captures_before_exposure() -> None:
    fake = provider()
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id="W1", policy_version="w1-v1"),
        provider=fake,
    )

    search = attempt.search("synthetic query")
    fetched = attempt.fetch(search.results[0].url)

    assert search.results[0].result_rank == 0
    assert fake.read_calls == (search.results[0].url,)
    search_records = [record for record in attempt.records if record.operation == "search"]
    assert search_records[-1].result_rank == 0
    assert search_records[-1].original_url == search.results[0].url
    assert fetched.exposed_text == "synthetic-official-source-body"
    assert fetched.provenance.captured is True
    assert fetched.provenance.content_sha256
    assert fetched.provenance.provider_version == "fake-v1"


@pytest.mark.parametrize("condition", ["R1", "H1", "B0"])
def test_implicit_web_access_is_denied_for_non_w1_conditions(condition: str) -> None:
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id=condition, policy_version="w1-v1"),
        provider=provider(),
    )

    with pytest.raises(ValueError, match="web policy"):
        attempt.search("synthetic query")
    assert attempt.records[-1].reason_code == ReasonCode.POLICY_VIOLATION


@pytest.mark.parametrize("condition", ["C99", "C1", "C2"])
def test_combined_web_access_requires_an_approved_condition_id(condition: str) -> None:
    attempt = W1Attempt(
        policy=W1Policy(
            schema_version=1,
            condition_id=condition,
            combined_condition=True,
            policy_version="w1-v1",
        ),
        provider=provider(),
    )

    with pytest.raises(ValueError, match="web policy"):
        attempt.search("synthetic query")


def test_redirects_and_protected_local_or_private_targets_fail_before_body_read() -> None:
    original = "https://kubernetes.io/docs/synthetic-page"
    fake = provider(url=original)
    fake.fetch_responses[original] = FetchResponse(
        schema_version=1,
        status=302,
        final_url="https://127.0.0.1/private",
        redirects=("https://127.0.0.1/private",),
        body="synthetic-protected-body",
        provider_version="fake-v1",
        token_count=3,
        duration_seconds=0.0,
    )
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id="W1", policy_version="w1-v1"), provider=fake
    )

    result = attempt.fetch(original)

    assert result.exposed_text is None
    assert result.provenance.reason_code == ReasonCode.POLICY_VIOLATION
    assert "synthetic-protected-body" not in result.provenance.model_dump_json()
    assert attempt.records[-1].final_url == "https://127.0.0.1/private"
    assert attempt.records[-1].redirects == ("https://127.0.0.1/private",)
    assert fake.prepare_calls == (original,)
    assert fake.read_calls == ()

    for forbidden in (
        "file:///tmp/private",
        "http://localhost/private",
        "http://192.168.1.10/private",
        "https://kubernetes.io/docs/../private",
        "https://kubernetes.io/docs/%2e%2e/private",
        "https://kubernetes.io/docs/%252e%252e/private",
        "https://kubernetes.io/docs/%255c..%255cprivate",
        "https://github.com/Nasus20202/local-llm-adaptation-thesis/blob/main/secret",
    ):
        denied = attempt.fetch(forbidden)
        assert denied.exposed_text is None
        assert denied.provenance.reason_code == ReasonCode.POLICY_VIOLATION


def test_denied_redirect_provenance_is_persisted_before_result_return() -> None:
    original = "https://kubernetes.io/docs/synthetic-page"
    fake = provider(url=original)
    fake.fetch_responses[original] = FetchResponse(
        schema_version=1,
        status=302,
        final_url="https://example.invalid/private",
        redirects=("https://example.invalid/private",),
        body="synthetic-protected-body",
        provider_version="fake-v1",
    )
    persisted = []
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id="W1", policy_version="w1-v1"),
        provider=fake,
        persist_provenance=lambda record: persisted.append(record) or True,
    )

    result = attempt.fetch(original)

    assert result.provenance.reason_code == ReasonCode.POLICY_VIOLATION
    assert len(persisted) == 1
    assert persisted[0].captured is True


def test_search_denies_non_allowlisted_results_without_echoing_protected_query() -> None:
    protected_query = "golden synthetic-protected-value"
    fake = FakeSearchFetchProvider(
        search_results=(
            SearchResult(
                schema_version=1,
                result_id="result-1",
                url="https://example.invalid/private",
                title="synthetic",
            ),
        )
    )
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id="W1", policy_version="w1-v1"),
        provider=fake,
    )

    result = attempt.search("ordinary synthetic query")

    assert result.results == ()
    assert result.provenance.reason_code == ReasonCode.POLICY_VIOLATION
    assert result.provenance.captured is True
    denied_result_records = [
        record
        for record in attempt.records
        if record.operation == "search" and record.original_url is not None
    ]
    assert denied_result_records[0].result_rank == 0
    assert denied_result_records[0].original_url == "https://example.invalid/private"

    denied_query = attempt.search(protected_query)
    encoded = denied_query.model_dump_json()
    assert denied_query.provenance.reason_code == ReasonCode.POLICY_VIOLATION
    assert protected_query not in encoded
    assert fake.search_calls == ("ordinary synthetic query",)
