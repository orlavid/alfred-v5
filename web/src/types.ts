export type DashboardPayload = {
  burning_fires: Array<{ type: string; summary: string }>;
  plan_today: Array<{
    type: string;
    summary: string;
    confidence: string;
    origin: string;
    provider: string;
    source_notes: string[];
  }>;
  next_best_action: {
    priority: string;
    action: string;
    why_it_matters: string;
    confidence: string;
  };
  operating_picture: {
    overall_health: string;
    confidence: string;
    meeting_focus: string;
    followup_pressure: { overdue: number; due_today: number; high_priority: number };
    open_loop_pressure: { critical: number; waiting_for: number; missing_owners: number };
    summary: string[];
  };
  navigation_priorities: Array<{ label: string; reason: string }>;
  interruption_policy: { level: string; rule: string };
  objectives: {
    health: Record<string, number>;
    items: Array<{
      title: string;
      lifecycle: string;
      confidence: string;
      supporting_projects: string[];
      linked_decisions: string[];
      stale_evidence: boolean;
      recommended_next_action: string;
    }>;
    summary: string[];
  };
  projects: {
    health: Record<string, number>;
    items: Array<{
      title: string;
      status: string;
      objective_linkage: string[];
      risk: string;
      recommendation: string;
    }>;
    summary: string[];
  };
  meetings: {
    subject: string;
    executive_summary: string[];
    related_people: string[];
    related_projects: string[];
    related_companies: string[];
    related_objectives: string[];
    related_decisions: string[];
    risks: string[];
    open_loops: string[];
    follow_ups: string[];
    recommended_discussion: string[];
    confidence: string;
  };
  board: {
    summary: string[];
    members: Array<{
      name: string;
      role: string;
      purpose: string;
      responsibilities: string[];
      authority: string;
      meeting_role: string;
      weekly_board_contribution: string;
      monthly_board_contribution: string;
      prompt_profile: string;
      communication_style: string;
      portrait_placeholder: string;
      status: string;
    }>;
    weekly_meeting: string[];
    monthly_meeting: string[];
    standing_agenda: string[];
  };
  ask_alfred: {
    questions: string[];
    responses: Array<{
      question: string;
      executive_answer: string[];
      supporting_evidence: string[];
      confidence: string;
      recommended_next_actions: string[];
    }>;
  };
  daily_brief: {
    executive_health: string[];
    overnight_changes: string[];
    top_three_priorities: string[];
    meetings_requiring_preparation: string[];
    followups_due_today: string[];
    open_loops_blocking_progress: string[];
    risks_escalating: string[];
    decisions_awaiting_you: string[];
    recommended_agenda: string[];
    one_page_executive_summary: string[];
    confidence: string;
  };
  knowledge: {
    summary: string[];
    entity_counts: Record<string, number>;
    graph: { node_count: number; edge_count: number; top_nodes: string[] };
  };
  admin_configuration: {
    overview: {
      environment_score: number;
      overall_health: string;
      architecture_rule: string;
      summary_lines: string[];
    };
    sections: {
      core_configuration: AdminComponent[];
      vault: AdminComponent[];
      ai_providers: AdminComponent[];
      knowledge_sources: AdminComponent[];
      runtime: AdminComponent[];
      services: AdminComponent[];
      security: AdminComponent[];
      diagnostics: AdminComponent[];
      deployment: AdminAction[];
      required_actions: string[];
    };
    auto_configured: Record<
      string,
      {
        value: string;
        discovery_method: string;
        confidence: string;
        timestamp: string;
      }
    >;
    doctor_summary: {
      environment_score: number;
      healthy: string[];
      warnings: string[];
      disabled: string[];
      recommended_actions: string[];
      summary_lines: string[];
    };
    actions: AdminAction[];
  };
  generated_from: {
    meeting_subject: string;
    runtime_model: string;
    sources: string[];
    confidence: string;
  };
};

export type AdminComponent = {
  name: string;
  status: string;
  health: string;
  version: string;
  install_location: string;
  configuration_source: string;
  required: boolean;
  dependencies: string[];
  last_checked: string;
  last_changed: string;
  recommended_action: string;
  work_instruction_link: string;
};

export type AdminAction = {
  label: string;
  command: string;
  summary: string;
  work_instruction_link: string;
  mode: string;
};
