import { MemoryRouter } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { DashboardPage } from "@/pages/DashboardPage";
import type { DashboardBootstrapPayload } from "@/types";

const payload: DashboardBootstrapPayload = {
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
  executive_home: {
    headline: "Executive engagement surface",
    summary_lines: ["2 matters currently need attention."],
    kpis: [
      { card_id: "attention", label: "Requires Your Attention", summary: "Approve Barclays commercial decision.", count: 2, route: "/" },
      { card_id: "decisions", label: "Decisions Required", summary: "Approve Barclays commercial decision.", count: 1, route: "/decisions" },
    ],
    sections: [
      {
        section_id: "requires_attention",
        title: "Requires Your Attention",
        summary: "Current matters that need executive time.",
        matters: [
          {
            matter_id: "matter-1",
            matter_category: "decision",
            business_title: "Approve Barclays commercial proposal",
            human_summary: "A decision is still outstanding before the next steering meeting.",
            why_it_matters: "The proposal affects a live commercial relationship.",
            why_now: "The next steering meeting is imminent.",
            status: "OPEN",
            priority: "HIGH",
            urgency: "HIGH",
            owner: "Unassigned",
            related: { objective: "Cost Management", projects: ["Barclays"], people: ["Phillip"], companies: ["Barclays"] },
            evidence_summary: "Recorded in the Barclays decision note with open commercial questions.",
            confidence: "HIGH",
            recommended_next_step: "Assign an owner and confirm the decision outcome.",
            available_actions: [{ action: "open_detail", label: "Open detail" }, { action: "assign_owner", label: "Assign owner" }],
            route: "/matters/matter-1",
            authoritative_route: "/decisions/dec-1",
            action_target: { kind: "matter", id: "matter-1" },
          },
        ],
      },
    ],
    system_health_route: "/system-health",
  },
  burning_fires: [],
  plan_today: [],
  next_best_action: {
    priority: "HIGH",
    action: "Approve Barclays commercial proposal",
    why_it_matters: "The proposal affects a live relationship.",
    confidence: "HIGH",
    origin: "executive_intent",
    source_notes: [],
    provider: "executive_intent",
  },
  operating_picture: {
    overall_health: "GREEN",
    confidence: "HIGH",
    meeting_focus: "Barclays",
    followup_pressure: { overdue: 2, due_today: 1, high_priority: 1 },
    open_loop_pressure: { critical: 1, waiting_for: 1, missing_owners: 1 },
    summary: ["Executive picture available."],
    origin: "executive_state",
    source_notes: [],
    provider: "executive_state",
  },
  navigation_priorities: [],
  interruption_policy: { level: "filter", rule: "Only interrupt for matters tied to current priorities." },
  objectives: { health: { total: 1, supported: 1, at_risk: 0, watch: 0 }, summary: [], count: 1 },
  projects: { health: { total: 1, supported: 1, at_risk: 0, watch: 0 }, summary: [], count: 1 },
  decisions: { counts: { total: 1, defined_status: 1, owner_defined: 0, source_notes: 1 }, summary: [] },
  followups: {
    counts: { total: 1, overdue: 0, due_today: 1, due_this_week: 1, waiting_on_others: 0, high_priority: 1 },
    summary: [],
    recommendations: [],
  },
  open_loops: {
    counts: { total: 1, critical: 1, waiting_for: 1, stalled_projects: 0, missing_decisions: 0, missing_owners: 1 },
    summary: [],
    recommended_actions: [],
  },
  matters: {
    counts: { total: 1, requires_attention: 1, decisions_required: 1, meetings_to_prepare: 0, objectives_projects_at_risk: 0, waiting_blocked: 0, recently_changed: 0 },
    summary: [],
  },
  meetings: {
    subject: "Barclays",
    executive_summary: [],
    related_people: [],
    related_projects: [],
    related_companies: [],
    related_objectives: [],
    related_decisions: [],
    risks: [],
    open_loops: [],
    follow_ups: [],
    recommended_discussion: [],
    confidence: "HIGH",
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
  knowledge: { summary: [], entity_counts: {}, graph: { node_count: 1, edge_count: 1, top_nodes: [] } },
  admin_configuration: {
    overview: { environment_score: 100, overall_health: "GREEN", architecture_rule: "", summary_lines: [] },
    sections: { core_configuration: [], vault: [], ai_providers: [], knowledge_sources: [], runtime: [], services: [], security: [], diagnostics: [], deployment: [], required_actions: [] },
    auto_configured: {},
    doctor_summary: { environment_score: 100, healthy: [], warnings: [], disabled: [], recommended_actions: [], summary_lines: [] },
    actions: [],
  },
  system_health: {
    summary: ["Operational readiness is GREEN."],
    data_quality_alerts: [],
    refresh_status: { overall_health: "GREEN", environment_score: 100 },
  },
  generated_from: {
    meeting_subject: "Barclays",
    runtime_model: "ExecutiveState",
    sources: ["ExecutiveState"],
    confidence: "HIGH",
  },
};

test("renders governed executive home sections instead of legacy dashboard cards", () => {
  render(
    <MemoryRouter>
      <DashboardPage data={payload} onRefresh={async () => {}} />
    </MemoryRouter>,
  );

  expect(screen.getByText("Executive engagement surface")).toBeInTheDocument();
  expect(screen.getAllByText("Requires Your Attention").length).toBeGreaterThan(0);
  expect(screen.getByText("Approve Barclays commercial proposal")).toBeInTheDocument();
  expect(screen.queryByText("Burning Fires")).not.toBeInTheDocument();
  expect(screen.queryByText("Plan Today")).not.toBeInTheDocument();
});
