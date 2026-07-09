from collections import defaultdict
import re

EXECUTIVE_TYPES = {"project", "objective", "company", "person", "decision", "open_loop"}
CANONICAL_EXECUTIVE_PREFIXES = (
    "02 People/",
    "03 Projects/",
    "04 Companies/",
    "04 Decisions/",
    "05 Meetings/",
    "06 Risks/",
    "07 Open Loops/",
    "08 Follow Ups/",
    "08 Follow-Ups/",
    "09 Objectives/",
    "09 Governance/",
    "10 Briefings/",
)
NOISY_ARTIFACT_PREFIXES = (
    "00 Inbox/Captures/",
    "07 AI Memory/Entities/",
)
DATE_TOKEN_RE = re.compile(r"(20\d{6}|\d{4}-\d{2}-\d{2})")

def _index_by_title(items, title_key="title"):
    return {
        item.get(title_key): item
        for item in items
        if isinstance(item, dict) and item.get(title_key)
    }

def _impact_index(impact):
    return {
        item["title"]: item.get("impact", 0)
        for item in impact
        if item.get("title")
    }

def _dependency_index(dependencies):
    return {
        item["title"]: item
        for item in dependencies.get("top_dependencies", [])
        if item.get("title")
    }

def _risk_index(risk):
    return {
        item["title"]: item
        for item in risk.get("all", [])
        if item.get("title")
    }

def _ownership_index(ownership):
    return {
        item["project"]: item
        for item in ownership.get("projects", [])
        if item.get("project")
    }

def _project_index(projects):
    return {
        item.title: item
        for item in projects.get("insights", [])
        if getattr(item, "title", None)
    }

def _company_index(companies):
    return {
        item.title: item
        for item in companies.get("insights", [])
        if getattr(item, "title", None)
    }

def _person_index(people):
    return {
        item.title: item
        for item in people.get("insights", [])
        if getattr(item, "title", None)
    }

def _decision_index(decisions):
    return _index_by_title(decisions.get("top_decisions", []))

def _entity_index(entities):
    return {
        entity.title: entity
        for entity in entities
        if getattr(entity, "title", None)
    }

def _entity_neighbour_counts(graph, entities):
    lookup = {e.id: e for e in entities}
    neighbours = defaultdict(set)

    for edge in graph.get("edges", []):
        neighbours[edge["source"]].add(edge["target"])
        neighbours[edge["target"]].add(edge["source"])

    counts = {}

    for entity in entities:
        linked = [
            lookup[n]
            for n in neighbours.get(entity.id, set())
            if n in lookup
        ]
        by_type = defaultdict(int)
        for item in linked:
            by_type[item.type] += 1

        counts[entity.title] = {
            "connections": len(linked),
            "linked_types": dict(by_type),
        }

    return counts

