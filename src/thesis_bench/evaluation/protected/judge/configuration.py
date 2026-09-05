from __future__ import annotations

from ....records import content_sha256
from .records import JudgeConfiguration


def configuration_digest(configuration: JudgeConfiguration) -> str:
    return content_sha256(configuration.model_dump(mode="json", exclude={"content_sha256"}))


def validate_judge_configuration(
    configuration: JudgeConfiguration, *, require_primary_eligibility: bool = False
) -> JudgeConfiguration:
    try:
        configuration = JudgeConfiguration.model_validate(configuration.model_dump(mode="python"))
    except ValueError:
        raise ValueError("judge configuration is invalid") from None
    if configuration.content_sha256 != configuration_digest(configuration):
        raise ValueError("judge configuration hash does not cover its configuration")
    if configuration.state != "frozen":
        raise ValueError("judge configuration is not frozen")
    thresholds = configuration.qualification_thresholds
    if require_primary_eligibility and not thresholds.is_frozen:
        raise ValueError("judge qualification threshold configuration is deferred")
    if require_primary_eligibility and configuration.suspension_state != "active":
        raise ValueError("judge configuration requires requalification")
    return configuration


def validate_judge_successor(
    prior: JudgeConfiguration, successor: JudgeConfiguration
) -> JudgeConfiguration:
    prior = validate_judge_configuration(prior)
    try:
        successor = JudgeConfiguration.model_validate(successor.model_dump(mode="python"))
    except ValueError:
        raise ValueError("judge successor configuration is invalid") from None
    if successor.judge_config_id == prior.judge_config_id:
        raise ValueError("judge successor must have a new identity")
    if successor.supersedes_judge_config_id != prior.judge_config_id:
        raise ValueError("judge successor must identify its predecessor")
    if successor.content_sha256 == prior.content_sha256:
        raise ValueError("judge successor must have a new configuration hash")
    if (
        successor.state == "superseded"
        or successor.content_sha256 is None
        or successor.content_sha256 != configuration_digest(successor)
    ):
        raise ValueError("judge successor configuration is invalid")
    return successor


__all__ = [
    "configuration_digest",
    "validate_judge_configuration",
    "validate_judge_successor",
]
