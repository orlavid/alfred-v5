from pathlib import Path


def test_gate3_deployment_files_exist():
    expected = [
        Path("docs/deployment/VPS_DEPLOYMENT_PLAN.md"),
        Path("docs/deployment/EXECUTIVE_ACCEPTANCE_TESTS.md"),
        Path("deploy_stage1.sh"),
        Path("deploy_stage2.sh"),
        Path("deploy_validation.sh"),
        Path("deploy_rollback.sh"),
        Path("scripts/install/deploy_common.sh"),
        Path("scripts/vps/verify_sacred_assets.sh"),
        Path("scripts/vps/check_capacity_growth.sh"),
        Path("scripts/vps/certify_live_knowledge.sh"),
    ]
    for path in expected:
        assert path.exists(), path


def test_gate3_plan_contains_required_sections():
    content = Path("docs/deployment/VPS_DEPLOYMENT_PLAN.md").read_text()
    required = [
        "## Preconditions",
        "## Configuration Migration",
        "## Sacred Asset Verification",
        "## Installation Order",
        "## Knowledge Certification",
        "## Executive Acceptance Tests",
        "## Capacity And Growth Assessment",
        "## Validation Gates",
        "## Rollback Plan",
        "## Cutover Plan",
        "## Risks",
        "## Estimated Downtime",
        "zero",
        "Hostinger snapshot",
        "Cloudflare config present",
    ]
    for item in required:
        assert item in content


def test_gate3_scripts_are_fail_fast_and_non_destructive():
    for path in [
        Path("deploy_stage1.sh"),
        Path("deploy_stage2.sh"),
        Path("deploy_validation.sh"),
        Path("deploy_rollback.sh"),
        Path("scripts/vps/verify_sacred_assets.sh"),
        Path("scripts/vps/check_capacity_growth.sh"),
        Path("scripts/vps/certify_live_knowledge.sh"),
    ]:
        content = path.read_text()
        assert "set -euo pipefail" in content
        assert "deploy_common.sh" in content
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
        "build_ask_alfred.py",
        "certify_live_knowledge.sh",
        "npm run build",
        "Overall Health: GREEN",
    ]
    for item in required:
        assert item in content


def test_gate3_supporting_scripts_cover_config_and_acceptance_hardening():
    stage2 = Path("deploy_stage2.sh").read_text()
    cert = Path("scripts/vps/certify_live_knowledge.sh").read_text()
    sacred = Path("scripts/vps/verify_sacred_assets.sh").read_text()
    capacity = Path("scripts/vps/check_capacity_growth.sh").read_text()
    acceptance = Path("docs/deployment/EXECUTIVE_ACCEPTANCE_TESTS.md").read_text()

    assert "ALFRED_OBSIDIAN_VAULT" in stage2
    assert "key_env_var" in stage2
    assert "certify live knowledge" in Path("deploy_validation.sh").read_text()
    assert "objectives" in cert
    assert "projects" in cert
    assert "knowledge_graph_nodes" in cert
    assert "HOSTINGER_SNAPSHOT_CONFIRMED" in sacred
    assert "Cloudflare" in sacred or "cloudflared" in sacred
    assert "disk free" in capacity
    assert "inode free" in capacity
    assert "What should I focus on today?" in acceptance
    assert "Prepare me for Barclays." in acceptance
