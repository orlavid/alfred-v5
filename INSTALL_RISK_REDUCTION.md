# Alfred Install Risk Reduction Checklist

## Before installing on another machine

Required:
- Git installed
- Python 3 installed
- Node/npm installed
- Network access to GitHub
- SSH access to target VPS if deploying remotely
- Vault path known
- Required environment variables documented

## Release integrity

Before install:
- Working tree clean
- Release tag exists
- BUILD_INFO generated
- requirements.txt present
- requirements-dev.txt present
- package-lock.json present
- .deploy/ ignored

## Installation must not be accepted unless all are GREEN

- Build
- Tests
- Production Runtime Certification
- Knowledge Certification
- Operational Readiness
- Smoke Test

## Standard deployment variables

export ALFRED_REMOTE_HOST=187.124.208.91
export ALFRED_REMOTE_USER=root
export ALFRED_OBSIDIAN_VAULT=/docker/obsidian-vault
export ALFRED_REMOTE_INSTALL_ROOT=/opt/alfred
