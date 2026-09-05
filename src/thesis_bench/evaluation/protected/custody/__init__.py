"""Protected custody records and access boundaries."""

from .access import (
    authorize_protected_access,
    load_protected_payload,
    model_facing_safe_handle,
    record_protected_event,
    safe_protected_handle,
)
from .judge_access import JudgeAccessGrant, validate_judge_access_grant
from .records import AccessDecision, ProtectedCustodyEvent, SafeProtectedHandle
from .repository import load_repository_protected_payload, repository_protected_reference

__all__ = [
    "AccessDecision",
    "JudgeAccessGrant",
    "ProtectedCustodyEvent",
    "SafeProtectedHandle",
    "authorize_protected_access",
    "load_protected_payload",
    "load_repository_protected_payload",
    "model_facing_safe_handle",
    "record_protected_event",
    "repository_protected_reference",
    "safe_protected_handle",
    "validate_judge_access_grant",
]
