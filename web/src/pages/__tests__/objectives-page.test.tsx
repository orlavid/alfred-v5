import { MemoryRouter, Route, Routes } from "react-router-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import { ObjectivesPage } from "@/pages/ObjectivesPage";
import { ObjectiveDetailPage } from "@/pages/ObjectiveDetailPage";
import type { DashboardPayload } from "@/types";

const payload: DashboardPayload = {
  burning_fires: [],
  plan_today: [],
  next_best_action: {
    priority: "HIGH",
    action: "Review objective governance.",
    why_it_matters: "It drives operating control.",
    confidence: "HIGH",
    origin: "intent",
    source_notes: ["09 Governance/Objectives/2026 Executive Objectives.md"],
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
  objectives: {
    health: { total: 1, supported: 1, at_risk: 0, watch: 0 },
    items: [
      {
        objective_id: "obj-123",
        title: "Operational Governance",
        source_path: "09 Governance/Objectives/2026 Executive Objectives.md#objective-1-operational-governance",
        source_entity_id: "09 Governance/Objectives/2026 Executive Objectives.md#objective-1-operational-governance",
        route: "/objectives/obj-123",
        lifecycle: "SUPPORTED",
        confidence: "MEDIUM",
        health: "GREEN",
        progress_indicator: "SUPPORTED, 2 supporting project(s), 1 linked decision(s)",
        owner: "Not defined",
        last_meaningful_activity: "2026-07-01",
        next_checkpoint_or_deadline: "Not defined",
        supporting_project_count: 2,
        linked_decision_count: 1,
        open_action_count: 1,
        key_risk_or_blocker: "Governance decision pending",
        supporting_projects: ["Governance Programme", "Risk Oversight"],
        linked_decisions: ["Governance Approval"],
        stale_evidence: false,
        recommended_next_action: "Add an explicit review cadence for this objective.",
        missing_fields: ["Accountable owner is not defined."],
      },
    ],
    details: {
      "obj-123": {
        objective_id: "obj-123",
        route: "/objectives/obj-123",
        title: "Operational Governance",
        source_entity_id: "09 Governance/Objectives/2026 Executive Objectives.md#objective-1-operational-governance",
        source_path: "09 Governance/Objectives/2026 Executive Objectives.md#objective-1-operational-governance",
        executive_definition: "Defined in the 2026 Executive Objectives register.",
        owner: "Not defined",
        delegates: [],
        current_status: "SUPPORTED",
        health: "GREEN",
        rag_rating: "GREEN",
        progress_assessment: "SUPPORTED, 2 supporting project(s), 1 linked decision(s)",
        evidence_confidence: "MEDIUM",
        start_date: "Not defined",
        target_date: "Not defined",
        last_review_date: "Not defined",
        next_review_date: "Not defined",
        last_meaningful_activity: "2026-07-01",
        next_checkpoint_or_deadline: "Not defined",
        supporting_projects: [
          {
            title: "Governance Programme",
            path: "03 Projects/Governance Programme.md",
            reason: "Linked to the objective in the executive knowledge graph.",
            route: "/projects",
          },
        ],
        linked_decisions: [
          {
            title: "Governance Approval",
            path: "09 Governance/Decisions/Governance Approval.md",
            reason: "Importance 120; linked to 1 projects and 1 objectives.",
            route: "/decisions",
          },
        ],
        risks_and_blockers: [
          {
            title: "Governance decision pending",
            path: "07 Open Loops/Open Loop Register.md",
            reason: "Decision review; status OPEN; priority HIGH.",
            type: "decision_review",
            route: "/open-loops",
          },
        ],
        open_actions: [
          {
            work_item_id: "follow_up::1",
            title: "Confirm governance review date.",
            type: "follow_up",
            status: "Not defined",
            priority: "HIGH",
            path: "08 Follow Ups/Follow Up Actions.md",
            reason: "Follow-up action; due Not defined; priority HIGH.",
            route: "/follow-ups",
          },
        ],
        follow_ups: [
          {
            work_item_id: "follow_up::1",
            title: "Confirm governance review date.",
            type: "follow_up",
            status: "Not defined",
            priority: "HIGH",
            path: "08 Follow Ups/Follow Up Actions.md",
            reason: "Follow-up action; due Not defined; priority HIGH.",
            route: "/follow-ups",
          },
        ],
        relevant_meetings: [],
        related_people: [],
        evidence_sources: [
          {
            label: "2026 Executive Objectives",
            path: "09 Governance/Objectives/2026 Executive Objectives.md#objective-1-operational-governance",
            reason: "Canonical objective evidence source.",
          },
        ],
        recent_changes: ["Last meaningful activity recorded on 2026-07-01."],
        recommended_next_action: "Add an explicit review cadence for this objective.",
        missing_information: ["Accountable owner is not defined."],
        smart_assessment: {
          specific: {
            current_assessment: "Evidence-backed",
            evidence: ["09 Governance/Objectives/2026 Executive Objectives.md#objective-1-operational-governance"],
            missing_or_weak_definition: "None identified from current evidence.",
            suggested_improvement: "Link the objective to the delivery programme or decision set that defines its scope.",
          },
          measurable: {
            current_assessment: "Weak or not defined",
            evidence: ["No evidence found."],
            missing_or_weak_definition: "No explicit status, checkpoint, or deadline evidence.",
            suggested_improvement: "Add explicit status checkpoints, target measures, or dated review points.",
          },
        },
        proposed_smart_refinement: [
          "Retain the current objective title: Operational Governance.",
          "Measurable: Add explicit status checkpoints, target measures, or dated review points.",
        ],
        stale_evidence: false,
        linked_decision_titles: ["Governance Approval"],
        relevant_meeting_titles: [],
        source_work_item_ids: ["follow_up::1"],
        provenance: {
          objective: ["09 Governance/Objectives/2026 Executive Objectives.md#objective-1-operational-governance"],
          supporting_projects: ["03 Projects/Governance Programme.md"],
          linked_decisions: ["09 Governance/Decisions/Governance Approval.md"],
          risks_and_blockers: ["07 Open Loops/Open Loop Register.md"],
          open_actions: ["08 Follow Ups/Follow Up Actions.md"],
        },
      },
    },
    summary: [],
  },
  projects: { health: { total: 0, supported: 0, at_risk: 0, watch: 0 }, items: [], summary: [] },
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

test("objective cards show management content and link to the workspace", () => {
  render(
    <MemoryRouter initialEntries={["/objectives"]}>
      <Routes>
        <Route path="/objectives" element={<ObjectivesPage data={payload} />} />
      </Routes>
    </MemoryRouter>,
  );

  expect(screen.getByText("Operational Governance")).toBeInTheDocument();
  expect(screen.getByText("Governance decision pending")).toBeInTheDocument();
  expect(screen.getByText("Open objective")).toBeInTheDocument();
  expect(screen.getAllByRole("link")[0]).toHaveAttribute("href", "/objectives/obj-123");
});

test("objective detail route renders SMART assessment and supporting content", () => {
  render(
    <MemoryRouter initialEntries={["/objectives/obj-123"]}>
      <Routes>
        <Route path="/objectives/:objectiveId" element={<ObjectiveDetailPage data={payload} />} />
      </Routes>
    </MemoryRouter>,
  );

  expect(screen.getByText("Objective Workspace")).toBeInTheDocument();
  expect(screen.getByText("Defined in the 2026 Executive Objectives register.")).toBeInTheDocument();
  expect(screen.getByText("Governance Programme")).toBeInTheDocument();
  expect(screen.getByText("SMART Assessment")).toBeInTheDocument();
  expect(screen.getAllByText(/measurable/i).length).toBeGreaterThan(0);
  expect(screen.getAllByText(/accountable owner is not defined/i).length).toBeGreaterThan(0);
});

test("clicking an objective card opens the detail workspace", () => {
  render(
    <MemoryRouter initialEntries={["/objectives"]}>
      <Routes>
        <Route path="/objectives" element={<ObjectivesPage data={payload} />} />
        <Route path="/objectives/:objectiveId" element={<ObjectiveDetailPage data={payload} />} />
      </Routes>
    </MemoryRouter>,
  );

  fireEvent.click(screen.getAllByRole("link")[0]);

  expect(screen.getByText("Management Links")).toBeInTheDocument();
  expect(screen.getByText("Evidence Sources")).toBeInTheDocument();
});
