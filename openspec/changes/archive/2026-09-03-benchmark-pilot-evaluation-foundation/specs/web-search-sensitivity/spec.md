## Purpose

Define a separately named official-source W1 sensitivity condition whose access, budgets, and retrieved evidence are bounded and auditable without exposing benchmark or golden repositories.

## ADDED Requirements

### Requirement: Explicit W1 condition identity
A web-enabled attempt SHALL identify itself as W1 or as an explicitly approved combined condition. R1 and H1 configurations SHALL reject implicit open-web access.

#### Scenario: W1 requested explicitly
- **WHEN** an eligible manifest names W1 and its policy identity
- **THEN** the web boundary may validate the request

#### Scenario: H1 requests web access
- **WHEN** H1 without a separately approved combined identifier requests search or fetch
- **THEN** the request is denied and recorded as a policy violation

### Requirement: Official-source allowlist and deny boundary
The web boundary SHALL allow only versioned policy entries for official Kubernetes documentation and approved upstream repository content. It SHALL revalidate redirects and SHALL deny this thesis repository, benchmark/golden storage, user files, local addresses, and all non-allowlisted domains.

#### Scenario: Allowed official page
- **WHEN** a search result and every redirect resolve to an allowlisted official path
- **THEN** the page may be fetched within the remaining budget

#### Scenario: Redirect leaves allowlist
- **WHEN** an allowed URL redirects to a prohibited host or path
- **THEN** the fetch is denied before prohibited content is read and the redirect is captured

#### Scenario: Benchmark repository requested
- **WHEN** a query or fetch targets the thesis repository or protected benchmark/golden location
- **THEN** access is denied regardless of remaining budget

### Requirement: Frozen per-response budgets
W1 SHALL enforce at most three search calls, five results per search, two page fetches, five total tool calls, 4,000 extracted context tokens, and 120 seconds of tool wall time per response. Extracted tokens SHALL be counted from the actual body before exposure, and search/fetch wall time SHALL include measured provider work rather than trusting preparation metadata alone. A combined condition SHALL use the same W1 budget unless separately approved before outputs.

#### Scenario: Request within budget
- **WHEN** the next operation remains within every frozen limit
- **THEN** it may execute and cumulative usage is updated

#### Scenario: Any limit exceeded
- **WHEN** the next operation would exceed a call, result, fetch, token, or time limit
- **THEN** it is denied and budget exhaustion is recorded as a valid W1 task failure

### Requirement: Complete retrieval provenance
Before retrieved text is exposed to a model, the system SHALL persist query, result rank, original/final URL, redirects, UTC timestamps, status, visible-body snapshot where lawful or immutable reference/hash otherwise, content hash, available tool/provider identity, extracted token count, rejection, error, and cumulative budget.

#### Scenario: Complete capture
- **WHEN** an allowed search or fetch succeeds and all required provenance is persisted
- **THEN** the bounded result may enter the model context

#### Scenario: Capture fails
- **WHEN** required provenance or content identity cannot be persisted
- **THEN** no retrieved text is exposed, and the attempt is marked invalid due to measurement infrastructure

#### Scenario: Provider version unavailable
- **WHEN** the provider does not expose a version
- **THEN** the record uses an explicit `not_exposed` value rather than inventing or omitting identity

### Requirement: Source-drift precheck
Each W1 family SHALL record a human pre-run decision, reviewer identity, rationale, frozen/current source hashes, and semantic-compatibility decision that the currently reachable official source preserves the frozen answer contract or identify a changed/unavailable source before model execution.

#### Scenario: Contract remains valid
- **WHEN** the human precheck confirms semantic compatibility with the pinned source snapshot
- **THEN** W1 execution may proceed without changing the item or evaluator

#### Scenario: Official answer changed
- **WHEN** the current official source changes the correct answer or required constraints
- **THEN** the W1 attempt is deferred and the source drift is reported without rewriting the family after outputs

### Requirement: Golden and evaluator isolation
Search queries, fetched pages, provider logs, model context, and W1 captures SHALL NOT receive golden answers, protected evidence maps, evaluator logic, or final-test payloads.

#### Scenario: Protected content routed to W1
- **WHEN** a W1 request context references protected evaluator or final-test material
- **THEN** preparation fails before any external request

### Requirement: W1 feasibility qualification
The system SHALL require complete provenance for every attempted access, zero successful deny-fixture access, redirect conformance, and at least 90% within-budget completion across eligible pilot attempts. Provider/service failure SHALL remain recorded as a valid W1 availability failure when capture is intact.

#### Scenario: W1 qualifies
- **WHEN** every access-control/provenance check passes and completion is at least 90%
- **THEN** qualification is `GO` for sensitivity use

#### Scenario: Prohibited access succeeds
- **WHEN** any deny fixture reaches prohibited content or a response is exposed without provenance
- **THEN** qualification is `STOP/DEFER` and W1 remains disabled

### Requirement: Routine tests remain offline
Routine validation and CI SHALL use deterministic search/fetch fakes and SHALL NOT contact external services.

#### Scenario: Default test suite
- **WHEN** routine tests execute without an explicit integration opt-in
- **THEN** every W1 response comes from a local deterministic fake and no network request occurs
