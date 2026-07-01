def calculate_score(metrics):
    score = 100

    score -= metrics["failed"] * 5

    score = max(0, min(score, 100))

    if score >= 95:
        status = "GREEN"
    elif score >= 80:
        status = "AMBER"
    else:
        status = "RED"

    return {
        "score": score,
        "status": status,
    }
