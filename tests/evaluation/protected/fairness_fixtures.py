from __future__ import annotations

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    Language,
    MetamorphicFixtureGroup,
    MetamorphicVariant,
    MetamorphicVariantKind,
    TaskClass,
)
from thesis_bench.records import ProtectedRootReference

from .contracts import mixed_contract
from .fixtures import semantic_knowledge_contract


def fairness_group(task_class: TaskClass, language: Language) -> MetamorphicFixtureGroup:
    contract = (
        semantic_knowledge_contract() if task_class == TaskClass.KNOWLEDGE else mixed_contract()
    ).model_copy(update={"language": language})
    return MetamorphicFixtureGroup(
        schema_version=1,
        group_id=f"group-{task_class.value}-{language.value}",
        task_class=task_class,
        language=language,
        contract=contract,
        variant_ids=tuple(kind.value for kind in MetamorphicVariantKind),
        variants=tuple(
            MetamorphicVariant(schema_version=1, variant_id=kind.value, kind=kind)
            for kind in MetamorphicVariantKind
        ),
        protected_fixture_reference=ProtectedRootReference(
            schema_version=1,
            root_id=APPROVED_PROTECTED_ROOT,
            relative_path=f"fairness/{task_class.value}-{language.value}.json",
            content_sha256="e" * 64,
        ),
    )
