from pathlib import Path


def test_deploy_vps_script_sequences_required_gates_and_rollback():
    content = Path("deploy_vps.sh").read_text()

    required = [
        'verify_git_deploy_state',
        'run_gate "pull GitHub" git pull --ff-only',
        'ensure_python_environment',
        'run_gate "build" "$VENV_PYTHON" "$ROOT_DIR/build_everything.py"',
        'run_gate "run tests" "$VENV_PYTHON" -m pytest',
        'run_gate "run Live Knowledge Certification" "$VENV_PYTHON" "$ROOT_DIR/build_live_knowledge_certification.py"',
        'build_release_bundle',
        'verify_remote_deploy_config',
        'prepare_remote_release',
        'run_remote_install',
        'run_remote_acceptance',
        'run_remote_start',
        'run_remote_smoke_test',
        'trap rollback_on_failure EXIT',
        "ssh -o BatchMode=yes",
        'if [[ -f deploy_rollback.sh ]]; then',
    ]

    for item in required:
        assert item in content

    assert "set -euo pipefail" in content
    assert 'ROLLBACK_TRIGGERED=0' in content
    assert 'require_command "$LOG_FILE" pytest' not in content
    assert 'python3 -m venv "$VENV_DIR"' in content
    assert '"$VENV_PYTHON" -m pip install -r "$ROOT_DIR/requirements-dev.txt"' in content
    assert '"$VENV_PYTHON" -m pip install pytest' not in content
    assert 'missing required deployment target: ALFRED_REMOTE_HOST' in content
    assert 'unsupported Git state: detached HEAD' in content
    assert 'unsupported Git state: working tree is dirty' in content
    assert "has no upstream" in content
    assert 'PASS: Git deployment state is supported on branch' in content
    assert 'missing required deployment target: ALFRED_REMOTE_HOST' in content
    assert 'local remote_command="$2"' in content
    assert 'ssh -o BatchMode=yes "$REMOTE_TARGET" "$remote_command"' in content
    assert 'BUILD_COMMIT="$(git -C "$ROOT_DIR" rev-parse HEAD)"' in content
    assert 'BUILD_TREE_STATE="$([ -z "$(git -C "$ROOT_DIR" status --short)" ] && echo clean || echo dirty)"' in content
    assert 'ALFRED_BUILD_COMMIT=$(shell_quote "$BUILD_COMMIT")' in content
    assert 'ALFRED_BUILD_TREE_STATE=$(shell_quote "$BUILD_TREE_STATE")' in content
    assert 'remote_run_script() {' in content
    assert 'ssh -o BatchMode=yes "$REMOTE_TARGET" bash -se <"$script_file"' in content
    assert 'remote_run_script "extract deployment bundle on VPS"' in content
    assert 'rm -rf $(shell_quote "$REMOTE_RELEASE_DIR")' in content
    assert 'mkdir -p $(shell_quote "$REMOTE_RELEASE_DIR")' in content
    assert 'tar -xzf $(shell_quote "$REMOTE_BUNDLE_PATH") -C $(shell_quote "$REMOTE_RELEASE_DIR")' in content
    assert 'ALFRED_INSTALL_ROOT="$REMOTE_INSTALL_ROOT"' not in content
    assert "run_gate \"install\" \"$ROOT_DIR/deploy_stage2.sh\"" not in content
    assert "run_gate \"start service\" \"$ROOT_DIR/scripts/install/start_alfred.sh\"" not in content
    assert "run_gate \"smoke test\" \"$ROOT_DIR/scripts/install/status_alfred.sh\"" not in content
