# AUTONOMY WORKER BRIDGE V1

## Purpose

AUTONOMY-02 installs the Worker Execution Bridge V1 for structured claim and result execution handoff.

Bridge capabilities:
- claim mode packetization for an existing structured task issue
- result mode completion packetization with status reconciliation
- deterministic artifact emission
- deterministic comment markers for downstream automation

## Scope

Working routes:
- workflow-only / no API route changes

The bridge is additive and does not replace deploy workflows.

## Lifecycle

1. Router normalizes task packet and applies queued status.
2. Worker bridge runs in `claim` mode.
3. Bridge emits packet artifacts and posts packet marker comment.
4. Worker executes assigned scope.
5. Worker bridge runs in `result` mode.
6. Bridge emits result/handoff artifacts and posts result + handoff comments.
7. Status reconcile workflow enforces a single `status:*` label.

## Contracts

### Workflow: `.github/workflows/worker_bridge.yml`

Modes:
- `claim`
- `result`

Required markers:
- `<!-- autonomy-worker-packet -->`
- `<!-- autonomy-worker-result -->`
- `<!-- autonomy-pr-handoff -->`

Required artifacts:
- `worker_packet.json`
- `worker_packet.txt`
- `worker_result.json`
- `worker_result.txt`
- `worker_handoff.txt`

### Workflow: `.github/workflows/task_status_reconcile.yml`

Rules:
- enforce exactly one status label
- add `status:queued` when no status label exists
- post reconcile comment marker `<!-- autonomy-status-reconcile -->`

## Dry-Run (Manual)

1. Open a structured autonomous task issue.
2. Run `worker_bridge.yml` with mode `claim`.
3. Verify packet comment marker and artifacts.
4. Run `worker_bridge.yml` with mode `result`.
5. Verify result + handoff markers and artifacts.
6. Run `task_status_reconcile.yml` for the issue.
7. Verify one and only one status label remains.

## Example Input Issue Body

### lane
be-core

### task_type
infra

### objective
Install worker bridge and status reconcile workflows.

### target_files
.github/workflows/worker_bridge.yml
.github/workflows/task_status_reconcile.yml
docs/governance/AUTONOMY_WORKER_BRIDGE_V1.md

### acceptance_criteria
Bridge emits packet/result/handoff artifacts.
Reconcile enforces single status label.

### proof_required
A-E

### environment
staging

### priority
p1

### execution_agent
vs

## Expected Labels Before Execution
- lane:be-core
- status:queued
- agent:vs

## Worker Packet Comment Output

<!-- autonomy-worker-packet -->
## Worker Packet
mode: claim
worker: vs
issue_number: 123
lane: be-core
task_type: infra
objective: Install worker bridge and status reconcile workflows.
target_files: .github/workflows/worker_bridge.yml
.github/workflows/task_status_reconcile.yml
docs/governance/AUTONOMY_WORKER_BRIDGE_V1.md
acceptance_criteria: Bridge emits packet/result/handoff artifacts.
Reconcile enforces single status label.
proof_required: A-E
environment: staging
priority: p1
execution_agent: vs

## Worker Result Comment Output

<!-- autonomy-worker-result -->
## Worker Result
mode: result
worker: vs
issue_number: 123
result_status: status:proof-ready
result_summary: AUTONOMY-02 installed and validated.
evidence_paths: docs/proofpacks/2026-03-06_be-core_autonomy-02

## PR / Commit Handoff Comment Output

<!-- autonomy-pr-handoff -->
## PR / Commit Handoff
worker: vs
issue_number: 123
pr_number: 456
commit_sha: abcdef1234567890
handoff_note: Ready for BE-Core review.

## Final Expected Status Labels
- status:proof-ready