def _score_entity(title, entity_type, indexes, neighbour_counts):
    impact = indexes["impact"].get(title, 0)
    dependency = indexes["dependencies"].get(title, {})
    risk = indexes["risk"].get(title, {})
    ownership = indexes["ownership"].get(title, {})
    project = indexes["projects"].get(title)
    company = indexes["companies"].get(title)
    person = indexes["people"].get(title)
    decision = indexes["decisions"].get(title)
    neighbours = neighbour_counts.get(title, {})
    entity = indexes["entities"].get(title)
    entity_path = getattr(entity, "path", "")
    evidence_paths = list(getattr(entity, "evidence_paths", ()) or ((entity_path,) if entity_path else ()))
    contract_status = getattr(entity, "status", None)
    contract_owner = getattr(entity, "owner", None)
    contract_priority = getattr(entity, "priority", None)
    contract_risk_level = getattr(entity, "risk_level", None)
    contract_due_date = getattr(entity, "due_date", None)
    contract_last_activity = getattr(entity, "last_activity", None)
    contract_related_objectives = tuple(getattr(entity, "related_objectives", ()) or ())
    contract_related_people = tuple(getattr(entity, "related_people", ()) or ())

    score = 0
    reasons = []
    recommended_actions = []

    if impact:
        addition = min(35, impact // 100)
        score += addition
        reasons.append(f"High executive impact score ({impact})")

    if dependency:
        bottleneck = dependency.get("bottleneck", 0)
        addition = min(30, bottleneck // 20)
        score += addition
        reasons.append(f"Dependency bottleneck score {bottleneck}")

    if risk:
        risk_score = risk.get("risk_score", 0)
        addition = min(40, risk_score // 2)
        score += addition
        reasons.append(f"Risk score {risk_score}")
        for reason in risk.get("reasons", []):
            reasons.append(reason)

    if entity_type == "project":
        if contract_owner is None and ownership and not ownership.get("owner"):
            score += 20
            reasons.append("No inferred project owner")
            recommended_actions.append("Assign an accountable owner")
        elif contract_owner is None and ownership and ownership.get("confidence", 0) < 0.5:
            score += 10
            reasons.append("Ownership is inferred with low confidence")
            recommended_actions.append("Confirm the real accountable owner")

        if project:
            if project.status == "AT RISK":
                score += 25
                reasons.append("Project intelligence status is AT RISK")
                recommended_actions.append("Review project governance and linkage")
            elif project.status == "WATCH":
                score += 10
                reasons.append("Project intelligence status is WATCH")
                recommended_actions.append("Check whether the project has enough supporting evidence")

    if entity_type == "company" and company:
        if company.status == "CRITICAL":
            score += 25
            reasons.append("Company intelligence status is CRITICAL")
            recommended_actions.append("Validate ownership, dependency and supplier governance")
        elif company.status == "IMPORTANT":
            score += 15
            reasons.append("Company intelligence status is IMPORTANT")

    if entity_type == "person" and person:
        if person.risk == "CRITICAL":
            score += 25
            reasons.append("Person has critical influence concentration")
            recommended_actions.append("Review succession and knowledge concentration risk")
        elif person.risk == "HIGH":
            score += 15
            reasons.append("Person has high executive influence")

    if entity_type == "decision" and decision:
        if decision.get("projects", 0) == 0 and decision.get("objectives", 0) == 0:
            score += 15
            reasons.append("Decision is weakly linked to projects and objectives")
            recommended_actions.append("Link decision to affected projects, objectives and owners")

    if entity is not None and _is_current_executive_entity(entity):
        score += 12
        reasons.append("Current executive source note")

    if entity is not None and _is_recent_decision(entity, entity_type):
        score += 10
        reasons.append("Recent executive decision")

    if entity is not None and _is_noisy_capture_artifact(entity):
        score -= 60
        reasons.append("Historical capture or AI-memory artefact")
        recommended_actions.append("Review whether the artefact should be archived, linked, or excluded from executive prioritisation")

    linked_types = neighbours.get("linked_types", {})

    if entity_type in ("project", "objective") and linked_types.get("person", 0) == 0 and not contract_related_people:
        score += 10
        reasons.append("No person relationship detected")

    if entity_type == "project" and linked_types.get("objective", 0) == 0 and not contract_related_objectives:
        score += 10
        reasons.append("No objective relationship detected")

    if not recommended_actions:
        recommended_actions.append("Review and confirm executive treatment")

    score = max(0, min(score, 100))

    if score >= 80:
        priority = "CRITICAL"
    elif score >= 60:
        priority = "HIGH"
    elif score >= 40:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "title": title,
        "type": entity_type,
        "priority_score": score,
        "priority": priority,
        "reasons": list(dict.fromkeys(reasons))[:8],
        "recommended_actions": list(dict.fromkeys(recommended_actions))[:5],
        "next_step": list(dict.fromkeys(recommended_actions))[0],
        "why_now": list(dict.fromkeys(reasons))[:3],
        "status": contract_status or _entity_status(entity_type, project, company, person, decision, risk),
        "owner": _normalise_owner(contract_owner) or (_normalise_owner(ownership.get("owner")) if ownership else None),
        "deadline_or_recency": contract_due_date or contract_last_activity or _entity_date_signal(entity, entity_type),
        "evidence_paths": evidence_paths[:5],
        "provider": getattr(entity, "provider", entity_type),
        "confidence": getattr(entity, "confidence", "MEDIUM"),
        "contract_entity_id": getattr(entity, "entity_id", getattr(entity, "id", title)),
        "contract_priority": contract_priority,
        "contract_risk_level": contract_risk_level,
        "missing_fields": list(getattr(entity, "missing_fields", ()) or ()),
    }

def build_priorities(vault, entities, graph, canonical_entities=None):
    scoring_entities = list(canonical_entities) if canonical_entities is not None else list(entities)
    indexes = {
        "impact": _impact_index(vault.get("impact", [])),
        "dependencies": _dependency_index(vault.get("dependency_analysis", {})),
        "risk": _risk_index(vault.get("risk", {})),
        "ownership": _ownership_index(vault.get("ownership", {})),
        "projects": _project_index(vault.get("projects", {})),
        "companies": _company_index(vault.get("companies", {})),
        "people": _person_index(vault.get("people", {})),
        "decisions": _decision_index(vault.get("decisions", {})),
        "entities": _entity_index(scoring_entities),
    }

    neighbour_counts = _entity_neighbour_counts(graph, entities)

    candidate_titles = set()
    candidate_titles.update(indexes["impact"].keys())
    candidate_titles.update(indexes["dependencies"].keys())
    candidate_titles.update(indexes["risk"].keys())
    candidate_titles.update(indexes["ownership"].keys())
    candidate_titles.update(indexes["projects"].keys())
    candidate_titles.update(indexes["companies"].keys())
    candidate_titles.update(indexes["people"].keys())
    candidate_titles.update(indexes["decisions"].keys())

    title_to_type = {}
    for entity in scoring_entities:
        if entity.type in EXECUTIVE_TYPES:
            title_to_type.setdefault(entity.title, entity.type)

    priorities = []

    for title in candidate_titles:
        entity_type = title_to_type.get(title)
        if not entity_type:
            continue

        item = _score_entity(title, entity_type, indexes, neighbour_counts)

        if item["priority_score"] > 0:
            priorities.append(item)

    priorities.sort(key=lambda x: x["priority_score"], reverse=True)

    return {
        "priority_count": len(priorities),
        "critical": sum(1 for x in priorities if x["priority"] == "CRITICAL"),
        "high": sum(1 for x in priorities if x["priority"] == "HIGH"),
        "medium": sum(1 for x in priorities if x["priority"] == "MEDIUM"),
        "low": sum(1 for x in priorities if x["priority"] == "LOW"),
        "top_priorities": priorities[:50],
    }


def _is_current_executive_entity(entity):
    path = getattr(entity, "path", "").replace("\\", "/")
    return any(path.startswith(prefix) for prefix in CANONICAL_EXECUTIVE_PREFIXES)


def _is_noisy_capture_artifact(entity):
    path = getattr(entity, "path", "").replace("\\", "/")
    title = getattr(entity, "title", "").lower()
    if any(path.startswith(prefix) for prefix in NOISY_ARTIFACT_PREFIXES):
        return True
    if title.startswith("historical capture"):
        return True
    if title.startswith("capture - "):
        return True
    return False


def _is_recent_decision(entity, entity_type):
    if entity_type != "decision":
        return False
    title = getattr(entity, "title", "")
    path = getattr(entity, "path", "")
    token = DATE_TOKEN_RE.search(f"{title} {path}")
    if token is None:
        return False
    value = token.group(1)
    if len(value) == 8 and value.isdigit():
        year = int(value[:4])
    else:
        year = int(value[:4])
    return year >= 2025


def _entity_status(entity_type, project, company, person, decision, risk):
    if entity_type == "project" and project is not None:
        return project.status
    if entity_type == "company" and company is not None:
        return company.status
    if entity_type == "person" and person is not None:
        return person.risk
    if entity_type == "decision" and decision is not None:
        return "RECENT" if decision.get("title") else "ACTIVE"
    if risk:
        return f"RISK {risk.get('risk_score', 0)}"
    return "ACTIVE"


def _normalise_owner(value):
    if value in {None, "", "Unknown", "None", "Not mentioned"}:
        return None
    return value


def _entity_date_signal(entity, entity_type):
    title = getattr(entity, "title", "")
    path = getattr(entity, "path", "")
    token = DATE_TOKEN_RE.search(f"{title} {path}")
    if token is None:
        return None
    label = "recent decision signal" if entity_type == "decision" else "dated evidence signal"
    return f"{label}: {token.group(1)}"
