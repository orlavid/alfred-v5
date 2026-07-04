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

1. Run `install_alfred_platform.sh` to create the target directory structure and copy the Alfred app into `/opt/alfred/app`.
2. Run `configure_alfred.sh` to seed `/opt/alfred/config/config.yaml` if it does not already exist.
3. Review deployment profile, vault path, Python path, Node path, and runtime output locations in `config.yaml`.
4. Run `start_alfred.sh` to build Dashboard API and UI artefacts inside the package.
5. Run `status_alfred.sh` to confirm package health markers.

## Safety Model

- The package is designed to sit alongside Hermes.
- It should not touch Telegram, Cloudflare, or the existing Hermes runtime.
- It should not assume ownership of the canonical vault unless explicitly configured.
- `uninstall_alfred.sh` removes Alfred application runtime only and preserves config and data.
