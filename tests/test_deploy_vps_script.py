from pathlib import Path


def test_deploy_vps_script_sequences_required_gates_and_rollback():
    content = Path("deploy_vps.sh").read_text()

    required = [
        'run_gate "pull GitHub" git pull --ff-only',
        'run_gate "install" "$ROOT_DIR/deploy_stage2.sh"',
        'run_gate "build" python3 "$ROOT_DIR/build_everything.py"',
        'run_gate "run tests" pytest',
        'run_gate "run Live Knowledge Certification" python3 "$ROOT_DIR/build_live_knowledge_certification.py"',
        'run_gate "run Executive Acceptance" "$ROOT_DIR/deploy_validation.sh"',
        'run_gate "start service" "$ROOT_DIR/scripts/install/start_alfred.sh"',
        'run_gate "smoke test" "$ROOT_DIR/scripts/install/status_alfred.sh"',
        'trap rollback_on_failure EXIT',
        '"$ROOT_DIR/deploy_rollback.sh"',
    ]

    for item in required:
        assert item in content

    assert "set -euo pipefail" in content
    assert 'ROLLBACK_TRIGGERED=0' in content
