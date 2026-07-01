from executive.analyzers.knowledge import analyze

def test_executive_contracts():
    result = analyze(None)
    vault = result["vault"]

    assert isinstance(vault, dict)

    graph = vault["graph"]
    assert isinstance(graph, dict)
    assert "entity_count" in graph
    assert "edge_count" in graph
    assert "entities_by_type" in graph
    assert "edges" in graph
    assert isinstance(graph["edges"], list)
    assert isinstance(graph["entities_by_type"], dict)

    priorities = vault["priorities"]
    assert isinstance(priorities, dict)
    assert "priority_count" in priorities
    assert "top_priorities" in priorities
    assert isinstance(priorities["top_priorities"], list)

    work_queue = vault["work_queue"]
    assert isinstance(work_queue, dict)
    assert "total_actions" in work_queue
    assert "top_actions" in work_queue
    assert isinstance(work_queue["top_actions"], list)

    do_next = vault["do_next"]
    assert isinstance(do_next, dict)
    assert "total_actions" in do_next
    assert "top_10" in do_next
    assert isinstance(do_next["top_10"], list)

    executive_reasoning = vault["executive_reasoning"]
    assert isinstance(executive_reasoning, dict)
    assert "conclusion_count" in executive_reasoning
    assert "conclusions" in executive_reasoning
    assert isinstance(executive_reasoning["conclusions"], list)
