## Purpose

Provide an opt-in, deterministic, and auditable execution boundary for a small paired static/interactive Kubernetes pilot without granting any adaptation condition privileged tools or uncontrolled cluster access.

## ADDED Requirements

### Requirement: Pinned disposable environment
Every interactive attempt SHALL identify the `kind` binary revision, node-image digest, workload-image digests, cluster configuration hash, host/container-runtime identity, namespace, scenario-family/variant identity, reset policy, and validator version. Mutable tags SHALL be rejected.

#### Scenario: Fully pinned environment
- **WHEN** all executable and image identities are immutable and the configuration hash resolves
- **THEN** the environment is eligible for reset validation

#### Scenario: Mutable image tag
- **WHEN** a node or workload image is identified only by a mutable tag
- **THEN** preparation fails before a cluster task starts

### Requirement: Deterministic reset and initial-state verification
The executor SHALL recreate or reset the isolated task state before every attempt and SHALL verify the declared initial-state hash and expected pre-task validator result before exposing observations.

#### Scenario: Reset matches expected state
- **WHEN** reset completes and both initial-state checks match
- **THEN** the attempt may begin and the reset evidence is recorded

#### Scenario: Reset mismatch
- **WHEN** the state hash or pre-task validator result differs
- **THEN** the attempt is invalid due to infrastructure and no model/task action is accepted

### Requirement: Namespace, privilege, and egress isolation
Benchmark workloads SHALL use a dedicated namespace, dummy credentials, no host mounts, no privileged task workloads, no cluster-scoped mutation, and no external DNS or network egress. The executor SHALL run approved positive permission fixtures and negative permission/egress fixtures before the stratum can qualify.

#### Scenario: Prohibited operation attempted
- **WHEN** a task requests cluster-scoped mutation, host/process access, privileged execution, secret exfiltration, or a non-allowlisted command
- **THEN** the executor denies the action, records the denial, and leaves the protected boundary unchanged

#### Scenario: Outbound access probe
- **WHEN** a task workload attempts DNS resolution or outbound HTTP(S)
- **THEN** the connection fails and the complete deny-fixture result is recorded

### Requirement: Matched neutral execution interface
Every applicable condition SHALL receive the same operation schema, command/action allowlist, namespace permissions, initial state, maximum action count, tool-output limit, timeout, and final-state validator. B0-I SHALL identify B0 under this nested interactive observation form rather than a new adaptation family. H1/S1 metadata SHALL NOT alter the neutral access contract.

#### Scenario: Conditions have matched access
- **WHEN** two applicable condition manifests reference one interactive family
- **THEN** validation confirms identical neutral execution-policy hashes

#### Scenario: Condition receives extra permission
- **WHEN** a condition declares a larger permission, action, observation, context, or time budget
- **THEN** comparison validation fails before execution

### Requirement: Complete append-only action capture
The executor SHALL append an ordered record for every requested action, normalized arguments, start/end timestamp, outcome, bounded stdout/stderr or structured result, denial, timeout, state-changing resource identity, and cumulative budget. It SHALL NOT overwrite an attempt.

#### Scenario: Allowed action completes
- **WHEN** an allowlisted observation or remediation action completes
- **THEN** its ordered capture and updated budget are persisted before the next action

#### Scenario: Budget exhausted
- **WHEN** the next action would exceed the frozen action, output, or time budget
- **THEN** the action is denied and the attempt ends as a valid evaluated-system failure with captured reason

### Requirement: Automatic final-state evaluation
Each interactive family SHALL reference a versioned final-state validator with positive, negative, boundary, malformed, and ambiguous fixtures. The executor SHALL run it after completion or budget termination and preserve both machine outcome and reason codes.

#### Scenario: Task succeeds
- **WHEN** the final state satisfies all required invariants and no prohibited-action gate failed
- **THEN** the primary interactive outcome is success

#### Scenario: Semantically plausible explanation without state repair
- **WHEN** the response explains the fault but the required final-state invariant is false
- **THEN** the primary interactive outcome is failure and any diagnosis score remains supporting evidence

### Requirement: Opt-in external execution
Routine validation and CI SHALL use synthetic fixtures and process fakes. Real `kind` creation SHALL require an explicit opt-in command/configuration and SHALL never run as an import side effect or routine test.

#### Scenario: Routine CI executes
- **WHEN** the default test suite runs without the opt-in flag
- **THEN** no real cluster, image pull, privileged node container, or network probe is started

### Requirement: Feasibility qualification
The system SHALL report the ten-reset, ten-egress-deny, permission, validator, matched-access, paired-variant, and reset-duration checks required by the approved protocol. Any isolation or privilege failure SHALL produce `STOP/DEFER`.

#### Scenario: All cluster checks pass
- **WHEN** every mandatory check meets its threshold
- **THEN** the controlled cluster stratum receives `GO`

#### Scenario: Isolation failure
- **WHEN** any prohibited outbound or privileged operation succeeds
- **THEN** qualification is `STOP/DEFER` and interactive execution remains disabled
