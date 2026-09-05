from __future__ import annotations

from thesis_bench.evaluation.protected import (
    AssessmentSource,
    AuditPolicy,
    CriterionDisposition,
    DecodingPolicy,
    JudgeConfiguration,
    JudgeFairnessCase,
    JudgeResponseSchema,
    JudgeScope,
    Language,
    MetamorphicVariantKind,
    QualificationThresholds,
    TaskClass,
)
from thesis_bench.records import content_sha256

from .fixtures import assessment, complete_knowledge_assessments, semantic_knowledge_contract


def judge_configuration() -> JudgeConfiguration:
    response_schema = JudgeResponseSchema(
        schema_version=1,
        schema_id="criterion-disposition-schema",
        schema_version_id="v1",
        schema_sha256="2" * 64,
    )
    decoding_policy = DecodingPolicy(
        schema_version=1,
        temperature=0.0,
        top_p=1.0,
        max_output_tokens=128,
        max_retries=0,
        failure_policy="route_to_human",
    )
    thresholds = QualificationThresholds(
        schema_version=1,
        threshold_set_id="deferred-thresholds",
        minimum_criterion_agreement=None,
        minimum_kappa=None,
        maximum_unresolved_rate=None,
    )
    audit_policy = AuditPolicy(
        schema_version=1,
        audit_policy_id="audit-policy-1",
        sampling_identity="predeclared-sampling-rule",
        frozen_before_outcomes=True,
        blinded=True,
    )
    scope = JudgeScope(
        schema_version=1,
        task_class=TaskClass.KNOWLEDGE,
        language=Language.EN,
        criterion_ids=("claim-a",),
    )
    candidate = JudgeConfiguration.model_construct(
        schema_version=1,
        judge_config_id="judge-config-1",
        revision="v1",
        model_identity="deferred-model-identity",
        provider_or_artifact_identity="deferred-provider-or-artifact",
        backend_identity="deferred-backend-v1",
        prompt_template_identity="deferred-template",
        prompt_template_sha256="1" * 64,
        response_schema=response_schema,
        decoding_policy=decoding_policy,
        protected_input_contract_id="protected-input-contract-v1",
        protected_input_contract_sha256="4" * 64,
        qualification_set_id="qualification-set-1",
        qualification_set_sha256="3" * 64,
        qualification_thresholds=thresholds,
        audit_policy=audit_policy,
        scopes=(scope,),
        state="frozen",
    )
    digest = content_sha256(candidate.model_dump(mode="json", exclude={"content_sha256"}))
    return JudgeConfiguration.model_validate({**candidate.model_dump(), "content_sha256": digest})


def rehash_judge_configuration(
    configuration: JudgeConfiguration, **updates: object
) -> JudgeConfiguration:
    candidate = configuration.model_copy(update=updates)
    digest = content_sha256(candidate.model_dump(mode="json", exclude={"content_sha256"}))
    return candidate.model_copy(update={"content_sha256": digest})


def judge_fairness_case(config: JudgeConfiguration) -> JudgeFairnessCase:
    def judge_variant(assessments: tuple) -> tuple:
        return tuple(
            assessment(
                item.criterion_id,
                item.disposition,
                AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
                judge_config_id=config.judge_config_id,
            )
            for item in assessments
        )

    return JudgeFairnessCase(
        schema_version=1,
        case_id="judge-fairness-case-1",
        scope_key="knowledge-en",
        contract=semantic_knowledge_contract(),
        covered_rule_ids=("claim-a", "claim-b"),
        primary_scores={
            MetamorphicVariantKind.CONCISE_CORRECT_PARAPHRASE: 1.0,
            MetamorphicVariantKind.CORRECT_SOURCE_LIKE: 1.0,
            MetamorphicVariantKind.ACCEPTED_SYNONYM_REORDERING: 1.0,
            MetamorphicVariantKind.LEXICALLY_SIMILAR_WRONG: 0.5,
            MetamorphicVariantKind.PARTIAL_MISSING_CLAIM: 0.5,
            MetamorphicVariantKind.IRRELEVANT_SOURCE_APPENDED: 1.0,
        },
        variants={
            MetamorphicVariantKind.CONCISE_CORRECT_PARAPHRASE: judge_variant(
                complete_knowledge_assessments()
            ),
            MetamorphicVariantKind.CORRECT_SOURCE_LIKE: judge_variant(
                complete_knowledge_assessments()
            ),
            MetamorphicVariantKind.ACCEPTED_SYNONYM_REORDERING: judge_variant(
                complete_knowledge_assessments()
            ),
            MetamorphicVariantKind.LEXICALLY_SIMILAR_WRONG: judge_variant(
                complete_knowledge_assessments(claim_a=CriterionDisposition.NOT_SATISFIED)
            ),
            MetamorphicVariantKind.PARTIAL_MISSING_CLAIM: judge_variant(
                complete_knowledge_assessments(claim_b=CriterionDisposition.NOT_SATISFIED)
            ),
            MetamorphicVariantKind.IRRELEVANT_SOURCE_APPENDED: judge_variant(
                complete_knowledge_assessments()
            ),
        },
        affected_criterion_ids={
            MetamorphicVariantKind.LEXICALLY_SIMILAR_WRONG: ("claim-a",),
            MetamorphicVariantKind.PARTIAL_MISSING_CLAIM: ("claim-b",),
        },
    )
