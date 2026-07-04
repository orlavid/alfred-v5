import { MemoryRouter } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { DashboardPage } from "@/pages/DashboardPage";
import type { DashboardPayload } from "@/types";

const payload: DashboardPayload = {
  burning_fires: [{ type: "risk", summary: "A critical supplier issue needs action." }],
  plan_today: ["Assign an owner to the critical supplier issue."],
  next_best_action: {
    priority: "HIGH",
    action: "Assign an owner to the critical supplier issue.",
    why_it_matters: "The issue is blocking a delivery path.",
    confidence: "HIGH",
  },
  operating_picture: {
    overall_health: "AMBER (80 / 100)",
    confidence: "HIGH",
    meeting_focus: "Barclays",
    followup_pressure: { overdue: 4, due_today: 1, high_priority: 2 },
    open_loop_pressure: { critical: 3, waiting_for: 2, missing_owners: 1 },
    summary: ["Top priority today: assign the owner."],
  },
  navigation_priorities: [{ label: "Meetings", reason: "Prepare for Barclays." }],
  interruption_policy: { level: "filter", rule: "Only interrupt for priority issues." },
  objectives: { health: { total: 1, supported: 1, at_risk: 0, watch: 0 }, items: [], summary: [] },
  projects: { health: { total: 1, supported: 1, at_risk: 0, watch: 0 }, items: [], summary: [] },
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
  generated_from: {
    meeting_subject: "Barclays",
    runtime_model: "ExecutiveState",
    sources: ["ExecutiveState"],
    confidence: "HIGH",
  },
};

test("renders dashboard API sections", () => {
  render(
    <MemoryRouter>
      <DashboardPage data={payload} />
    </MemoryRouter>,
  );

  expect(screen.getByText("Burning Fires")).toBeInTheDocument();
  expect(screen.getByText("Next Best Action")).toBeInTheDocument();
  expect(screen.getByText("A critical supplier issue needs action.")).toBeInTheDocument();
  expect(screen.getAllByText("Assign an owner to the critical supplier issue.").length).toBeGreaterThan(0);
});
