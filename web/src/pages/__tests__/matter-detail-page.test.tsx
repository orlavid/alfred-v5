import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import { MatterDetailPage } from "@/pages/MatterDetailPage";
import type { DashboardBootstrapPayload, ExecutiveMatterDetail } from "@/types";

const bootstrap: DashboardBootstrapPayload = {
  snapshot: {
    snapshot_version: "test",
    build_timestamp: "2026-07-14T10:00:00Z",
    source_vault_timestamp: "2026-07-14T09:00:00Z",
    deployed_commit: "abc1234",
    certification_status: "GREEN",
    last_successful_refresh: "2026-07-14T10:00:00Z",
    last_failed_refresh: null,
    last_failed_reason: null,
    refresh_in_progress: false,
  },
  executive_home: { headline: "", summary_lines: [], kpis: [], sections: [], system_health_route: "/system-health" },
  burning_fires: [],
  plan_today: [],
  next_best_action: { priority: "HIGH", action: "", why_it_matters: "", confidence: "HIGH", origin: "", source_notes: [], provider: "" },
  operating_picture: { overall_health: "GREEN", confidence: "HIGH", meeting_focus: "", followup_pressure: { overdue: 0, due_today: 0, high_priority: 0 }, open_loop_pressure: { critical: 0, waiting_for: 0, missing_owners: 0 }, summary: [], origin: "", source_notes: [], provider: "" },
  navigation_priorities: [],
  interruption_policy: { level: "filter", rule: "" },
  objectives: { health: {}, summary: [], count: 0 },
  projects: { health: {}, summary: [], count: 0 },
  decisions: { counts: { total: 0, defined_status: 0, owner_defined: 0, source_notes: 0 }, summary: [] },
  followups: { counts: { total: 0, overdue: 0, due_today: 0, due_this_week: 0, waiting_on_others: 0, high_priority: 0 }, summary: [], recommendations: [] },
  open_loops: { counts: { total: 0, critical: 0, waiting_for: 0, stalled_projects: 0, missing_decisions: 0, missing_owners: 0 }, summary: [], recommended_actions: [] },
  matters: { counts: { total: 0, requires_attention: 0, decisions_required: 0, meetings_to_prepare: 0, objectives_projects_at_risk: 0, waiting_blocked: 0, recently_changed: 0 }, summary: [] },
  meetings: { subject: "", executive_summary: [], related_people: [], related_projects: [], related_companies: [], related_objectives: [], related_decisions: [], risks: [], open_loops: [], follow_ups: [], recommended_discussion: [], confidence: "LOW" },
  board: { summary: [], members: [], weekly_meeting: [], monthly_meeting: [], standing_agenda: [] },
  ask_alfred: { questions: [], responses: [] },
  daily_brief: { executive_health: [], overnight_changes: [], top_three_priorities: [], meetings_requiring_preparation: [], followups_due_today: [], open_loops_blocking_progress: [], risks_escalating: [], decisions_awaiting_you: [], recommended_agenda: [], one_page_executive_summary: [], confidence: "HIGH" },
  knowledge: { summary: [], entity_counts: {}, graph: { node_count: 0, edge_count: 0, top_nodes: [] } },
  admin_configuration: { overview: { environment_score: 100, overall_health: "GREEN", architecture_rule: "", summary_lines: [] }, sections: { core_configuration: [], vault: [], ai_providers: [], knowledge_sources: [], runtime: [], services: [], security: [], diagnostics: [], deployment: [], required_actions: [] }, auto_configured: {}, doctor_summary: { environment_score: 100, healthy: [], warnings: [], disabled: [], recommended_actions: [], summary_lines: [] }, actions: [] },
  system_health: { summary: [], data_quality_alerts: [], refresh_status: { overall_health: "GREEN", environment_score: 100 } },
  generated_from: { meeting_subject: "", runtime_model: "ExecutiveState", sources: ["ExecutiveState"], confidence: "HIGH" },
};

const detail: ExecutiveMatterDetail = {
  matter_id: "matter-1",
  matter_category: "decision",
  business_title: "Approve Barclays commercial proposal",
  human_summary: "A decision is outstanding before the next steering meeting.",
  why_it_matters: "The proposal affects a current commercial relationship.",
  why_now: "It must be resolved before the next steering meeting.",
  status: "OPEN",
  priority: "HIGH",
  urgency: "HIGH",
  owner: "Unassigned",
  related: { objective: "Cost Management", projects: ["Barclays"], people: ["Phillip"], companies: ["Barclays"] },
  evidence_summary: "Recorded in the Barclays decision note.",
  confidence: "HIGH",
  recommended_next_step: "Assign an owner and confirm the decision outcome.",
  available_actions: [{ action: "open_detail", label: "Open detail" }, { action: "assign_owner", label: "Assign owner" }],
  route: "/matters/matter-1",
  authoritative_route: "/decisions/dec-1",
  action_target: { kind: "matter", id: "matter-1" },
  source_path: "04 Decisions/Barclays.md",
  evidence_paths: ["04 Decisions/Barclays.md"],
  provenance: { decision: ["04 Decisions/Barclays.md"] },
  source_kind: "decision",
  source_record_id: "dec-1",
  detail_backlink_label: "Open decision register",
  recent_activity: "2026-07-14",
  audit_history: [],
  management_notes: [],
  missing_information: [],
};

test("matter detail route renders landing-page engagement workspace", async () => {
  global.fetch = vi.fn(async (input: RequestInfo | URL) => {
    if (String(input).endsWith("/api/matters/matter-1.json")) {
      return new Response(JSON.stringify(detail), { status: 200 });
    }
    throw new Error(`Unexpected fetch ${String(input)}`);
  }) as typeof fetch;

  render(
    <MemoryRouter initialEntries={["/matters/matter-1"]}>
      <Routes>
        <Route path="/matters/:matterId" element={<MatterDetailPage data={bootstrap} onRefresh={async () => {}} />} />
      </Routes>
    </MemoryRouter>,
  );

  await waitFor(() => expect(screen.getByText("Approve Barclays commercial proposal")).toBeInTheDocument());
  expect(screen.getByText("Matter Workspace")).toBeInTheDocument();
  expect(screen.getByText("Workflow Actions")).toBeInTheDocument();
  expect(screen.getByText("Evidence and Provenance")).toBeInTheDocument();
});
