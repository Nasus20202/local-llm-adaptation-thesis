from __future__ import annotations

from pydantic import Field, model_validator

from ..records import VersionedRecord
from ..schemas import Identifier
from .family import FamilyRecord
from .models import VariantRecord


class PilotManifest(VersionedRecord):
    manifest_id: Identifier
    policy_version: Identifier
    families: tuple[FamilyRecord, ...] = Field(min_length=1)
    variants: tuple[VariantRecord, ...] = ()

    @model_validator(mode="after")
    def validate_identity_and_nesting(self) -> PilotManifest:
        if self.policy_version != "pilot-policy-v1":
            raise ValueError("unknown pilot policy version")
        family_ids = [family.family_id for family in self.families]
        if len(set(family_ids)) != len(family_ids):
            raise ValueError("family identifiers must be unique")
        variant_ids = [variant.variant_id for variant in self.variants]
        if len(set(variant_ids)) != len(variant_ids):
            raise ValueError("variant identifiers must be unique")
        family_set = set(family_ids)
        if any(variant.family_id not in family_set for variant in self.variants):
            raise ValueError("variant must reference a manifest family")
        return self
