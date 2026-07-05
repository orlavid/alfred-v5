from pathlib import Path

from src.operations.config_registry import build_configuration_registry
from src.operations.production_validation import build_production_validation


def test_production_validation_blocks_demo_content(tmp_path: Path):
    output = tmp_path / "output"
    output.mkdir()
    (output / "Dashboard_Home.json").write_text('{"summary":"Barclays demo"}')

    registry = build_configuration_registry(tmp_path, output_dir=output, vault_path=tmp_path / "vault")
    report = build_production_validation(registry, output_dir=output)

    assert report.status == "FAIL"
    assert any(finding.forbidden_string == "Barclays" for finding in report.findings)


def test_production_validation_passes_without_forbidden_strings(tmp_path: Path):
    output = tmp_path / "output"
    output.mkdir()
    (output / "Dashboard_Home.json").write_text('{"summary":"No evidence found"}')

    registry = build_configuration_registry(tmp_path, output_dir=output, vault_path=tmp_path / "vault")
    report = build_production_validation(registry, output_dir=output)

    assert report.status == "PASS"
