## Purpose

Provide a deliberately small command-line boundary for validating metadata, preparing provenance-only runs, and inspecting run integrity in local development and CI.

## ADDED Requirements

### Requirement: Stable command set

The installed `thesis-bench` command SHALL provide `validate-config <experiment-path>`, `prepare-run <experiment-path> [--results-root <path>]`, `show-run <run-directory>`, and `--version`. It SHALL NOT provide experiment execution or model-management commands in this change.

#### Scenario: Help requested
- **WHEN** a user invokes the root command or a subcommand with `--help`
- **THEN** the CLI describes only the approved foundation commands and exits successfully

#### Scenario: Version requested
- **WHEN** a user invokes `thesis-bench --version`
- **THEN** the CLI prints the installed package version and exits successfully

### Requirement: Configuration validation command

`validate-config` SHALL perform the complete side-effect-free configuration validation and SHALL print a JSON object containing `valid: true`, the experiment and condition IDs, normalized project-relative source paths, and source/semantic hashes on success.

#### Scenario: Valid configuration from CLI
- **WHEN** `validate-config` receives a valid experiment path
- **THEN** it emits the required JSON on standard output, emits no error on standard error, and exits `0`

#### Scenario: Invalid configuration from CLI
- **WHEN** configuration validation fails
- **THEN** it emits a structured error on standard error, emits no success document, exits `2`, and creates no run directory

### Requirement: Run preparation command

`prepare-run` SHALL validate configuration and provenance and then create one prepared run without executing a model. The default results root SHALL be `<project-root>/results/raw`; an explicit results root SHALL be supported for isolated tests and exploratory storage. On success the command SHALL print a JSON object containing the run ID, project-relative run path when applicable, manifest semantic hash, and `status: prepared`.

#### Scenario: Prepare with default root
- **WHEN** `prepare-run` succeeds without `--results-root`
- **THEN** it publishes one run under the project `results/raw` directory and exits `0`

#### Scenario: Preparation provenance failure
- **WHEN** Git or filesystem requirements prevent preparation
- **THEN** the command emits a structured error on standard error, exits `3`, and does not report a successful run

#### Scenario: Existing target or integrity conflict
- **WHEN** preparation encounters an existing run target or detects unsafe existing content
- **THEN** the command exits `4` and leaves existing content unchanged

### Requirement: Run inspection command

`show-run` SHALL perform read-only integrity inspection and print a JSON summary containing the run, experiment, condition, run kind, preparation timestamp, Git commit and cleanliness, and latest event type.

#### Scenario: Show intact run
- **WHEN** `show-run` receives an intact prepared run directory
- **THEN** it emits the summary on standard output and exits `0`

#### Scenario: Missing run
- **WHEN** the supplied run directory does not exist
- **THEN** it emits a structured error on standard error and exits `2`

#### Scenario: Corrupt run
- **WHEN** the supplied run fails integrity inspection
- **THEN** it emits a structured integrity error on standard error, exits `4`, and makes no filesystem changes

### Requirement: Machine-readable diagnostics

All successful command payloads and non-help diagnostics SHALL be UTF-8 JSON with a trailing newline. Error objects SHALL contain a stable error code, a concise message, and optional safe location details; they SHALL not include Python tracebacks unless an explicit developer-debug mechanism is added in a later approved change.

#### Scenario: Expected user error
- **WHEN** a command encounters invalid user input
- **THEN** the emitted error is parseable JSON and contains no traceback

#### Scenario: Output is redirected
- **WHEN** a command is used by CI or a script
- **THEN** standard output contains only the success JSON and standard error contains only diagnostics
