# Post Install Validation

Use this checklist after installing Alfred into `/opt/alfred`.

## Required Validation

- UI starts
- Dashboard loads
- ExecutiveState builds
- Pipeline succeeds
- Daily Brief generated
- Dashboard API generated
- Operational Readiness green
- Environment inventory generated
- Admin / Configuration populated

## Suggested Commands

```bash
/opt/alfred/app/.venv/bin/python /opt/alfred/app/build_dashboard_api.py
/opt/alfred/app/.venv/bin/python /opt/alfred/app/build_executive_state.py
/opt/alfred/app/.venv/bin/python /opt/alfred/app/build_executive_pipeline.py
/opt/alfred/app/.venv/bin/python /opt/alfred/app/build_daily_brief.py
/opt/alfred/app/.venv/bin/python /opt/alfred/app/build_environment_inventory.py
/opt/alfred/app/.venv/bin/python /opt/alfred/app/build_operational_readiness.py
cd /opt/alfred/app && npm run build
/opt/alfred/app/scripts/install/status_alfred.sh
```

## Validation Outcomes

### UI starts

- `dist/index.html` exists after `npm run build`.

### Dashboard loads

- `output/Dashboard_Home.json` is regenerated successfully.

### ExecutiveState builds

- `output/ExecutiveState_Summary.md` exists and is current.

### Pipeline succeeds

- `output/Executive_Pipeline_Report.md` reports successful stage completion.

### Daily Brief generated

- `output/Daily_Brief.md` exists.

### Dashboard API generated

- `output/Dashboard_Home.json` exists.

### Environment inventory generated

- `output/Environment_Inventory.json` exists.
- `output/Environment_Inventory.md` exists.
- `/opt/alfred/config/config.yaml` contains a `detected_environment` section.

### Operational Readiness green

- `output/Operational_Readiness_Report.md` exists.
- `status_alfred.sh` reports the expected files and services.
- Remaining warnings should be understood and acceptable for the chosen deployment profile.

### Admin / Configuration populated

- Admin / Configuration shows discovered platform components and required actions.
- Secrets are not displayed.
- Operational actions reference existing Alfred commands.

## Re-run Discovery

```bash
/opt/alfred/app/.venv/bin/python /opt/alfred/app/build_environment_inventory.py
/opt/alfred/app/.venv/bin/python /opt/alfred/app/build_operational_readiness.py
```
