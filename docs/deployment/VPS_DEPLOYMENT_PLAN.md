# VPS Deployment Plan

## Preconditions

- Gate 1 discovery has been rerun on the production VPS and the resulting `output/vps` reports have been reviewed.
- Migration manifest reviewed: `docs/migration/MIGRATION_MANIFEST.md`.
- Existing Hermes runtime is healthy:
  - `hermes-telegram.service` active
  - Hermes container present
  - Existing ingress unchanged
- `/docker/obsidian-vault` is readable from the host and will remain untouched.
- Sufficient disk exists for `/opt/alfred` plus build artefacts.
- Existing `python3`, `node`, and `npm` are present and acceptable for reuse.
- `/opt/alfred` is available for side-by-side installation and contains no conflicting live service owned by Hermes.

## Installation Order

1. Run `deploy_stage1.sh` for read-only prechecks:
   - disk
   - Docker
   - Python
   - Node
   - current services
   - vault accessibility
2. Install Alfred side-by-side into `/opt/alfred` using the Gate 2 package:
   - `scripts/install/install_alfred_platform.sh`
   - `scripts/install/configure_alfred.sh`
   - `scripts/install/start_alfred.sh`
3. Review `/opt/alfred/config/config.yaml` and confirm:
   - `profile: VPS`
   - existing Python/Node paths are reused
   - vault path points to the intended readable location only
4. Run `deploy_validation.sh` to generate and verify:
   - UI build
   - Dashboard API
   - ExecutiveState
   - Pipeline
   - Daily Brief
   - Operational Readiness

## Validation Gates

- Stage 1 prechecks must all pass.
- `/opt/alfred/app/output/Dashboard_Home.json` exists.
- `/opt/alfred/app/output/ExecutiveState_Summary.md` exists.
- `/opt/alfred/app/output/Executive_Pipeline_Report.md` exists.
- `/opt/alfred/app/output/Daily_Brief.md` exists.
- `/opt/alfred/app/dist/index.html` exists.
- `scripts/install/status_alfred.sh` reports:
  - build version
  - Python
  - Node
  - vault configured
  - ExecutiveState freshness
  - Dashboard API
  - UI status
  - optional services
- `output/Operational_Readiness_Report.md` is `GREEN`.

## Rollback Plan

- Do not touch Hermes.
- Do not change Cloudflare.
- Do not change Telegram.
- Do not change the Obsidian vault.
- If Alfred validation fails:
  1. Run `deploy_rollback.sh`.
  2. This clears Alfred runtime markers only.
  3. Preserve `/opt/alfred`, logs, config, and generated outputs for inspection.
  4. Continue using Hermes as the active production path.

## Cutover Plan

- Target cutover is a later controlled step, not part of this deployment preparation.
- Alfred must first prove:
  - reproducible build success
  - reproducible pipeline success
  - green operational readiness
  - zero impact on Hermes
- Any public routing or operator-interface move should occur only in Gate 5.

## Risks

- Gate 1 output reports are not committed on `main`; they must be regenerated before execution.
- Existing Node or Python versions may be present but incompatible with future package evolution.
- Operational Readiness may remain non-green if vault path, outputs, or environment assumptions are wrong.
- Optional retrieval and enrichment services are intentionally not installed and must remain placeholders.
- Building alongside Hermes still consumes host disk and CPU, so preflight capacity checks matter.

## Estimated Downtime

- Target: zero.
- Alfred installs alongside Hermes without stopping or modifying Hermes-owned services.
