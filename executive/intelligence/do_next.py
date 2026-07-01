from collections import defaultdict


def _score(item):
    return item.get("score", 0)


def _dedupe(items):
    seen = set()
    out = []

    for i in items:
        key = i["title"].lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(i)

    return out


def build_do_next(vault):
    work_queue = vault.get("work_queue", {})
    priorities = vault.get("priorities", {})
    ownership = vault.get("ownership", {})
    risk = vault.get("risk", {})
    reasoning = vault.get("executive_reasoning", {})

    actions = []

    # 1. Work queue (primary signal)
    for a in work_queue.get("top_actions", []):
        actions.append({
            "title": a["title"],
            "action": a["action"],
            "score": a["score"] + 50,
            "source": "work_queue",
            "horizon": "THIS_WEEK",
        })

    # 2. Critical priorities
    for p in priorities.get("top_priorities", []):
        if p["priority"] == "CRITICAL":
            actions.append({
                "title": p["title"],
                "action": p.get("recommended_actions", ["Review"])[0],
                "score": p["priority_score"] + 60,
                "source": "priority",
                "horizon": "TODAY",
            })

    # 3. Ownership gaps
    for o in ownership.get("projects", []):
        if o["owner"] is None:
            actions.append({
                "title": o["project"],
                "action": "Assign accountable owner",
                "score": 140,
                "source": "ownership",
                "horizon": "TODAY",
            })

    # 4. High risk drivers
    for r in risk.get("high_risk", []):
        actions.append({
            "title": r["title"],
            "action": "Stabilise or review governance",
            "score": r["risk_score"],
            "source": "risk",
            "horizon": "THIS_WEEK",
        })

    # 5. Executive reasoning signals
    for c in reasoning.get("conclusions", []):
        actions.append({
            "title": c["headline"],
            "action": c["recommendation"],
            "score": 120,
            "source": "reasoning",
            "horizon": "STRATEGIC",
        })

    actions = _dedupe(actions)
    actions.sort(key=lambda x: x["score"], reverse=True)

    top10 = actions[:10]

    grouped = {
        "TODAY": [],
        "THIS_WEEK": [],
        "STRATEGIC": []
    }

    for a in top10:
        grouped[a["horizon"]].append(a)

    return {
        "total_actions": len(actions),
        "top_10": top10,
        "today": grouped["TODAY"],
        "this_week": grouped["THIS_WEEK"],
        "strategic": grouped["STRATEGIC"],
    }
