from executive.analyzers import systemd, timers

def execute(evidence_root):
    systemd_result = systemd.analyze(evidence_root)
    timers_result = timers.analyze(evidence_root)

    return {
        "health": systemd_result["health"],
        "risks": systemd_result["risks"],
        "timers": timers_result,
    }
