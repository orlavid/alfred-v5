from importlib import import_module
from pathlib import Path

ANALYZERS = [
    "systemd",
    "timers",
    "docker",
    "knowledge",
]

def execute(evidence_root: Path, *, vault_root: Path | None = None):
    result = {}

    for name in ANALYZERS:
        module = import_module(f"executive.analyzers.{name}")
        if name == "knowledge":
            output = module.analyze(evidence_root, vault_root=vault_root)
        else:
            output = module.analyze(evidence_root)

        if isinstance(output, dict):
            result[name] = output

            if name == "systemd":
                result["health"] = output["health"]
                result["risks"] = output["risks"]

    return result
