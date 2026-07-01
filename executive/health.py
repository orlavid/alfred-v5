def platform_health(services):
    running = sum(1 for s in services if s["state"] == "running")
    failed = sum(1 for s in services if s["active"] == "failed")
    score = max(0, 100 - failed * 5)
    return {
        "running": running,
        "failed": failed,
        "score": score,
    }
