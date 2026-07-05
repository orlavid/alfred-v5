# Alfred Platform Installation Guide

## Objective

Install Alfred as a repeatable package alongside the existing Hermes runtime without affecting it.

This is an installation package, not a migration and not a live deploy.

## Install Root

Alfred installs into:

- `/opt/alfred`

With standard folders:

- `/opt/alfred/app`
- `/opt/alfred/config`
- `/opt/alfred/data`
- `/opt/alfred/logs`
- `/opt/alfred/runtime`

## Configuration Registry

Everything configurable for the package should be sourced from:

- `/opt/alfred/config/config.yaml`

No runtime path should need to be hard-coded outside the installer defaults that seed this file.

## Deployment Profiles

Supported package profiles:

- Local Development
- Single Machine
- VPS
- Enterprise (placeholder)

## Package Scripts

- `scripts/install/install_alfred_platform.sh`
- `scripts/install/configure_alfred.sh`
- `scripts/install/start_alfred.sh`
- `scripts/install/stop_alfred.sh`
- `scripts/install/status_alfred.sh`
- `scripts/install/uninstall_alfred.sh`

## Install Flow

1. Run `install_alfred_platform.sh` with an explicit source mode to create the target directory structure and copy the Alfred app into `/opt/alfred/app`.
2. Run `configure_alfred.sh` to seed `/opt/alfred/config/config.yaml` if it does not already exist.
3. Review deployment profile, vault path, Python path, Node path, and runtime output locations in `config.yaml`.
4. Run `start_alfred.sh` to build Dashboard API and UI artefacts inside the package.
5. Run `status_alfred.sh` to confirm package health markers.

## Supported Installation Modes

The installer refuses to run unless a valid Alfred source is supplied explicitly. It never infers the source repository from the installer location.

Exactly three installation modes are supported:

1. Install from a Git repository:
   - `scripts/install/install_alfred_platform.sh --mode git --git-url <repo> [--git-ref <ref>]`
2. Install from a packaged release tarball:
   - `scripts/install/install_alfred_platform.sh --mode tarball --tarball /path/to/alfred-release.tar.gz`
3. Install from an explicitly supplied local source directory:
   - `scripts/install/install_alfred_platform.sh --mode local --source-dir /path/to/alfred-handbook`

The installer validates the Alfred project structure before copying. If validation fails, installation exits immediately with a clear error.

## Safety Guards

- The installer never infers the Alfred source from its own location.
- The installer validates the source contains the expected Alfred project structure.
- The installer refuses to recurse into the destination directory.
- The installer prevents self-copy loops, including cases where the install root is inside the source tree or the source tree is inside the install destination.
- The installer seeds configuration from the copied app tree, not from the location of the installer script that launched the process.

## Environment Discovery

- The installer performs environment discovery where practical before and after configuration.
- Alfred records a persistent environment inventory containing detected platform components, health, locations, dependencies, and recommended actions.
- Optional components do not block installation. Missing optional components are surfaced as next actions instead.
- Required core configuration is auto-populated only when discovery confidence is high.
- If discovery confidence is insufficient, Alfred marks the item `ACTION_REQUIRED` instead of guessing.

## Admin / Configuration

- Use the Admin / Configuration console under `CONTROL -> Operations` to review:
  - core configuration
  - vault
  - AI providers
  - knowledge sources
  - runtime
  - services
  - security
  - diagnostics
  - deployment actions
  - required actions
- Secrets are never displayed. Presence and configuration source are shown instead.
- Re-run discovery with:
  - `python build_environment_inventory.py`
  - `python build_operational_readiness.py`

## Safety Model

- The package is designed to sit alongside Hermes.
- It should not touch Telegram, Cloudflare, or the existing Hermes runtime.
- It should not assume ownership of the canonical vault unless explicitly configured.
- `uninstall_alfred.sh` removes Alfred application runtime only and preserves config and data.
