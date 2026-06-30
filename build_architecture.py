#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).parent
ARCH = ROOT / "architecture"
ARCH.mkdir(exist_ok=True)

docs = {
    "00 Vision.md": "src.architecture.vision",
    "01 Principles.md": "src.architecture.principles",
    "02 System Architecture.md": "src.architecture.system",
    "03 Component Specifications.md": "src.architecture.components",
    "04 Capability Model.md": "src.architecture.capabilities",
    "05 Agent Organisation.md": "src.architecture.agents",
    "06 Information Model.md": "src.architecture.information",
    "07 Security & Governance.md": "src.architecture.governance",
    "08 Build Roadmap.md": "src.architecture.roadmap",
    "10 Architectural Decision Records.md": "src.architecture.adrs",
}

for filename, module_name in docs.items():
    module = __import__(module_name, fromlist=["render"])
    (ARCH / filename).write_text(module.render().strip() + "\n")

blueprint = ARCH / "Alfred Architecture Blueprint.md"

with blueprint.open("w") as out:
    out.write("# Alfred Architecture Blueprint\n\n")
    for filename in sorted(docs):
        out.write(f"\n---\n\n# {filename}\n\n")
        out.write((ARCH / filename).read_text())

print("Architecture generated.")
