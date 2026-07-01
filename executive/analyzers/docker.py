from executive.parser import read

def analyze(evidence_root):
    containers_text = read("docker/containers.txt", evidence_root)

    containers = []
    running = 0
    exited = 0

    for line in containers_text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("NAMES"):
            continue

        containers.append(stripped)

        if " Up " in f" {stripped} ":
            running += 1

        if "Exited" in stripped:
            exited += 1

    return {
        "container_count": len(containers),
        "running": running,
        "exited": exited,
        "containers": containers,
    }
