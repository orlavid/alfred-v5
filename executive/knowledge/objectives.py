from dataclasses import dataclass

@dataclass
class ObjectiveInsight:
    title: str
    path: str
    linked_entities: int
    status: str
    recommendation: str

def analyze_objectives(entities, graph):
    objective_entities = [e for e in entities if e.type == "objective"]

    linked_counts = {}

    for edge in graph["edges"]:
        linked_counts[edge["source"]] = linked_counts.get(edge["source"], 0) + 1
        linked_counts[edge["target"]] = linked_counts.get(edge["target"], 0) + 1

    insights = []

    for objective in objective_entities:
        linked = linked_counts.get(objective.id, 0)

        if linked == 0:
            status = "AT RISK"
            recommendation = "Review objective linkage; no supporting projects, decisions, people or evidence are connected."
        elif linked < 3:
            status = "WATCH"
            recommendation = "Objective has limited supporting evidence; review whether it is actively managed."
        else:
            status = "SUPPORTED"
            recommendation = "Objective has supporting vault evidence."

        insights.append(ObjectiveInsight(
            title=objective.title,
            path=objective.path,
            linked_entities=linked,
            status=status,
            recommendation=recommendation,
        ))

    return {
        "objective_count": len(objective_entities),
        "at_risk": sum(1 for i in insights if i.status == "AT RISK"),
        "watch": sum(1 for i in insights if i.status == "WATCH"),
        "supported": sum(1 for i in insights if i.status == "SUPPORTED"),
        "insights": insights,
    }
