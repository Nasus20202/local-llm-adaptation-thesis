from __future__ import annotations

from tests.web.fixtures import provider
from thesis_bench.records import ReasonCode
from thesis_bench.web import (
    FetchMetadata,
    FetchResponse,
    PreparedFetch,
    W1Attempt,
    W1Policy,
)


def test_fetch_preparation_contains_no_body_channel() -> None:
    fake = provider()

    prepared = fake.prepare_fetch("https://kubernetes.io/docs/synthetic-page")

    assert isinstance(prepared.metadata, FetchMetadata)
    assert not hasattr(prepared, "body")


def test_prepared_fetch_handle_freezes_the_body_source() -> None:
    url = "https://kubernetes.io/docs/synthetic-page"
    fake = provider(url=url)

    prepared = fake.prepare_fetch(url)
    fake.fetch_responses[url] = fake.fetch_responses[url].model_copy(
        update={"body": "synthetic-mutated-body"}
    )

    assert isinstance(prepared, PreparedFetch)
    assert fake.read_fetch(prepared) == "synthetic-official-source-body"


def test_missing_search_capture_prevents_result_exposure() -> None:
    fake = provider()
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id="W1", policy_version="w1-v1"),
        provider=fake,
        persist_provenance=lambda _: False,
    )

    result = attempt.search("ordinary synthetic query")

    assert result.results == ()
    assert result.provenance.captured is False
    assert result.provenance.reason_code == ReasonCode.INFRASTRUCTURE_FAILURE


def test_missing_capture_prevents_context_exposure_and_unknown_provider_version_is_explicit() -> (
    None
):
    url = "https://kubernetes.io/docs/synthetic-page"
    fake = provider(url=url)
    fake.fetch_responses[url] = fake.fetch_responses[url].model_copy(
        update={"provider_version": None}
    )
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id="W1", policy_version="w1-v1"),
        provider=fake,
        persist_provenance=lambda _: False,
    )

    result = attempt.fetch(url)

    assert result.exposed_text is None
    assert result.provenance.captured is False
    assert result.provenance.provider_version == "not_exposed"
    assert result.provenance.reason_code == ReasonCode.INFRASTRUCTURE_FAILURE
    assert attempt.records[-1].captured is False


def test_provider_error_response_is_captured_without_exposing_error_body() -> None:
    url = "https://kubernetes.io/docs/synthetic-error"
    fake = provider(url=url)
    fake.fetch_responses[url] = FetchResponse(
        schema_version=1,
        status=503,
        final_url=url,
        body="synthetic-provider-error-body",
        provider_version="fake-v1",
    )
    attempt = W1Attempt(
        policy=W1Policy(schema_version=1, condition_id="W1", policy_version="w1-v1"),
        provider=fake,
    )

    result = attempt.fetch(url)

    assert result.exposed_text is None
    assert result.provenance.reason_code == ReasonCode.PROVIDER_UNAVAILABLE
    assert "synthetic-provider-error-body" not in result.model_dump_json()
