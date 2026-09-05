"""Protected custody records and access boundaries."""

from .access import (
    authorize_protected_access,
    load_protected_payload,
    model_facing_safe_handle,
    record_protected_event,
    safe_protected_handle,
)
from .records import AccessDecision, ProtectedCustodyEvent, SafeProtectedHandle

__all__ = [
    "AccessDecision",
    "ProtectedCustodyEvent",
    "SafeProtectedHandle",
    "authorize_protected_access",
    "load_protected_payload",
    "model_facing_safe_handle",
    "record_protected_event",
    "safe_protected_handle",
]
