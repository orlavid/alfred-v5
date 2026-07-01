from executive.scoring import calculate_score

def platform_health(services):
    metrics = {
        "running": sum(
            1 for s in services
            if s["state"] == "running"
        ),
        "failed": sum(
            1
            for s in services
            if (
                s["active"] == "failed"
                or s["state"] == "failed"
                or s["load"] == "failed"
            )
        ),
    }

    metrics.update(calculate_score(metrics))

    return metrics
