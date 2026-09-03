from __future__ import annotations

from typing import Literal

from ..records import ReasonCode, VersionedRecord
from ..schemas import NonBlankStr


class ProviderEntryPointRecord(VersionedRecord):
    status: Literal["not_exposed"]
    reason_code: ReasonCode
    message: NonBlankStr


def provider_qualification_help(*, opt_in: bool = False) -> ProviderEntryPointRecord:
    del opt_in
    return ProviderEntryPointRecord(
        schema_version=1,
        status="not_exposed",
        reason_code=ReasonCode.POLICY_VIOLATION,
        message=(
            "external provider qualification is opt-in and currently exposes prerequisites only"
        ),
    )
