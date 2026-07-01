from importlib import import_module
from pathlib import Path

ANALYZERS = [
    "systemd",
    "timers",
]

def execute(evidence_root: Path):
    result = {}

    for name in ANALYZERS:
        module = import_module(f"executive.analyzers.{name}")
        output = module.analyze(evidence_root)

        if isinstance(output, dict):
            result[name] = output

            if name == "systemd":
                result["health"] = output["health"]
                result["risks"] = output["risks"]

    return result
