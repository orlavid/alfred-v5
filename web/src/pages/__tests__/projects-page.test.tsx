import { MemoryRouter, Route, Routes } from "react-router-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import { ProjectsPage } from "@/pages/ProjectsPage";
import { ProjectDetailPage } from "@/pages/ProjectDetailPage";
import type { DashboardPayload } from "@/types";

const payload: DashboardPayload = {
  burning_fires: [],
  plan_today: [],
  next_best_action: {
    priority: "HIGH",
    action: "Advance Project Phoenix.",
    why_it_matters: "Delivery depends on it.",
    confidence: "HIGH",
    origin: "intent",
    source_notes: ["03 Projects/Project Phoenix.md"],
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
  projects: {
    health: { total: 2, supported: 1, at_risk: 1, watch: 0 },
    items: [
      {
        project_id: "proj-1",
        title: "Project Phoenix",
        source_path: "03 Projects/Project Phoenix.md",
        source_entity_id: "project-phoenix",
        route: "/projects/proj-1",
        status: "AT RISK",
        health: "RED",
        owner: "Phillip Doheny",
        progress_indicator: "AT RISK, 1 linked objective(s), 2 open work item(s)",
        last_meaningful_activity: "2026-07-10",
        next_checkpoint_or_deadline: "2026-07-20",
        objective_linkage: ["Operational Governance"],
        linked_decision_count: 1,
        open_action_count: 2,
        evidence_confidence: "HIGH",
        risk: "Phoenix dependency pending",
        recommendation: "Resolve the blocking dependency and confirm the checkpoint date.",
        missing_fields: ["Review cadence is not defined."],
      },
      {
        project_id: "proj-2",
        title: "Project Atlas",
        source_path: "03 Projects/Project Atlas.md",
        source_entity_id: "project-atlas",
        route: "/projects/proj-2",
        status: "SUPPORTED",
        health: "GREEN",
        owner: "Jane Smith",
        progress_indicator: "SUPPORTED, 1 linked objective(s)",
        last_meaningful_activity: "2026-07-09",
        next_checkpoint_or_deadline: "Not defined",
        objective_linkage: ["Risk Management"],
        linked_decision_count: 0,
        open_action_count: 0,
        evidence_confidence: "MEDIUM",
        risk: "No evidence found",
        recommendation: "Maintain the current delivery cadence.",
        missing_fields: [],
      },
    ],
    details: {
      "proj-1": {
        project_id: "proj-1",
        route: "/projects/proj-1",
        title: "Project Phoenix",
        source_entity_id: "project-phoenix",
        source_path: "03 Projects/Project Phoenix.md",
        executive_definition: "Project Phoenix is the current delivery vehicle for the governance change.",
        owner: "Phillip Doheny",
        delegates: [],
        contributors: [],
        current_status: "AT RISK",
        health: "RED",
        rag_rating: "RED",
        progress_assessment: "AT RISK, 1 linked objective(s), 2 open work item(s)",
        progress_percentage: null,
        evidence_confidence: "HIGH",
        priority: "HIGH",
        start_date: "2026-06-01",
        target_date: "2026-07-20",
        last_review_date: "Not defined",
        next_review_date: "Not defined",
        last_meaningful_activity: "2026-07-10",
        next_checkpoint_or_deadline: "2026-07-20",
        linked_objectives: [
          { id: "obj-1", title: "Operational Governance", path: "09 Governance/Objectives/2026 Executive Objectives.md", reason: "Connected in canonical executive state.", route: "/objectives/obj-1" },
        ],
        linked_decisions: [
          { title: "Phoenix Approval", path: "09 Governance/Decisions/Phoenix Approval.md", reason: "Importance 140; linked to 1 projects and 1 objectives.", route: "/decisions" },
        ],
        related_companies: [],
        risks_and_blockers: [
          { title: "Phoenix dependency pending", path: "07 Open Loops/Open Loop Register.md", reason: "Open loop; status OPEN; priority HIGH.", type: "open_loop", route: "/open-loops" },
        ],
        open_actions: [
          { work_item_id: "follow_up::1", title: "Confirm Phoenix checkpoint this week.", type: "follow_up", status: "OPEN", priority: "HIGH", path: "08 Follow Ups/Follow Up Actions.md", reason: "Follow-up action; due Not defined; priority HIGH.", route: "/follow-ups" },
        ],
        follow_ups: [
          { work_item_id: "follow_up::1", title: "Confirm Phoenix checkpoint this week.", type: "follow_up", status: "OPEN", priority: "HIGH", path: "08 Follow Ups/Follow Up Actions.md", reason: "Follow-up action; due Not defined; priority HIGH.", route: "/follow-ups" },
        ],
        open_loops: [
          { work_item_id: "open_loop::1", title: "Phoenix dependency pending", type: "open_loop", status: "OPEN", priority: "HIGH", path: "07 Open Loops/Open Loop Register.md", reason: "Open loop; status OPEN; priority HIGH.", route: "/open-loops" },
        ],
        relevant_meetings: [],
        related_people: [],
        evidence_sources: [
          { label: "Project Phoenix", path: "03 Projects/Project Phoenix.md", reason: "Canonical objective evidence source." },
        ],
        success_measures: [],
        milestones: [],
        resources: [],
        dependencies: [],
        management_notes: [],
        audit_history: [],
        relationship_options: {
          linked_objectives: [],
          linked_decisions: [],
          follow_ups: [],
          open_loops: [],
          relevant_meetings: [],
          related_people: [],
          related_companies: [],
        },
        recent_changes: ["Last meaningful activity recorded on 2026-07-10."],
        recommended_next_action: "Resolve the blocking dependency and confirm the checkpoint date.",
        missing_information: ["Review cadence is not defined."],
        stale_evidence: false,
        provenance: { project: ["03 Projects/Project Phoenix.md"] },
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

test("projects page supports filtering and drill-through", () => {
  render(
    <MemoryRouter initialEntries={["/projects"]}>
      <Routes>
        <Route path="/projects" element={<ProjectsPage data={payload} />} />
      </Routes>
    </MemoryRouter>,
  );

  expect(screen.getByText("Project Phoenix")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Search"), { target: { value: "Atlas" } });
  expect(screen.queryByText("Project Phoenix")).not.toBeInTheDocument();
  expect(screen.getByText("Project Atlas")).toBeInTheDocument();
});

test("project detail route renders the workspace", () => {
  render(
    <MemoryRouter initialEntries={["/projects/proj-1"]}>
      <Routes>
        <Route path="/projects/:projectId" element={<ProjectDetailPage data={payload} onRefresh={async () => undefined} />} />
      </Routes>
    </MemoryRouter>,
  );

  expect(screen.getByText("Project Workspace")).toBeInTheDocument();
  expect(screen.getAllByText("Project Phoenix").length).toBeGreaterThan(0);
  expect(screen.getByText("Management Data")).toBeInTheDocument();
  expect(screen.getByText("Audit History")).toBeInTheDocument();
});
