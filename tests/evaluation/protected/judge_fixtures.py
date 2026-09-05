from __future__ import annotations

from thesis_bench.evaluation.protected import (
    APPROVED_PROTECTED_ROOT,
    AssessmentSource,
    AuditPolicy,
    CriterionDisposition,
    DecodingPolicy,
    JudgeConfiguration,
    JudgeCriterionAuthorization,
    JudgeFairnessCase,
    JudgeQualification,
    JudgeResponseSchema,
    JudgeScope,
    Language,
    MetamorphicVariantKind,
    QualificationThresholds,
    TaskClass,
    qualify_judge_configuration,
)
from thesis_bench.records import ProtectedRootReference, content_sha256

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
        membership_manifest_id="audit-membership-manifest-1",
        membership_manifest_sha256="6" * 64,
        membership_manifest_root_reference=ProtectedRootReference(
            schema_version=1,
            root_id=APPROVED_PROTECTED_ROOT,
            relative_path="audit/membership-manifest-1.json",
            content_sha256="6" * 64,
        ),
        selected_response_ids=("response-1",),
    )
    authorization = JudgeCriterionAuthorization(
        schema_version=1,
        task_class=TaskClass.KNOWLEDGE,
        language=Language.EN,
        criterion_id="claim-a",
        protected_input_contract_id="protected-input-contract-v1",
        protected_input_contract_sha256="4" * 64,
        artifact_id="criterion-input-claim-a-1",
        artifact_kind="semantic-criterion-input",
        artifact_sha256="5" * 64,
        root_reference=ProtectedRootReference(
            schema_version=1,
            root_id=APPROVED_PROTECTED_ROOT,
            relative_path="judge-inputs/claim-a.json",
            content_sha256="5" * 64,
        ),
    )
    scope = JudgeScope(
        schema_version=1,
        task_class=TaskClass.KNOWLEDGE,
        language=Language.EN,
        criterion_ids=("claim-a",),
        criterion_authorizations=(authorization,),
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


def qualified_judge() -> tuple[JudgeConfiguration, JudgeQualification]:
    config = rehash_judge_configuration(
        judge_configuration(),
        qualification_thresholds=QualificationThresholds(
            schema_version=1,
            threshold_set_id="synthetic-test-thresholds",
            minimum_criterion_agreement=0.0,
            minimum_kappa=None,
            maximum_unresolved_rate=1.0,
        ),
    )
    qualification = qualify_judge_configuration(
        config,
        criterion_agreement={"claim-a": 1.0},
        confusion_matrix={"claim-a": {"satisfied": {"satisfied": 4}}},
        unresolved_count=0,
        schema_failure_count=0,
        fairness_cases=(judge_fairness_case(config),),
        qualification_adjudications=(),
        qualification_revision="v1",
        qualification_root_reference=ProtectedRootReference(
            schema_version=1,
            root_id=APPROVED_PROTECTED_ROOT,
            relative_path="qualification/synthetic-green.json",
            content_sha256="0" * 64,
        ),
    )
    return config, qualification


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
                complete_knowledge_assessments(unsupported=CriterionDisposition.SATISFIED)
            ),
        },
    )
