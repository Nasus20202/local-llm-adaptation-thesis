from __future__ import annotations

import pytest

from thesis_bench.evaluation.protected import validate_judge_successor

from .judge_fixtures import judge_configuration, rehash_judge_configuration


def test_judge_configuration_successor_requires_new_identity_and_hash() -> None:
    prior = judge_configuration()
    successor = rehash_judge_configuration(
        prior,
        judge_config_id="judge-config-2",
        revision="requalification_required",
        supersedes_judge_config_id=prior.judge_config_id,
    )
    assert validate_judge_successor(prior, successor) == successor
    with pytest.raises(ValueError):
        validate_judge_successor(prior, rehash_judge_configuration(prior, revision="new"))
