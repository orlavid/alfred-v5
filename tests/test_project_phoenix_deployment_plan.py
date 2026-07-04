from pathlib import Path


def test_gate3_deployment_files_exist():
    expected = [
        Path("docs/deployment/VPS_DEPLOYMENT_PLAN.md"),
        Path("deploy_stage1.sh"),
        Path("deploy_stage2.sh"),
        Path("deploy_validation.sh"),
        Path("deploy_rollback.sh"),
        Path("scripts/install/deploy_common.sh"),
    ]
    for path in expected:
        assert path.exists(), path


def test_gate3_plan_contains_required_sections():
    content = Path("docs/deployment/VPS_DEPLOYMENT_PLAN.md").read_text()
    required = [
        "## Preconditions",
        "## Installation Order",
        "## Validation Gates",
        "## Rollback Plan",
        "## Cutover Plan",
        "## Risks",
        "## Estimated Downtime",
        "zero",
    ]
    for item in required:
        assert item in content


def test_gate3_scripts_are_fail_fast_and_non_destructive():
    for path in [
        Path("deploy_stage1.sh"),
        Path("deploy_stage2.sh"),
        Path("deploy_validation.sh"),
        Path("deploy_rollback.sh"),
    ]:
        content = path.read_text()
        assert "set -euo pipefail" in content
        assert "source \"$ROOT_DIR/scripts/install/deploy_common.sh\"" in content
        assert "rm -rf /docker/obsidian-vault" not in content
        assert "systemctl stop hermes-telegram.service" not in content
        assert "cloudflared" not in content or "Do not change Cloudflare" in content


def test_gate3_validation_script_checks_required_outputs():
    content = Path("deploy_validation.sh").read_text()
    required = [
        "build_dashboard_api.py",
        "build_executive_state.py",
        "build_executive_pipeline.py",
        "build_daily_brief.py",
        "build_operational_readiness.py",
        "npm run build",
        "Overall Health: GREEN",
    ]
    for item in required:
        assert item in content
