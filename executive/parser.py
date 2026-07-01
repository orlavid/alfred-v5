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
        if parts and parts[0] == "●":
            parts = parts[1:]
        if len(parts) < 4:
            continue
        services.append({
            "name": parts[0],
            "load": parts[1],
            "active": parts[2],
            "state": parts[3],
        })
    return services

def parse_timers(root):
    timers = []
    for line in read("system/timers.txt", root).splitlines():
        if ".timer" not in line:
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        timers.append({
            "name": parts[-1],
            "raw": line,
        })
    return timers
