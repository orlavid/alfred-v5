export type SnapshotInfo = {
  snapshot_version: string;
  build_timestamp: string;
  source_vault_timestamp: string | null;
  deployed_commit: string;
  certification_status: string;
  last_successful_refresh: string | null;
  last_failed_refresh: string | null;
  last_failed_reason: string | null;
  refresh_in_progress: boolean;
  refresh_started_at?: string | null;
  current_snapshot_version?: string | null;
};

export type PlanItem = {
  type: string;
  summary: string;
  confidence: string;
  origin: string;
  provider: string;
  source_notes: string[];
};

export type LinkedObjectiveItem = {
  id?: string;
  work_item_id?: string;
  title: string;
  path: string;
  reason: string;
  route: string;
};

export type SmartAssessmentDimension = {
  current_assessment: string;
  evidence: string[];
  missing_or_weak_definition: string;
  suggested_improvement: string;
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

export type ObjectiveDetail = {
  objective_id: string;
  route: string;
  title: string;
  source_entity_id: string;
  source_path: string;
  executive_definition: string;
  owner: string;
  delegates: string[];
  contributors: string[];
  current_status: string;
  health: string;
  rag_rating: string;
  progress_assessment: string;
  progress_percentage: number | null;
  evidence_confidence: string;
  priority: string;
  start_date: string;
  target_date: string;
  last_review_date: string;
  next_review_date: string;
  last_meaningful_activity: string;
  next_checkpoint_or_deadline: string;
  supporting_projects: LinkedObjectiveItem[];
  linked_decisions: LinkedObjectiveItem[];
  risks_and_blockers: Array<LinkedObjectiveItem & { type: string }>;
  open_actions: Array<{
    work_item_id: string;
    title: string;
    type: string;
    status: string;
    priority: string;
    path: string;
    reason: string;
    route: string;
  }>;
  follow_ups: Array<{
    work_item_id: string;
    title: string;
    type: string;
    status: string;
    priority: string;
    path: string;
    reason: string;
    route: string;
  }>;
  open_loops: Array<{
    work_item_id: string;
    title: string;
    type: string;
    status: string;
    priority: string;
    path: string;
    reason: string;
    route: string;
  }>;
  relevant_meetings: LinkedObjectiveItem[];
  related_people: LinkedObjectiveItem[];
  evidence_sources: Array<{
    label: string;
    path: string;
    reason: string;
  }>;
  success_measures: string[];
  milestones: Array<{
    milestone_id: string;
    title: string;
    due_date: string;
    status: string;
    completed_at: string | null;
  }>;
  resources: string[];
  dependencies: string[];
  management_notes: Array<{
    note_id: string;
    text: string;
    timestamp: string;
    source: string;
    reason: string;
  }>;
  audit_history: Array<{
    audit_id: string;
    timestamp: string;
    action: string;
    field: string;
    previous_value: unknown;
    new_value: unknown;
    source: string;
    reason: string;
  }>;
  smart_enrichment_proposal: {
    proposal_id: string;
    created_at: string;
    status: string;
    source: string;
    reason: string;
    summary_lines: string[];
    field_proposals: Record<string, unknown>;
    evidence_paths: string[];
    accepted_fields?: string[];
  } | null;
  relationship_options: Record<string, LinkedObjectiveItem[]>;
  recent_changes: string[];
  recommended_next_action: string;
  missing_information: string[];
  smart_assessment: Record<string, SmartAssessmentDimension>;
  proposed_smart_refinement: string[];
  stale_evidence: boolean;
  linked_decision_titles: string[];
  relevant_meeting_titles: string[];
  source_work_item_ids: string[];
  provenance: Record<string, string[]>;
};

export type ProjectDetail = {
  project_id: string;
  route: string;
  title: string;
  source_entity_id: string;
  source_path: string;
  executive_definition: string;
  owner: string;
  delegates: string[];
  contributors: string[];
  current_status: string;
  health: string;
  rag_rating: string;
  progress_assessment: string;
  progress_percentage: number | null;
  evidence_confidence: string;
  priority: string;
  start_date: string;
  target_date: string;
  last_review_date: string;
  next_review_date: string;
  last_meaningful_activity: string;
  next_checkpoint_or_deadline: string;
  linked_objectives: LinkedObjectiveItem[];
  linked_decisions: LinkedObjectiveItem[];
  related_companies: LinkedObjectiveItem[];
  risks_and_blockers: Array<LinkedObjectiveItem & { type: string }>;
  open_actions: ObjectiveDetail["open_actions"];
  follow_ups: ObjectiveDetail["follow_ups"];
  open_loops: ObjectiveDetail["open_loops"];
  relevant_meetings: LinkedObjectiveItem[];
  related_people: LinkedObjectiveItem[];
  evidence_sources: ObjectiveDetail["evidence_sources"];
  success_measures: string[];
  milestones: ObjectiveDetail["milestones"];
  resources: string[];
  dependencies: string[];
  management_notes: ObjectiveDetail["management_notes"];
  audit_history: ObjectiveDetail["audit_history"];
  relationship_options: Record<string, LinkedObjectiveItem[]>;
  recent_changes: string[];
  recommended_next_action: string;
  missing_information: string[];
  stale_evidence: boolean;
  provenance: Record<string, string[]>;
};

export type DecisionDetail = {
  decision_id: string;
  route: string;
  title: string;
  source_entity_id: string;
  source_path: string;
  decision_date: string;
  current_status: string;
  owner: string;
  importance: number;
  evidence_confidence: string;
  rationale: string;
  related_projects: LinkedObjectiveItem[];
  related_objectives: LinkedObjectiveItem[];
  related_people: LinkedObjectiveItem[];
  related_companies: LinkedObjectiveItem[];
  related_work_items: Array<{
    work_item_id: string;
    title: string;
    path: string;
    reason: string;
    route: string;
    type: string;
  }>;
  relevant_meetings: LinkedObjectiveItem[];
  evidence_sources: ObjectiveDetail["evidence_sources"];
  recent_changes: string[];
  missing_information: string[];
  stale_evidence: boolean;
  source_entities: string[];
  source_work_items: string[];
  provenance: Record<string, string[]>;
};

export type ObjectivesDomainPayload = {
  health: Record<string, number>;
  items: Array<{
    objective_id: string;
    title: string;
    source_path: string;
    source_entity_id: string;
    route: string;
    lifecycle: string;
    confidence: string;
    health: string;
    progress_indicator: string;
    owner: string;
    last_meaningful_activity: string;
    next_checkpoint_or_deadline: string;
    supporting_project_count: number;
    linked_decision_count: number;
    open_action_count: number;
    key_risk_or_blocker: string;
    supporting_projects: string[];
    linked_decisions: string[];
    stale_evidence: boolean;
    recommended_next_action: string;
    missing_fields: string[];
  }>;
  details?: Record<string, ObjectiveDetail>;
  summary: string[];
};

export type ProjectsDomainPayload = {
  health: Record<string, number>;
  items: Array<{
    project_id: string;
    title: string;
    source_path: string;
    source_entity_id: string;
    route: string;
    status: string;
    health: string;
    owner: string;
    progress_indicator: string;
    last_meaningful_activity: string;
    next_checkpoint_or_deadline: string;
    objective_linkage: string[];
    linked_decision_count: number;
    open_action_count: number;
    evidence_confidence: string;
    risk: string;
    recommendation: string;
    missing_fields: string[];
  }>;
  details?: Record<string, ProjectDetail>;
  summary: string[];
};

export type DecisionsDomainPayload = {
  counts: {
    total: number;
    defined_status: number;
    owner_defined: number;
    source_notes: number;
  };
  items: Array<{
    decision_id: string;
    title: string;
    source_path: string;
    source_entity_id: string;
    route: string;
    status: string;
    owner: string;
    decision_date: string;
    related_project_count: number;
    related_objective_count: number;
    related_people_count: number;
    evidence_confidence: string;
    rationale: string;
    missing_fields: string[];
    importance: number;
  }>;
  details?: Record<string, DecisionDetail>;
  summary: string[];
};

export type FollowupsDomainPayload = {
  counts: {
    total: number;
    overdue: number;
    due_today: number;
    due_this_week: number;
    waiting_on_others: number;
    high_priority: number;
  };
  items: Array<{
    work_item_id: string;
    title: string;
    summary: string;
    source_path: string;
    status: string;
    priority: string;
    owner: string;
    due_date: string;
    source_date: string;
    recency: string;
    buckets: string[];
    classification: string;
    confidence: string;
    evidence_paths: string[];
    provenance: Record<string, string[]>;
  }>;
  summary: string[];
  recommendations: string[];
};

export type OpenLoopsDomainPayload = {
  counts: {
    total: number;
    critical: number;
    waiting_for: number;
    stalled_projects: number;
    missing_decisions: number;
    missing_owners: number;
  };
  items: Array<{
    work_item_id: string;
    title: string;
    summary: string;
    source_path: string;
    status: string;
    priority: string;
    owner: string;
    due_date: string;
    source_date: string;
    recency: string;
    buckets: string[];
    classification: string;
    confidence: string;
    related_entities: string[];
    evidence_paths: string[];
    provenance: Record<string, string[]>;
  }>;
  summary: string[];
  recommended_actions: string[];
};

export type DashboardBootstrapPayload = {
  snapshot: SnapshotInfo;
  burning_fires: Array<{ type: string; summary: string }>;
  plan_today: PlanItem[];
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
    summary: string[];
    count: number;
  };
  projects: {
    health: Record<string, number>;
    summary: string[];
    count: number;
  };
  decisions: {
    counts: {
      total: number;
      defined_status: number;
      owner_defined: number;
      source_notes: number;
    };
    summary: string[];
  };
  followups: {
    counts: FollowupsDomainPayload["counts"];
    summary: string[];
    recommendations: string[];
  };
  open_loops: {
    counts: OpenLoopsDomainPayload["counts"];
    summary: string[];
    recommended_actions: string[];
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

export type DashboardPayload = Omit<
  DashboardBootstrapPayload,
  "objectives" | "projects" | "decisions" | "followups" | "open_loops"
> & {
  objectives: ObjectivesDomainPayload;
  projects: ProjectsDomainPayload;
  decisions: DecisionsDomainPayload;
  followups: FollowupsDomainPayload;
  open_loops: OpenLoopsDomainPayload;
};
