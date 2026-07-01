from pathlib import Path

def read(rel, root):
    p = Path(root) / rel
    if not p.exists():
        return ""
    return p.read_text(errors="ignore")

def parse_services(root):
    services = []
    for line in read("system/services.txt", root).splitlines():
        if ".service" not in line:
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        services.append({
            "name": parts[0],
            "load": parts[1],
            "active": parts[2],
            "state": parts[3],
        })
    return services
