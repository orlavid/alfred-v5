# VPS Deployment Plan

## Preconditions

- Gate 1 discovery has been rerun on the production VPS and the resulting `output/vps` reports have been reviewed.
- Migration manifest reviewed: `docs/migration/MIGRATION_MANIFEST.md`.
- Executive acceptance pack reviewed: `docs/deployment/EXECUTIVE_ACCEPTANCE_TESTS.md`.
- Existing Hermes runtime is healthy:
  - `hermes-telegram.service` active
  - Hermes container present
  - Existing ingress unchanged
- `/docker/obsidian-vault` is readable from the host and will remain untouched.
- Sufficient disk exists for `/opt/alfred` plus build artefacts.
- Sufficient inode capacity exists for `/opt/alfred`, log growth, and generated outputs.
- Existing `python3`, `node`, and `npm` are present and acceptable for reuse.
- `/opt/alfred` is available for side-by-side installation and contains no conflicting live service owned by Hermes.
- A recovery bundle exists and manual Hostinger snapshot confirmation has been completed before execution.

## Configuration Migration

- Alfred configuration is created at `/opt/alfred/config/config.yaml` by `scripts/install/configure_alfred.sh` only if that file does not already exist.
- Deployment execution must provide `ALFRED_OBSIDIAN_VAULT`; the installer fails if the vault path is not explicitly supplied.
- `config.yaml` must contain at minimum:
  - deployment profile
  - build version
  - install, app, config, data, logs, runtime, vault, and output paths
  - Python and Node executable locations
  - optional service toggles
  - model provider and model placeholders
  - API base URL and key environment-variable placeholder
- Secrets are never printed and are not written directly into the file by the deployment plan. Only environment-variable placeholders are recorded.
- If required configuration fields are missing after creation, Stage 2 fails immediately.

## Sacred Asset Verification

- `scripts/vps/verify_sacred_assets.sh` must succeed before any install action.
- Verify, but do not modify:
  - Cloudflare config present
  - Telegram env or service present
  - Obsidian vault path readable
  - optional LlamaIndex or enrichment config if already present
  - recovery bundle present
  - Hostinger snapshot manually confirmed
- Failure at this stage blocks deployment. No automated remediation is permitted in Gate 3.

## Installation Order

1. Run `deploy_stage1.sh` for read-only prechecks:
   - disk
   - inode capacity
   - Docker
   - Python
   - Node
   - current services
   - vault accessibility
   - sacred asset verification
   - capacity and projected growth review
2. Install Alfred side-by-side into `/opt/alfred` using the Gate 2 package:
   - `scripts/install/install_alfred_platform.sh`
   - `scripts/install/configure_alfred.sh`
   - `scripts/install/start_alfred.sh`
3. Review `/opt/alfred/config/config.yaml` and confirm:
   - `profile: VPS`
   - existing Python/Node paths are reused
   - vault path points to the intended readable location only
   - output path is explicit
   - optional services are toggled as placeholders only
   - model and API entries contain placeholders, not secrets
4. Run `deploy_validation.sh` to generate and verify:
   - UI build
   - Dashboard API
   - ExecutiveState
    - Pipeline
    - Daily Brief
    - Operational Readiness
    - live knowledge certification
    - executive acceptance prompts

## Knowledge Certification

- `scripts/vps/certify_live_knowledge.sh` is the hard gate that proves Alfred is reading configured Obsidian data instead of placeholder or demo data.
- The certification report must capture:
  - objectives count
  - projects count
  - companies count
  - people count
  - decisions count
  - daily logs count
  - open loops count
  - follow-ups count
  - knowledge graph nodes and edges
  - ExecutiveState generated confirmation
- Unexpected zero counts produce a failure for core knowledge domains and a warning for secondary domains. Deployment may not proceed on a failed certification.

## Executive Acceptance Tests

- The operator must run the scripted acceptance prompts documented in `docs/deployment/EXECUTIVE_ACCEPTANCE_TESTS.md`.
- Required questions:
  - What should I focus on today?
  - What are my top objectives?
  - Prepare me for Barclays.
  - What changed yesterday?
  - Which projects are at risk?
  - What follow-ups need action?
- Acceptance requires evidence-backed answers and successful output generation without impacting Hermes.

## Capacity And Growth Assessment

- `scripts/vps/check_capacity_growth.sh` captures:
  - disk free
  - inode free
  - Docker usage
  - log directory size
  - `/opt/alfred` projected growth
  - output directory size
  - warning thresholds for review
- Any threshold breach must be resolved before execution, not during it.

## Validation Gates

- Stage 1 prechecks must all pass.
- Sacred asset verification must pass.
- Capacity review must complete with no unresolved red flags.
- Configuration verification must confirm no missing required fields and no printed secrets.
- Knowledge certification must pass and show non-placeholder evidence counts.
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
- Executive acceptance prompts complete successfully.

## Rollback Plan

- Do not touch Hermes.
- Do not change Cloudflare.
- Do not change Telegram.
- Do not change the Obsidian vault.
- Do not delete Alfred data automatically.
- If Alfred validation fails:
  1. Run `deploy_rollback.sh`.
  2. This disables or removes Alfred runtime markers only.
  3. Preserve `/opt/alfred`, logs, config, and generated outputs for inspection.
  4. Continue using Hermes as the active production path.
  5. Hostinger snapshot recovery is not automatic and is not part of this rollback unless separately approved.

## Cutover Plan

- Target cutover is a later controlled step, not part of this deployment preparation.
- Alfred must first prove:
  - reproducible build success
  - reproducible pipeline success
  - green operational readiness
  - live knowledge certification against the real vault
  - executive acceptance answers are credible and evidence-backed
  - zero impact on Hermes
- Any public routing or operator-interface move should occur only in Gate 5.

## Risks

- Gate 1 output reports are not committed on `main`; they must be regenerated before execution.
- Existing Node or Python versions may be present but incompatible with future package evolution.
- Operational Readiness may remain non-green if vault path, outputs, or environment assumptions are wrong.
- Optional retrieval and enrichment services are intentionally not installed and must remain placeholders.
- Building alongside Hermes still consumes host disk and CPU, so preflight capacity checks matter.
- ExecutiveState currently remains a generated artefact gate; live-knowledge proof depends on the knowledge builder and certification script, not on a separate runtime daemon.
- Snapshot confirmation is manual, so operator discipline is part of deployment risk control.

## Estimated Downtime

- Target: zero.
- Alfred installs alongside Hermes without stopping or modifying Hermes-owned services.
