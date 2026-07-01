from dataclasses import dataclass

@dataclass
class ProjectInsight:
    title: str
    path: str
    linked_entities: int
    status: str
    recommendation: str

def analyze_projects(entities, graph):
    project_entities = [e for e in entities if e.type == "project"]

    linked_counts = {}

    for edge in graph["edges"]:
        linked_counts[edge["source"]] = linked_counts.get(edge["source"], 0) + 1
        linked_counts[edge["target"]] = linked_counts.get(edge["target"], 0) + 1

    insights = []

    for project in project_entities:
        linked = linked_counts.get(project.id, 0)

        if linked == 0:
            status = "AT RISK"
            recommendation = "Project has no graph linkage; review whether it is current, duplicated, or missing relationships."
        elif linked < 3:
            status = "WATCH"
            recommendation = "Project has limited supporting evidence; review owner, objective, decisions and dependencies."
        else:
            status = "SUPPORTED"
            recommendation = "Project has supporting vault evidence."

        insights.append(ProjectInsight(
            title=project.title,
            path=project.path,
            linked_entities=linked,
            status=status,
            recommendation=recommendation,
        ))

    return {
        "project_count": len(project_entities),
        "at_risk": sum(1 for i in insights if i.status == "AT RISK"),
        "watch": sum(1 for i in insights if i.status == "WATCH"),
        "supported": sum(1 for i in insights if i.status == "SUPPORTED"),
        "insights": insights,
    }
