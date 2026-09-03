from __future__ import annotations

from typing import Literal

from ..records import ReasonCode, VersionedRecord
from ..schemas import NonBlankStr


class KindEntryPointRecord(VersionedRecord):
    status: Literal["not_exposed"]
    reason_code: ReasonCode
    message: NonBlankStr


def real_kind_qualification_help(*, opt_in: bool = False) -> KindEntryPointRecord:
    del opt_in
    return KindEntryPointRecord(
        schema_version=1,
        status="not_exposed",
        reason_code=ReasonCode.POLICY_VIOLATION,
        message="real kind qualification is opt-in and currently exposes prerequisites only",
    )
