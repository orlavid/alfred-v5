# Migration Manifest

## Gate 1 Discovery

Capture the current Hermes VPS estate as a complete, read-only migration manifest.

- Inventory storage, runtime, configuration, and data assets.
- Build a dependency graph and asset register.
- Classify each discovered asset as `KEEP`, `REPLACE`, `ARCHIVE`, `DELETE`, or `UNKNOWN`.
- Make no destructive changes, no configuration changes, and no service restarts.

## Gate 2 Deploy

Prepare the target Alfred deployment package without touching the live cutover path.

- Stand up the target runtime from the Alfred repository.
- Recreate only the assets classified as `KEEP` or deliberate `REPLACE`.
- Keep legacy Hermes runtime isolated for fallback.

## Gate 3 Live Knowledge

Reconnect live executive knowledge flows on the target platform.

- Validate canonical vault availability.
- Rebuild knowledge, graph, runtime state, and dashboard outputs from the target environment.
- Reintroduce optional services only after explicit validation.

## Gate 4 Acceptance

Confirm the new deployment behaves as expected before traffic moves.

- Validate builds, tests, and operational readiness.
- Compare executive outputs against the known-good Hermes baseline.
- Confirm data freshness and dependency integrity.

## Gate 5 Cutover

Move live usage from Hermes to the target Alfred package with rollback protection.

- Switch operator usage to the new platform.
- Retain Hermes artefacts for rollback and audit.
- Archive replaced runtime components only after the new path is stable.
