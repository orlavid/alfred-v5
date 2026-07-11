import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { FollowupsPage } from "@/pages/FollowupsPage";
import { OpenLoopsPage } from "@/pages/OpenLoopsPage";
import type { DashboardPayload } from "@/types";

const payload: DashboardPayload = {
  burning_fires: [],
  plan_today: [],
  next_best_action: {
    priority: "HIGH",
    action: "Focus on executive follow-ups.",
    why_it_matters: "Outstanding work items are accumulating.",
    confidence: "HIGH",
    origin: "intent",
    source_notes: ["01 Daily Logs/2026-07-10.md"],
    provider: "executive_intent",
  },
  operating_picture: {
    overall_health: "AMBER",
    confidence: "HIGH",
    meeting_focus: "No active meeting identified.",
    followup_pressure: { overdue: 4, due_today: 1, high_priority: 2 },
    open_loop_pressure: { critical: 3, waiting_for: 2, missing_owners: 1 },
    summary: [],
  },
  navigation_priorities: [],
  interruption_policy: { level: "filter", rule: "Only interrupt for priority issues." },
  objectives: { health: { total: 0, supported: 0, at_risk: 0, watch: 0 }, items: [], summary: [] },
  projects: { health: { total: 0, supported: 0, at_risk: 0, watch: 0 }, items: [], summary: [] },
  followups: {
    counts: { total: 61, overdue: 4, due_today: 1, due_this_week: 8, waiting_on_others: 5, high_priority: 2 },
    items: [
      {
        work_item_id: "follow_up::1",
        title: "Confirm procurement KPI input before the 13 July deadline.",
        summary: "Confirm procurement KPI input before the 13 July deadline.",
        source_path: "01 Daily Logs/2026-07-10.md",
        status: "Not defined",
        priority: "HIGH",
        owner: "Not defined",
        due_date: "2026-07-13",
        source_date: "2026-07-10",
        recency: "2026-07-10",
        buckets: ["High Priority", "Due This Week"],
        classification: "High Priority",
        confidence: "MEDIUM",
        evidence_paths: ["01 Daily Logs/2026-07-10.md"],
        provenance: { evidence_paths: ["01 Daily Logs/2026-07-10.md"] },
      },
      {
        work_item_id: "follow_up::2",
        title: "Progress Jira item VM-675.",
        summary: "Progress Jira item VM-675.",
        source_path: "08 Follow Ups/Follow Up Actions.md",
        status: "WAITING",
        priority: "NORMAL",
        owner: "Not defined",
        due_date: "Not defined",
        source_date: "No evidence found",
        recency: "No evidence found",
        buckets: ["Waiting On Others"],
        classification: "Waiting On Others",
        confidence: "LOW",
        evidence_paths: ["08 Follow Ups/Follow Up Actions.md"],
        provenance: { evidence_paths: ["08 Follow Ups/Follow Up Actions.md"] },
      },
    ],
    summary: [],
    recommendations: [],
  },
  open_loops: {
    counts: { total: 209, critical: 12, waiting_for: 8, stalled_projects: 3, missing_decisions: 7, missing_owners: 2 },
    items: [
      {
        work_item_id: "open_loop::1",
        title: "Awaiting clarification from Finance/AP on invoice edits.",
        summary: "Awaiting clarification from Finance/AP on invoice edits.",
        source_path: "01 Daily Logs/2026-07-09.md",
        status: "OPEN",
        priority: "HIGH",
        owner: "Not defined",
        due_date: "Not defined",
        source_date: "2026-07-09",
        recency: "2026-07-09",
        buckets: ["Critical Open Loops", "Waiting For"],
        classification: "Critical",
        confidence: "HIGH",
        related_entities: ["Finance/AP"],
        evidence_paths: ["01 Daily Logs/2026-07-09.md"],
        provenance: { evidence_paths: ["01 Daily Logs/2026-07-09.md"] },
      },
      {
        work_item_id: "open_loop::2",
        title: "Awaiting final SOW from Polo.",
        summary: "Awaiting final SOW from Polo.",
        source_path: "01 Daily Logs/2026-07-06.md",
        status: "OPEN",
        priority: "MEDIUM",
        owner: "Not defined",
        due_date: "Not defined",
        source_date: "2026-07-06",
        recency: "2026-07-06",
        buckets: ["Waiting For"],
        classification: "Waiting For",
        confidence: "MEDIUM",
        related_entities: ["Polo"],
        evidence_paths: ["01 Daily Logs/2026-07-06.md"],
        provenance: { evidence_paths: ["01 Daily Logs/2026-07-06.md"] },
      },
    ],
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
    followups_due_today: ["Close or progress Jira item VM-675 today."],
    open_loops_blocking_progress: ["Awaiting clarification from Finance/AP on invoice edits."],
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

test("follow-ups page shows the full canonical collection and keeps the daily brief summary", () => {
  render(
    <MemoryRouter initialEntries={["/follow-ups"]}>
      <Routes>
        <Route path="/follow-ups" element={<FollowupsPage data={payload} />} />
      </Routes>
    </MemoryRouter>,
  );

  expect(screen.getByText("Priority Now")).toBeInTheDocument();
  expect(screen.getByText(/Close or progress Jira item VM-675 today\./)).toBeInTheDocument();
  expect(screen.getByText("Full Canonical Count:")).toBeInTheDocument();
  expect(screen.getByText("61")).toBeInTheDocument();
  expect(screen.getByText("Confirm procurement KPI input before the 13 July deadline.")).toBeInTheDocument();
  expect(screen.getByText("Progress Jira item VM-675.")).toBeInTheDocument();
});

test("open-loops page shows the full canonical collection and keeps the daily brief summary", () => {
  render(
    <MemoryRouter initialEntries={["/open-loops"]}>
      <Routes>
        <Route path="/open-loops" element={<OpenLoopsPage data={payload} />} />
      </Routes>
    </MemoryRouter>,
  );

  expect(screen.getByText("Priority Now")).toBeInTheDocument();
  expect(screen.getAllByText(/Awaiting clarification from Finance\/AP on invoice edits\./).length).toBe(2);
  expect(screen.getByText("Full Canonical Count:")).toBeInTheDocument();
  expect(screen.getByText("209")).toBeInTheDocument();
  expect(screen.getByText("Awaiting final SOW from Polo.")).toBeInTheDocument();
});
