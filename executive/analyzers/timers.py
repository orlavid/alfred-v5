from executive.parser import parse_timers

def analyze(evidence_root):
    timers = parse_timers(evidence_root)

    return {
        "timer_count": len(timers),
        "timers": timers,
    }
