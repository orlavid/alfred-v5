import { MemoryRouter, Route, Routes } from "react-router-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import { DecisionsPage } from "@/pages/DecisionsPage";
import { DecisionDetailPage } from "@/pages/DecisionDetailPage";
import type { DashboardPayload } from "@/types";

const payload: DashboardPayload = {
  burning_fires: [],
  plan_today: [],
  next_best_action: {
    priority: "HIGH",
    action: "Resolve decision backlog.",
    why_it_matters: "Projects depend on active decisions.",
    confidence: "HIGH",
    origin: "intent",
    source_notes: ["04 Decisions/Decision 1.md"],
    provider: "executive_intent",
  },
  operating_picture: {
    overall_health: "AMBER",
    confidence: "HIGH",
    meeting_focus: "No active meeting identified.",
    followup_pressure: { overdue: 0, due_today: 0, high_priority: 0 },
    open_loop_pressure: { critical: 0, waiting_for: 0, missing_owners: 0 },
    summary: [],
  },
  navigation_priorities: [],
  interruption_policy: { level: "filter", rule: "Only interrupt for priority issues." },
  objectives: { health: { total: 0, supported: 0, at_risk: 0, watch: 0 }, items: [], summary: [] },
  projects: { health: { total: 0, supported: 0, at_risk: 0, watch: 0 }, items: [], summary: [] },
  decisions: {
    counts: { total: 2, defined_status: 1, owner_defined: 1, source_notes: 2 },
    items: [
      {
        decision_id: "dec-1",
        title: "Decision 1",
        source_path: "04 Decisions/Decision 1.md",
        source_entity_id: "decision-1",
        route: "/decisions/dec-1",
        status: "OPEN",
        owner: "Jane Smith",
        decision_date: "2026-07-10",
        related_project_count: 1,
        related_objective_count: 1,
        related_people_count: 1,
        evidence_confidence: "HIGH",
        rationale: "Approval for Project Phoenix.",
        missing_fields: [],
        importance: 140,
      },
      {
        decision_id: "dec-2",
        title: "Decision 2",
        source_path: "04 Decisions/Decision 2.md",
        source_entity_id: "decision-2",
        route: "/decisions/dec-2",
        status: "Not defined",
        owner: "Not defined",
        decision_date: "Not defined",
        related_project_count: 0,
        related_objective_count: 0,
        related_people_count: 0,
        evidence_confidence: "LOW",
        rationale: "No rationale found in the source evidence.",
        missing_fields: ["Accountable owner is not defined."],
        importance: 10,
      },
    ],
    details: {
      "dec-1": {
        decision_id: "dec-1",
        route: "/decisions/dec-1",
        title: "Decision 1",
        source_entity_id: "decision-1",
        source_path: "04 Decisions/Decision 1.md",
        decision_date: "2026-07-10",
        current_status: "OPEN",
        owner: "Jane Smith",
        importance: 140,
        evidence_confidence: "HIGH",
        rationale: "Approval for Project Phoenix.",
        related_projects: [{ title: "Project Phoenix", path: "03 Projects/Project Phoenix.md", reason: "Connected in canonical executive state.", route: "/projects/proj-1" }],
        related_objectives: [{ title: "Operational Governance", path: "09 Governance/Objectives/2026 Executive Objectives.md", reason: "Connected in canonical executive state.", route: "/objectives/obj-1" }],
        related_people: [{ title: "Jane Smith", path: "02 People/Jane Smith.md", reason: "Connected to the objective through the executive knowledge graph.", route: "/people" }],
        related_companies: [],
        related_work_items: [],
        relevant_meetings: [],
        evidence_sources: [{ label: "Decision 1", path: "04 Decisions/Decision 1.md", reason: "Canonical objective evidence source." }],
        recent_changes: ["Last meaningful activity recorded on 2026-07-10."],
        missing_information: [],
        stale_evidence: false,
        source_entities: ["decision-1"],
        source_work_items: [],
        provenance: { decision: ["04 Decisions/Decision 1.md"] },
      },
    },
    summary: [],
  },
  followups: {
    counts: { total: 0, overdue: 0, due_today: 0, due_this_week: 0, waiting_on_others: 0, high_priority: 0 },
    items: [],
    summary: [],
    recommendations: [],
  },
  open_loops: {
    counts: { total: 0, critical: 0, waiting_for: 0, stalled_projects: 0, missing_decisions: 0, missing_owners: 0 },
    items: [],
    summary: [],
    recommended_actions: [],
  },
  meetings: {
    subject: "No active meeting identified.",
    meeting_purpose: [],
    executive_summary: [],
    relationship_history: [],
    related_people: [],
    related_projects: [],
    related_companies: [],
    related_objectives: [],
    related_decisions: [],
    risks: [],
    commercial_issues: [],
    recent_changes: [],
    open_loops: [],
    follow_ups: [],
    dependencies: [],
    recommended_discussion: [],
    recommended_questions: [],
    recommended_decisions: [],
    evidence_references: [],
    confidence: "LOW",
  },
  board: { summary: [], members: [], weekly_meeting: [], monthly_meeting: [], standing_agenda: [] },
  ask_alfred: { questions: [], responses: [] },
  daily_brief: {
    executive_health: [],
    overnight_changes: [],
    top_three_priorities: [],
    meetings_requiring_preparation: [],
    followups_due_today: [],
    open_loops_blocking_progress: [],
    risks_escalating: [],
    decisions_awaiting_you: [],
    recommended_agenda: [],
    one_page_executive_summary: [],
    confidence: "HIGH",
  },
  knowledge: { summary: [], entity_counts: {}, graph: { node_count: 0, edge_count: 0, top_nodes: [] } },
  admin_configuration: {
    overview: { environment_score: 100, overall_health: "GREEN", architecture_rule: "", summary_lines: [] },
    sections: {
      core_configuration: [],
      vault: [],
      ai_providers: [],
      knowledge_sources: [],
      runtime: [],
      services: [],
      security: [],
      diagnostics: [],
      deployment: [],
      required_actions: [],
    },
    auto_configured: {},
    doctor_summary: { environment_score: 100, healthy: [], warnings: [], disabled: [], recommended_actions: [], summary_lines: [] },
    actions: [],
  },
  generated_from: {
    meeting_subject: "",
    runtime_model: "ExecutiveState",
    production_mode: true,
    sources: ["ExecutiveState"],
    confidence: "HIGH",
  },
};

test("decisions page supports filtering and drill-through", () => {
  render(
    <MemoryRouter initialEntries={["/decisions"]}>
      <Routes>
        <Route path="/decisions" element={<DecisionsPage data={payload} />} />
      </Routes>
    </MemoryRouter>,
  );

  expect(screen.getByText("Decision 1")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Search"), { target: { value: "Decision 2" } });
  expect(screen.queryByText("Decision 1")).not.toBeInTheDocument();
  expect(screen.getByText("Decision 2")).toBeInTheDocument();
});

test("decision detail route renders the workspace", () => {
  render(
    <MemoryRouter initialEntries={["/decisions/dec-1"]}>
      <Routes>
        <Route path="/decisions/:decisionId" element={<DecisionDetailPage data={payload} />} />
      </Routes>
    </MemoryRouter>,
  );

  expect(screen.getByText("Decision Workspace")).toBeInTheDocument();
  expect(screen.getAllByText("Decision 1").length).toBeGreaterThan(0);
  expect(screen.getByText("Related Entities")).toBeInTheDocument();
  expect(screen.getByText("Evidence")).toBeInTheDocument();
});
