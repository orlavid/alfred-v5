# Python Codebase Catalogue

Generated: 2026-06-30T21:41:58.616601


## Purpose

Summarises discovered Python modules, imports, functions and classes.

## Responsibilities

- Provide a searchable engineering inventory.
- Support future architecture documentation generation.
- Expose likely extension points without manual inspection.

## Inputs

- AST parser output
- Python source files

## Outputs

- Module catalogue
- Function inventory
- Class inventory

## Dependencies

- Python source code
- Evidence collector

## Failure Modes

- Syntax warnings from source files.
- Generated catalogue becomes stale if not regenerated after changes.

## Recovery Procedure

- Regenerate engineering evidence pack.
- Review parsing errors in catalogue output.

## Source Evidence

### python/second_brain_python_inventory.json

Size: 322265 bytes

```text
[
  {
    "file": "/opt/second-brain/tests/test_alfred_validators.py",
    "imports": [
      "__future__",
      "pathlib",
      "retrieval",
      "sys",
      "unittest"
    ],
    "functions": [
      "test_valid_compound_daily_answer",
      "test_missing_daily_section_fails",
      "test_generated_source_fails",
      "test_false_inference_fails",
      "test_nonexistent_source_fails",
      "test_invalid_line_fails"
    ],
    "classes": [
      "DailyValidationTests",
      "ObjectiveValidationTests",
      "SourceValidationTests"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/tests/test_alfred_router.py",
    "imports": [
      "__future__",
      "pathlib",
      "retrieval",
      "sys",
      "unittest"
    ],
    "functions": [
      "test_explicit_daily_compound",
      "test_daily_reverse_wording",
      "test_objective_route_is_protected",
      "test_tprm_route",
      "test_cost_route",
      "test_primary_source",
      "test_generated_source",
      "test_primary_only_rejects_generated"
    ],
    "classes": [
      "QueryClassifierTests",
      "SourcePolicyTests"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/tests/run_retrieval_regression.py",
    "imports": [
      "__future__",
      "argparse",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "time",
      "typing"
    ],
    "functions": [
      "normalise",
      "run_one",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/tests/run_routing_paraphrase_matrix.py",
    "imports": [
      "__future__",
      "json",
      "pathlib",
      "retrieval",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/reporting/render_report.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "render_dashboard"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/alfred_router.py",
    "imports": [
      "__future__",
      "argparse",
      "audit",
      "classifiers",
      "datetime",
      "hashlib",
      "json",
      "os",
      "pathlib",
      "strategies",
      "sys",
      "time",
      "typing",
      "validators"
    ],
    "functions": [
      "utc_now",
      "output_hash",
      "parse_args",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/source_policy.py",
    "imports": [
      "__future__",
      "dataclasses"
    ],
    "functions": [
      "classify_source",
      "allowed_for_policy"
    ],
    "classes": [
      "SourceClassification"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/__init__.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": "Alfred structured retrieval and routing package."
  },
  {
    "file": "/opt/second-brain/retrieval/models.py",
    "imports": [
      "__future__",
      "dataclasses",
      "typing"
    ],
    "functions": [
      "to_dict"
    ],
    "classes": [
      "RouteDecision"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/validators.py",
    "imports": [
      "__future__",
      "dataclasses",
      "models",
      "pathlib",
      "re",
      "subprocess",
      "typing"
    ],
    "functions": [
      "_normalise_cited_path",
      "_extract_sources",
      "_validate_source",
      "_contains_forbidden_source",
      "_has_no_evidence_claim",
      "_has_false_inference_claim",
      "_has_obvious_unsupported_target",
      "_lexical_evidence_exists",
      "_count_markers",
      "_require_headings",
      "_validate_daily",
      "_validate_objectives",
      "_validate_cost",
      "_validate_tprm",
      "validate_answer",
      "to_dict"
    ],
    "classes": [
      "ValidationResult"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/strategies.py",
    "imports": [
      "__future__",
      "dataclasses",
      "models",
      "os",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "_run",
      "deterministic_daily_log",
      "protected_legacy",
      "execute_strategy"
    ],
    "classes": [
      "StrategyResult"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/audit.py",
    "imports": [
      "__future__",
      "fcntl",
      "json",
      "pathlib",
      "typing"
    ],
    "functions": [
      "append_audit"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/retrieval/classifiers.py",
    "imports": [
      "__future__",
      "models",
      "re"
    ],
    "functions": [
      "_daily_sections",
      "_date_reference",
      "classify_query"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/gui/server.py",
    "imports": [
      "datetime",
      "email",
      "html",
      "http",
      "json",
      "math",
      "os",
      "ownership_router",
      "pathlib",
      "re",
      "secrets",
      "subprocess",
      "sys",
      "time",
      "urllib"
    ],
    "functions": [
      "load_auth_env",
      "load_auth_state",
      "save_auth_state",
      "now_ts",
      "send_magic_link",
      "esc",
      "shell",
      "file_table",
      "load_state",
      "save_state",
      "registry_page",
      "ai_format_entity",
      "trading_dashboard_files",
      "trading_title",
      "explain_trading_score_html",
      "trading_concentration_fingerprint",
      "inject_trading_concentration_review",
      "count_files",
      "latest_file_time",
      "executive_home",
      "briefing_table",
      "chat_page",
      "run_chat",
      "eos_load_json",
      "eos_write_json",
      "workflow_now",
      "operation_id",
      "operation_entry_defaults",
      "append_operation",
      "start_operation",
      "update_operation",
      "load_operation_events",
      "operations_latest",
      "operation_timeline",
      "latest_operation",
      "operations_worker_script",
      "process_operation_now",
      "retry_operation",
      "terminal_operation_update",
      "handle_operation_control",
      "operation_control_buttons",
      "advisory_memo_engine_script",
      "advisory_memo_index",
      "advisory_source_key",
      "latest_advisory_memo_summary",
      "safe_advisory_memo_path",
      "advisory_source_type",
      "advisory_payload_for",
      "advisory_memo_controls",
      "run_advisory_memo_generation",
      "handle_advisory_memo_action",
      "memo_text",
      "memo_sentences",
      "memo_paragraph",
      "render_paragraph_section",
      "render_supporting_value",
      "advisory_memo_metadata",
      "render_advisory_memo_sections",
      "render_executive_briefing_memo",
      "advisory_memo_page",
      "normalised_operation_output_link",
      "safe_operation_output_path",
      "review_list",
      "operation_output_page",
      "run_tracked_subprocess",
      "operation_monitor_counts",
      "operation_status_badge",
      "operation_monitor_page",
      "operation_detail_page",
      "load_workflow_state",
      "save_workflow_state",
      "workflow_key",
      "workflow_item",
      "canonical_lifecycle_state",
      "lifecycle_is_active",
      "lifecycle_is_history",
      "lifecycle_target_state",
      "lifecycle_audit_entry",
      "route_governance_owner",
      "explicit_owner_value",
      "apply_record_lifecycle",
      "record_workflow_event",
      "governance_activity_entry",
      "governance_record_title",
      "governance_record_description",
      "append_governance_activity",
      "workflow_history_for",
      "render_activity_history",
      "update_workflow_object",
      "governance_action_path",
      "governance_escalation_path",
      "daily_governance_index_path",
      "daily_governance_state_path",
      "normalize_governance_escalation_status",
      "load_governance_escalation_registry",
      "save_governance_escalation_registry",
      "normalize_governance_escalation_record",
      "governance_escalation_records",
      "governance_escalation_candidate_records",
      "update_governance_escalations",
      "create_governance_escalation",
      "promote_governance_attention_to_escalation",
      "update_governance_actions",
      "governance_registry_config",
      "update_governance_register_records",
      "create_governance_action",
      "item_detail_href",
      "eos_count",
      "eos_objectives",
      "eos_objective_status",
      "eos_objectives_summary_html",
      "eos_dashboard_counts",
      "eos_intelligence",
      "objective_console_status",
      "objective_console_confidence",
      "objective_console_agent_status",
      "objective_console_records",
      "objective_console_record",
      "objective_console_contributors",
      "objective_console_improvement_actions",
      "objective_operation_outputs",
      "objective_recommendation_valid",
      "objective_recommendation_from_output",
      "objective_console_recommendations",
      "objective_console_agent_views",
      "objective_console_action_buttons",
      "objective_console_detail_page",
      "objective_operating_console_page",
      "handle_objective_console_action",
      "eos_recent_activity_html",
      "eos_people_company_html",
      "eos_objective_intelligence_page",
      "alfred_execution_edit_page",
      "alfred_lifecycle_data",
      "alfred_technical_debt_data",
      "alfred_technical_debt_page",
      "alfred_board_session_data",
      "alfred_board_session_page",
      "alfred_board_secretary_data",
      "alfred_board_secretary_page",
      "alfred_executive_committee_data",
      "alfred_executive_committee_page",
      "alfred_ai_agent_debate_data",
      "alfred_ai_agent_debate_page",
      "ai_office_nav",
      "ai_office_preamble",
      "alfred_ai_executive_office_page",
      "alfred_executive_ai_briefing_data",
      "alfred_executive_ai_briefing_page",
      "alfred_ai_agent_reviews_data",
      "alfred_agent_workspace_page",
      "alfred_agent_triage_data",
      "alfred_agent_triage_summary",
      "alfred_agent_triage_page",
      "alfred_governance_intelligence_data",
      "governance_attention_record_id",
      "governance_attention_records",
      "governance_escalations_page",
      "alfred_governance_intelligence_page",
      "alfred_dashboard_cache",
      "command_centre_severity_rank",
      "command_centre_severity_label",
      "command_centre_action_query",
      "command_centre_action_button",
      "command_centre_action_controls",
      "command_centre_hidden_fields",
      "command_centre_card",
      "command_centre_objective_controls",
      "command_centre_objective_card",
      "command_centre_objective_items",
      "command_centre_governance_items",
      "command_centre_action_items",
      "command_centre_risk_items",
      "command_centre_decision_items",
      "command_centre_open_loop_items",
      "command_centre_portfolio_item",
      "command_centre_daily_record_items",
      "command_centre_items",
      "command_centre_item_list",
      "command_centre_attention_drawer_items",
      "command_centre_attention_panel",
      "command_centre_priority_panel",
      "command_centre_kpi_card",
      "command_centre_radar_segment",
      "command_centre_agent_card",
      "command_centre_handle_action",
      "create_objective_reevaluation_request",
      "alfred_objective_reevaluation_feedback_page",
      "alfred_objective_reevaluation_status_page",
      "alfred_dashboard_cached_page",
      "alfred_dashboard_v2",
      "alfred_execution_page",
      "alfred_sitemap_page",
      "alfred_administration_page",
      "alfred_overnight_jobs_data",
      "alfred_overnight_jobs_page",
      "alfred_health_dashboard_data",
      "alfred_rag_badge",
      "alfred_health_dashboard_page",
      "alfred_access_data",
      "alfred_access_allowed",
      "alfred_access_page",
      "alfred_reflection_intelligence_page",
      "alfred_actions_data",
      "alfred_objectives_options",
      "alfred_action_edit_page",
      "update_legacy_action_record",
      "alfred_ownership_page",
      "alfred_daily_governance_data",
      "alfred_daily_type_label",
      "markdown_excerpt_for_daily_record",
      "alfred_daily_governance_page",
      "update_daily_records",
      "update_agent_recommendations",
      "update_open_loop_lifecycle",
      "update_workflow_lifecycle",
      "apply_lifecycle_transition",
      "apply_batch_lifecycle_transition",
      "handle_functional_lifecycle_action",
      "handle_functional_lifecycle_batch_action",
      "alfred_governance_edit_page",
      "handle_governance_save",
      "governance_record_is_visible",
      "alfred_governance_workspace_page",
      "alfred_board_minutes_page",
      "alfred_board_capture_page",
      "alfred_board_pack_data",
      "alfred_status_badge",
      "alfred_board_pack_page",
      "alfred_org_data",
      "alfred_org_operational_counts",
      "alfred_owner_key_for_profile",
      "org_preview_0812",
      "org_preview_1017",
      "org_preview_1020",
      "alfred_titan_rca_data",
      "alfred_titan_rca_for_id",
      "alfred_titan_find_record",
      "alfred_titan_outcome_detail_page",
      "alfred_titan_outcomes_page",
      "alfred_titan_incidents_page",
      "alfred_athena_governance_watch_page",
      "athena_apply_finding_action",
      "alfred_athena_finding_detail_page",
      "alfred_titan_rca_page",
      "alfred_titan_metrics_page",
      "alfred_titan_data",
      "alfred_titan_control_page",
      "load_first_json",
      "load_canonical_identity_contract",
      "load_organisation_profiles",
      "load_jsonl_records",
      "canonical_identity_records",
      "canonical_identity_index",
      "organisation_profile_index",
      "canonical_profile_id_map",
      "resolve_profile_for_canonical_id",
      "portrait_directory_candidates",
      "resolve_portrait_filename",
      "resolve_identity_portrait",
      "identity_aliases",
      "matches_identity",
      "active_workload_items",
      "workload_items_for_identity",
      "authority_text",
      "authority_rights_text",
      "authority_delegation_text",
      "operating_cadence_text",
      "profile_human_detail",
      "render_identity_workload_html",
      "render_profile_detail",
      "alfred_agent_directory_page",
      "alfred_organisation_chart_page",
      "alfred_authority_matrix_page",
      "alfred_workload_view_page",
      "alfred_agent_profile_page",
      "alfred_clean_organisation_page",
      "org_preview_1124",
      "alfred_org_page",
      "alfred_metrics",
      "alfred_metric_rows",
      "alfred_status_icon",
      "alfred_kpi_cards_html",
      "alfred_executive_summary_html",
      "alfred_executive_metrics_page",
      "eos_home_body",
      "eos_objectives_page",
      "alfred_org_chart_page",
      "alfred_board_office_intelligence_data",
      "alfred_board_decision_queue_data",
      "alfred_echo_timeline_data",
      "alfred_board_decision_queue_page",
      "alfred_board_decision_detail_page",
      "alfred_board_decision_lifecycle_page",
      "alfred_echo_timeline_page",
      "alfred_echo_timeline_detail_page",
      "alfred_executive_committee_review_data",
      "alfred_executive_committee_page",
      "alfred_executive_committee_review_page",
      "alfred_executive_committee_member_page",
      "alfred_strategic_memory_page",
      "alfred_agent_council_page",
      "alfred_board_office_intelligence_page",
      "eos_board_page",
      "eos_emergency_board_page",
      "create_emergency_board_session",
      "eos_governance_page",
      "load_agent_registry",
      "latest_matching_file",
      "agents_page",
      "run_agent_council",
      "ask_specific_agent",
      "canonical_agent_slug",
      "agent_review_buttons",
      "contextual_engine_script",
      "agent_outputs_dir",
      "load_agent_review_history",
      "safe_agent_output_path",
      "review_mode_label",
      "first_review_value",
      "review_output_parts",
      "summarize_review_evidence",
      "executive_review_summary",
      "alfred_agent_review_history_page",
      "alfred_agent_review_output_page",
      "render_agent_review_result_page",
      "render_agent_review_provenance",
      "run_contextual_agent_review",
      "alfred_agent_context_review_page",
      "load_open_loops",
      "save_open_loops",
      "load_open_loop_archive",
      "save_open_loop_archive",
      "open_loop_record",
      "open_loop_edit_page",
      "handle_open_loop_save",
      "governance_attention_edit_page",
      "handle_governance_attention_save",
      "open_loop_display_record",
      "open_loop_matches_filters",
      "open_loops_manager",
      "main",
      "render_value",
      "rows_for",
      "block",
      "ul",
      "table",
      "opts",
      "is_open",
      "due",
      "card",
      "rows",
      "batch_form",
      "block",
      "kpi",
      "item_table",
      "card",
      "table",
      "page_url",
      "get_cookie",
      "authorised",
      "login_page",
      "require_auth",
      "send_html",
      "redirect",
      "do_GET",
      "do_POST",
      "bullets",
      "list_html",
      "list_html",
      "list_html",
      "list_html",
      "list_html"
    ],
    "classes": [
      "Handler"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/semantic/index_vault.py",
    "imports": [
      "faiss",
      "hashlib",
      "json",
      "numpy",
      "pathlib",
      "re",
      "sentence_transformers"
    ],
    "functions": [
      "clean_text",
      "chunk_text"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/semantic/search_vault_server.py",
    "imports": [
      "faiss",
      "http",
      "json",
      "numpy",
      "pathlib",
      "sentence_transformers",
      "sys",
      "urllib"
    ],
    "functions": [
      "do_GET",
      "log_message"
    ],
    "classes": [
      "Handler"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/semantic/search_vault.py",
    "imports": [
      "faiss",
      "json",
      "numpy",
      "pathlib",
      "sentence_transformers",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_resolver.py",
    "imports": [
      "__future__",
      "argparse",
      "dataclasses",
      "json",
      "pathlib",
      "sys",
      "typing"
    ],
    "functions": [
      "main",
      "can_execute_as_agent",
      "to_dict",
      "__init__",
      "default_root",
      "_load_json",
      "normalise",
      "_build_alias_index",
      "local_path",
      "resolve",
      "resolve_agent",
      "resolve_agent_id",
      "validate_authority",
      "validate_domain",
      "all_aliases",
      "add"
    ],
    "classes": [
      "AgentResolutionError",
      "AgentAuthorityError",
      "AgentDomainError",
      "ResolvedIdentity",
      "AgentResolver"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_operating_rhythm.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "datetime",
      "pathlib",
      "run_daily_executive_briefing",
      "run_executive_council",
      "run_monthly_governance_review",
      "shutil",
      "sys",
      "tempfile",
      "typing"
    ],
    "functions": [
      "repo_second_brain_root",
      "make_temp_root",
      "assert_true",
      "seed_queue",
      "unique_values",
      "validate",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/trading_governance_synthesis.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/open_loop_review.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/close_agent_task.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "json",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/morning_briefing.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/knowledge_service.py",
    "imports": [
      "json",
      "pathlib",
      "time",
      "urllib"
    ],
    "functions": [
      "read_file",
      "norm",
      "score_name",
      "get_note",
      "get_recent_changes",
      "find_best_notes",
      "get_objectives",
      "get_open_loops",
      "get_company",
      "get_person",
      "get_project",
      "get_risks",
      "get_decisions",
      "get_executive_state",
      "scan_base"
    ],
    "classes": [
      "KnowledgeService"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/direct_reference_search.py",
    "imports": [
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "extract_terms",
      "excluded",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_signal_engine.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/governance_lifecycle.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "update"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/daily_synthesis.py",
    "imports": [
      "datetime",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ai_agent_review_layer.py",
    "imports": [
      "agent_resolver",
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "call_hermes",
      "fallback_review",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/governance_lifecycle_review.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/lexical_vault_search.py",
    "imports": [
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "clean_query",
      "query_terms",
      "matching_snippets",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hybrid_openrouter.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "load_env",
      "call_openrouter",
      "call_model_choice",
      "semantic_context",
      "infer_agent",
      "load_learning_hint",
      "recommend",
      "build_prompt",
      "run",
      "debate",
      "chain",
      "feedback",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/athena_governance_review.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "parse_dt",
      "age_days",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_resolver.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "norm",
      "excluded",
      "candidate_phrases",
      "score_path",
      "read_excerpt",
      "recent_dated_sections",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/open_loop_manager_patch.py",
    "imports": [
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_delegation_queue.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "pathlib",
      "shutil",
      "tempfile"
    ],
    "functions": [
      "fail",
      "require",
      "prepare_temp_root",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_synthesis.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "read_tail"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/link_related.py",
    "imports": [
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_intelligence.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/open_loop_escalation.py",
    "imports": [
      "collections",
      "contextual_recommendation_engine",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "contextualize",
      "normalise_previous_record",
      "safe_seen_count",
      "preserve_ux02_fields"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/init_open_loop_register.py",
    "imports": [
      "datetime",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/approve_loop_candidate.py",
    "imports": [
      "pathlib",
      "re",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/extract_entities_ai.py",
    "imports": [
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_action_triage.py",
    "imports": [
      "datetime",
      "json",
      "ownership_router",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "infer_owner",
      "closure_recommendation",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/action_register.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "normalise_action",
      "update",
      "close",
      "reopen",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/cost_evidence_search.py",
    "imports": [
      "__future__",
      "collections",
      "pathlib",
      "re"
    ],
    "functions": [
      "candidate_files",
      "path_priority",
      "score",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/generate_domain_briefing.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "read",
      "recent_matching_files",
      "ask_hermes",
      "generate_one"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_council_action.py",
    "imports": [
      "agent_resolver",
      "agent_task_queue",
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/extract_entities.py",
    "imports": [
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/orchestrate_agents.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_consolidation.py",
    "imports": [
      "collections",
      "datetime",
      "difflib",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "clean",
      "normalise",
      "acronym"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_capture.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "next_id",
      "add_decision",
      "add_risk",
      "add_action",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/email_daily_change_briefing.py",
    "imports": [
      "datetime",
      "email",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "load_env"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/access_control.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "norm",
      "valid",
      "add",
      "remove",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/open_loop.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "read",
      "write",
      "next_id",
      "add_loop",
      "list_loops",
      "close_loop",
      "show"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/email_daily_briefing.py",
    "imports": [
      "datetime",
      "email",
      "markdown",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "load_env",
      "markdown_to_html",
      "send_briefing"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/query_memory.py",
    "imports": [
      "json",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "urllib"
    ],
    "functions": [
      "classify_intent",
      "classify_entity",
      "run",
      "keyword_hits"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/build_reporting_evidence_bundle.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "read"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/run_monthly_governance_review.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "collections",
      "datetime",
      "json",
      "pathlib",
      "run_executive_council",
      "sys",
      "typing",
      "uuid"
    ],
    "functions": [
      "now",
      "parse_date",
      "is_open",
      "stale_actions",
      "count_by",
      "council_effectiveness",
      "build_review",
      "task_line",
      "write_review",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/autonomous_watchlist.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "run_chain",
      "materiality_score",
      "should_create_open_loop",
      "write_watchlist_report",
      "write_open_loop",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/delegation_engine.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/run_executive_council.py",
    "imports": [
      "__future__",
      "agent_resolver",
      "agent_task_queue",
      "argparse",
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality",
      "subprocess",
      "sys",
      "typing",
      "uuid"
    ],
    "functions": [
      "now",
      "default_root",
      "load_jsonl",
      "append_jsonl",
      "generate_run_id",
      "split_csv",
      "mode_defaults",
      "select_by_domain",
      "resolve_unique",
      "fallback_agent_view",
      "live_agent_view",
      "derive_agreements",
      "derive_disagreements",
      "create_action_tasks",
      "write_markdown_summary",
      "run_council",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/update_open_loops.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_memory.py",
    "imports": [
      "datetime",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/unresolved_intelligence_report.py",
    "imports": [
      "datetime",
      "html",
      "pathlib"
    ],
    "functions": [
      "esc",
      "cls"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_reset_circuit_breaker.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_executive_council.py",
    "imports": [
      "__future__",
      "agent_resolver",
      "agent_task_queue",
      "pathlib",
      "run_executive_council",
      "shutil",
      "tempfile"
    ],
    "functions": [
      "fail",
      "require",
      "prepare_temp_root",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_watchlists.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "load_entity_state"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/retrieve_memory.py",
    "imports": [
      "json",
      "sys",
      "urllib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/decision_intelligence.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "read"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/image_artifact.py",
    "imports": [
      "base64",
      "datetime",
      "json",
      "os",
      "pathlib",
      "subprocess",
      "sys",
      "urllib"
    ],
    "functions": [
      "load_env_file",
      "semantic_context",
      "openrouter_text",
      "build_visual_spec",
      "extract_prompt",
      "generate_with_openrouter",
      "generate_with_openai",
      "write_vault_record",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_telegram_agent_commands.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "os",
      "pathlib",
      "shutil",
      "telegram_agent_commands",
      "tempfile"
    ],
    "functions": [
      "require",
      "prepare_temp_root",
      "main",
      "__init__",
      "reply_text",
      "__init__",
      "__init__"
    ],
    "classes": [
      "FakeMessage",
      "FakeUpdate",
      "FakeContext"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/daily_governance_index.py",
    "imports": [
      "datetime",
      "json",
      "ownership_router",
      "pathlib"
    ],
    "functions": [
      "now",
      "load_json",
      "save_json",
      "backup_json",
      "next_registry_id",
      "record_provenance",
      "route_record_owner",
      "mark_linked",
      "date_for_file",
      "norm_heading",
      "split_items",
      "extract_from_file",
      "entry_id",
      "discover_files",
      "rebuild",
      "write_markdown",
      "sync_follow_up_actions",
      "sync_open_loops",
      "mutate",
      "create_action_from_record",
      "promote_decision_record",
      "promote_decision_from_record",
      "promote_decisions",
      "promote_all_decisions",
      "promote_problem_from_record",
      "promote_problems",
      "sync_all",
      "main",
      "flush"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hermes_enrich_latest_capture.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_opinions.py",
    "imports": [
      "agent_resolver",
      "datetime",
      "pathlib",
      "sys"
    ],
    "functions": [
      "now",
      "stance",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/perplexity_with_memory.py",
    "imports": [
      "json",
      "os",
      "pathlib",
      "subprocess",
      "sys",
      "urllib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/governance_intelligence.py",
    "imports": [
      "datetime",
      "json",
      "ownership_router",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "parse_date",
      "main",
      "add"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/historical_ingestion_candidates.py",
    "imports": [
      "collections",
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [
      "excluded",
      "score_file"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_council_pack.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess",
      "textwrap"
    ],
    "functions": [
      "ask_once"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/governance_register.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "sys"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "next_id",
      "add_decision",
      "add_risk",
      "add_action",
      "summary",
      "usage",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_ai_briefing.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load",
      "extract_lines",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_secretary.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "call_hermes",
      "fallback",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_committee_review.py",
    "imports": [
      "agent_resolver",
      "collections",
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/recommendation_quality.py",
    "imports": [
      "__future__",
      "datetime",
      "hashlib",
      "json",
      "typing"
    ],
    "functions": [
      "today_plus",
      "stable_id",
      "normalise_agent",
      "default_owner",
      "is_generic_text",
      "confidence_score",
      "build_contract",
      "enrich_record_recommendation",
      "degraded_agent_review",
      "validate_contract",
      "validate_recommendations",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/run_daily_executive_briefing.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "datetime",
      "json",
      "pathlib",
      "run_executive_council",
      "sys",
      "typing",
      "uuid"
    ],
    "functions": [
      "now",
      "parse_date",
      "is_open",
      "priority_rank",
      "load_recent_agent_outputs",
      "recent_council_decisions",
      "build_briefing",
      "task_line",
      "write_briefing",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/telegram_agent_commands.py",
    "imports": [
      "__future__",
      "agent_resolver",
      "agent_task_queue",
      "os",
      "pathlib",
      "run_daily_executive_briefing",
      "run_executive_council",
      "run_monthly_governance_review",
      "sys",
      "typing"
    ],
    "functions": [
      "second_brain_root",
      "ensure_script_path",
      "load_runtime",
      "context_args",
      "safe_handler",
      "format_aliases",
      "agents_response",
      "delegate_response",
      "open_tasks",
      "tasks_response",
      "task_response",
      "council_response",
      "dailybrief_response",
      "govreview_response",
      "register_agent_commands"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/panel_agents.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_rca.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/reflection_intelligence.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_task_queue.py",
    "imports": [
      "__future__",
      "agent_resolver",
      "datetime",
      "json",
      "pathlib",
      "typing",
      "uuid"
    ],
    "functions": [
      "now",
      "default_root",
      "__init__",
      "ensure_storage",
      "load_tasks",
      "save_tasks",
      "generate_task_id",
      "audit_event",
      "resolve_assignment",
      "create_task",
      "get_task",
      "update_task",
      "close_task",
      "write_task_result"
    ],
    "classes": [
      "TaskQueueError",
      "AgentTaskQueue"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/enrich_capture.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "has_any"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_memory_synthesis.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "read",
      "recent_files"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/alfred_overnight_jobs_status.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "run",
      "file_age",
      "rag_from_timer",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ask_hybrid_agent.py",
    "imports": [
      "agent_resolver",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_self_heal.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "run",
      "find_recovery",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/alfred_health_dashboard.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "zoneinfo"
    ],
    "functions": [
      "now",
      "run",
      "file_age_hours",
      "status_from_bool",
      "timer_status",
      "service_status",
      "file_fresh",
      "log_check",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/get_daily_section.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "pathlib",
      "re",
      "sys",
      "zoneinfo"
    ],
    "functions": [
      "normalise_heading",
      "resolve_date",
      "extract_section",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/alfred_board_pack_generator.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "now",
      "load",
      "safe_text",
      "run_if_exists",
      "action_accountability",
      "section",
      "table",
      "build_pack"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/email_markdown_file.py",
    "imports": [
      "email",
      "html",
      "markdown",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/route_agents.py",
    "imports": [
      "agent_resolver",
      "agent_task_queue",
      "argparse",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/curate_entities.py",
    "imports": [
      "collections",
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [
      "norm",
      "safe_filename"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_registry_maintenance.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "load_state",
      "save_state",
      "norm",
      "approved_names",
      "removed_names",
      "extract_companies_from_vault",
      "ai_match_entity",
      "refresh",
      "render_html",
      "init",
      "main",
      "esc",
      "approved_rows",
      "proposed_rows",
      "removed_rows",
      "unmatched_rows"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/intelligence_postprocess.py",
    "imports": [
      "datetime",
      "hashlib",
      "html",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "load_state",
      "save_state",
      "norm",
      "fp",
      "severity",
      "rank",
      "esc",
      "cls",
      "latest_watchlist_files",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/build_knowledge_graph.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "yaml"
    ],
    "functions": [
      "slugify",
      "ensure_entity_page",
      "inject_links"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/chatgpt_bridge.py",
    "imports": [
      "json",
      "knowledge_service",
      "sys"
    ],
    "functions": [
      "emit",
      "executive_state",
      "company",
      "person",
      "project",
      "risks",
      "decisions",
      "open_loops",
      "recent",
      "usage"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/create_agent_task.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "json",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/rebuild_agent_registry.py",
    "imports": [
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "title_from_file",
      "infer_domain",
      "first_meaningful_line"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/task_lifecycle.py",
    "imports": [
      "datetime",
      "hashlib",
      "json",
      "pathlib"
    ],
    "functions": [
      "tid"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/athena_governance_watch.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/process_capture_lifecycle.py",
    "imports": [
      "datetime",
      "pathlib",
      "shutil"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_registry_server.py",
    "imports": [
      "datetime",
      "http",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "load_state",
      "save_state",
      "make_approved_from_match",
      "make_removed_from_match",
      "norm_name",
      "state_dedup",
      "safe_json_extract",
      "ai_format_entity",
      "main",
      "redirect",
      "do_GET",
      "do_POST"
    ],
    "classes": [
      "Handler"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/list_agent_tasks.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "json"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_triage_approve.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "approve",
      "reject"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_session_from_secretary.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "stamp",
      "load",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_memory_action.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ask_with_memory.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_council.py",
    "imports": [
      "agent_resolver",
      "datetime",
      "json",
      "pathlib",
      "recommendation_quality"
    ],
    "functions": [
      "now",
      "load",
      "latest_jsonl"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/second_brain_dashboard_server.py",
    "imports": [
      "datetime",
      "http",
      "json",
      "pathlib",
      "urllib"
    ],
    "functions": [
      "now",
      "esc",
      "load_loops",
      "save_loops",
      "next_id",
      "commands",
      "command_guide_html",
      "reindex",
      "do_GET",
      "do_POST",
      "render"
    ],
    "classes": [
      "H"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_committee.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "call_hermes",
      "fallback",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/classify_recent_captures.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/historical_ingest.py",
    "imports": [
      "datetime",
      "pathlib",
      "re",
      "subprocess"
    ],
    "functions": [
      "is_excluded",
      "safe_name"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hermes_enrich_capture.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "re",
      "subprocess",
      "sys"
    ],
    "functions": [
      "ask_hermes",
      "extract_json",
      "yaml_list"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_memory.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_control.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "allowed_ops",
      "request",
      "approve",
      "reject",
      "execute",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_decision_engine.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save",
      "stable_id",
      "add_event"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/technical_debt_monitor.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/agent_state_scorecard.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/contextual_recommendation_engine.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "hashlib",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "typing"
    ],
    "functions": [
      "now",
      "review_date",
      "runtime_path",
      "safe_read",
      "load_json",
      "save_json",
      "compact_text",
      "stable_id",
      "issue_query",
      "keywords",
      "score_text",
      "normalise_identity",
      "executable_agent_id",
      "json_context_sources",
      "iter_records",
      "search_json_context",
      "vault_roots",
      "search_obsidian_context",
      "run_command",
      "hermes_provider_required",
      "run_hermes_provider",
      "semantic_search",
      "collect_context",
      "should_attempt_openrouter",
      "agent_prompt",
      "call_agent",
      "degraded_view",
      "concrete_fallback_recommendation",
      "run_multi_model_review",
      "section_excerpt",
      "hermes_text_from_views",
      "is_trading_relevant",
      "contains_generic_only",
      "synthesise",
      "infer_owner",
      "source_references",
      "generate_contextual_recommendation",
      "enrich_recommendation_record",
      "run_agent_review",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/retrieval_planner.py",
    "imports": [
      "json",
      "re",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ownership_router.py",
    "imports": [
      "__future__",
      "datetime",
      "typing"
    ],
    "functions": [
      "utc_now",
      "canonical_object_type",
      "clean_owner",
      "is_placeholder_owner",
      "assignment_source_is_manual",
      "assignment_source_is_automatic",
      "automatic_source_hint",
      "owner_is_replaceable",
      "context_text",
      "score_domains",
      "route_owner",
      "apply_ownership_route"
    ],
    "classes": [],
    "docstring": "Canonical Alfred governance ownership router."
  },
  {
    "file": "/opt/second-brain/scripts/alfred_operations_worker.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "time",
      "typing",
      "urllib"
    ],
    "functions": [
      "now",
      "read_json",
      "write_json",
      "append_jsonl",
      "load_events",
      "latest_operations",
      "operation_transition",
      "operation_output_link",
      "agent_output_link",
      "advisory_memo_link",
      "queued_operations",
      "normalised_status",
      "normalised_operation_type",
      "operation_by_id",
      "objective_id_for",
      "find_objective",
      "objective_evidence",
      "current_objective_score",
      "evaluate_objective",
      "concrete_objective_recommendation",
      "hermes_provider_script",
      "parse_json_output",
      "advisory_memo_engine_script",
      "run_executive_advisory_memo",
      "invoke_hermes_provider",
      "invoke_contextual_objective_review",
      "safe_filename",
      "create_action_for_objective",
      "agent_from_operation",
      "run_agent_review",
      "process_operation",
      "process_once",
      "process_operation_id",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/entity_registry.py",
    "imports": [
      "collections",
      "json",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "load_registry",
      "registry_terms",
      "scan_vault",
      "propose",
      "suggest_category",
      "summary",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/objective_evidence_search.py",
    "imports": [
      "collections",
      "pathlib",
      "re"
    ],
    "functions": [
      "excluded",
      "priority",
      "is_generic_objective_text",
      "line_score",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_advisory_memo_engine.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "hashlib",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "typing"
    ],
    "functions": [
      "now",
      "parse_time",
      "safe_filename",
      "stable_hash",
      "load_json",
      "write_json",
      "compact",
      "sentence",
      "scrub_internal_artifacts",
      "sanitize_section_value",
      "source_label",
      "owner_for",
      "score_or_status",
      "hermes_provider_script",
      "invoke_contextual_engine",
      "extract_provenance",
      "context_narrative",
      "multi_model_narrative",
      "option_paragraphs",
      "section_lines",
      "section_text",
      "context_record_count",
      "evidence_considered_text",
      "build_sections",
      "text_for_section",
      "is_generic",
      "contains_internal_artifact",
      "validate_memo_sections",
      "generate_memo",
      "memo_path",
      "latest_index_path",
      "source_key",
      "store_memo",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/propose_loops.py",
    "imports": [
      "datetime",
      "pathlib",
      "subprocess"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hermes_intelligence_provider.py",
    "imports": [
      "__future__",
      "argparse",
      "datetime",
      "hashlib",
      "json",
      "os",
      "pathlib",
      "re",
      "subprocess",
      "sys",
      "typing"
    ],
    "functions": [
      "now",
      "runtime_path",
      "safe_filename",
      "stable_id",
      "compact",
      "load_json",
      "safe_read",
      "write_json",
      "append_jsonl",
      "operation_transition",
      "tokens",
      "score_record",
      "top_related",
      "records_from",
      "advisory_memo_records",
      "open_loop_records",
      "watchlist_findings",
      "obsidian_context",
      "build_context_pack",
      "hybrid_chain_script",
      "build_prompt",
      "run_hybrid_chain",
      "fallback_output",
      "extract_sections",
      "quality_gate",
      "lines",
      "build_result",
      "context_files",
      "context_records_considered",
      "source_references",
      "generate_intelligence",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/semantic_query_fast.py",
    "imports": [
      "json",
      "sys",
      "urllib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ask_agent.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/delegate_request.py",
    "imports": [
      "agent_resolver",
      "agent_task_queue",
      "argparse",
      "datetime",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "choose_agent"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/orchestrate_agents_parallel.py",
    "imports": [
      "concurrent",
      "subprocess",
      "sys"
    ],
    "functions": [
      "run_agent"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/openrouter_research.py",
    "imports": [
      "json",
      "os",
      "pathlib",
      "requests",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/chief_delegate.py",
    "imports": [
      "agent_resolver",
      "agent_task_queue",
      "argparse",
      "concurrent",
      "datetime",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "run_agent"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/update_agent_task.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "json",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/email_intelligence_digest.py",
    "imports": [
      "datetime",
      "email",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "load_env"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/contextual_watchlists.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "subprocess"
    ],
    "functions": [
      "load_registry",
      "load_watchlists",
      "build_prompt",
      "run_chain",
      "extract_severity",
      "should_create_open_loop",
      "write_report",
      "write_open_loop",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/state_registry.py",
    "imports": [
      "datetime",
      "hashlib",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "oid"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_minutes.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "stamp",
      "run_capture",
      "create_minutes"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/run_agent_task.py",
    "imports": [
      "__future__",
      "agent_task_queue",
      "argparse",
      "subprocess",
      "sys"
    ],
    "functions": [
      "build_fallback_output",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/hermes_knowledge_api.py",
    "imports": [
      "http",
      "json",
      "knowledge_service",
      "pathlib",
      "time",
      "urllib"
    ],
    "functions": [
      "read_file",
      "list_recent",
      "norm",
      "score_name",
      "find_best_notes",
      "semantic_search",
      "read_url",
      "write_json",
      "scan_base",
      "do_GET",
      "log_message"
    ],
    "classes": [
      "Handler"
    ],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/strategic_memory_graph.py",
    "imports": [
      "collections",
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "normalise",
      "detect_domain"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ask_agent_with_memory.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/tprm_evidence_search.py",
    "imports": [
      "__future__",
      "collections",
      "pathlib",
      "re"
    ],
    "functions": [
      "candidate_files",
      "path_priority",
      "evidence_score",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_meeting_engine.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "session_id",
      "latest_intel",
      "objective_snapshot",
      "make_session",
      "write_markdown",
      "list_sessions",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/athena_auto_escalation.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "save"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_intelligence_layer.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "now",
      "safe_read",
      "discover_dirs",
      "candidate_files",
      "classify_objectives",
      "title_for_file",
      "make_excerpt",
      "smart_evidence_context",
      "is_low_quality_evidence",
      "score_status",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_metrics_registry.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "trend_for",
      "board_recommendation",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/execution_update.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/board_office_intelligence.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/athena_finding_action.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/validate_agent_identity.py",
    "imports": [
      "__future__",
      "json",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "fail",
      "load_json",
      "local_path",
      "normalise_alias",
      "require_non_empty",
      "scan_known_personas",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_dashboard_cache.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/render_daily_report_design.py",
    "imports": [
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [
      "status_card",
      "write_dashboard",
      "wrap_existing_brief",
      "render_governance_dashboard",
      "render_5am_dashboard",
      "render_reporting_pack_catalogue",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/titan_executor.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "shutil",
      "subprocess"
    ],
    "functions": [
      "now",
      "load_json",
      "write_json",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/executive_knowledge_graph.py",
    "imports": [
      "datetime",
      "json",
      "pathlib",
      "re"
    ],
    "functions": [
      "now",
      "read",
      "classify_objectives",
      "is_bad_signal",
      "has_outcome_language",
      "excerpt_for",
      "discover_files",
      "structured_records",
      "file_records",
      "build_graph",
      "write_outputs",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/ai_agent_debate.py",
    "imports": [
      "datetime",
      "json",
      "pathlib"
    ],
    "functions": [
      "now",
      "load",
      "call_hermes",
      "fallback",
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/scripts/chatgpt_vault_answer.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "bridge"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/second-brain/baselines/2026-06-28/engineering-spec/collect_alfred_inventory.py",
    "imports": [
      "ast",
      "datetime",
      "pathlib"
    ],
    "functions": [
  
```

### python/alfred_v2_python_inventory.json

Size: 619266 bytes

```text
[
  {
    "file": "/opt/alfred-v2/batch.py",
    "imports": [
      "__future__",
      "app",
      "datetime",
      "json",
      "pathlib",
      "sys",
      "traceback"
    ],
    "functions": [
      "_utcnow",
      "run",
      "step"
    ],
    "classes": [],
    "docstring": "Alfred v2 overnight batch runner.\n\nPer the spec Operating Model:\n  3. Overnight batch runs.\n  4. Alfred updates runtime state.\n  5. Morning Brief generated.\n\nOrder matters \u2014 insights are generated FIRST, then the Morning Brief consumes\nthem. Invoked by systemd timers:\n\n  daily   (every night 02:00)  ->  python batch.py daily\n  weekly  (Mon 02:00)          ->  python batch.py weekly\n  monthly (1st of month 02:00) ->  python batch.py monthly\n\nA monthly run implicitly includes weekly + daily; a weekly run includes daily.\nEvery run writes a machine-readable status file to data/last_batch.json and\nprints a summary (captured by journalctl)."
  },
  {
    "file": "/opt/alfred-v2/seed.py",
    "imports": [
      "__future__",
      "app"
    ],
    "functions": [
      "seed"
    ],
    "classes": [],
    "docstring": "Seed Alfred v2 with realistic sample objects so the app is clickable.\n\nIdempotent: only seeds if the DB has no objectives yet. Does NOT call the LLM\n(keeps seeding fast and offline-safe); workspaces/briefs are generated lazily\non first view, which is where the real Hermes calls happen."
  },
  {
    "file": "/opt/alfred-v2/app/auth.py",
    "imports": [
      "__future__",
      "email",
      "json",
      "os",
      "pathlib",
      "secrets",
      "subprocess",
      "time"
    ],
    "functions": [
      "_env",
      "allowed_emails",
      "_load",
      "_save",
      "_now",
      "_prune",
      "request_link",
      "verify_token",
      "session_email",
      "destroy_session"
    ],
    "classes": [],
    "docstring": "Alfred v2 authentication \u2014 passwordless magic-link, echoing Alfred Classic.\n\nSame mechanism Classic uses (/opt/second-brain/gui/server.py):\n  * ALLOWED_EMAILS whitelist\n  * one-time token emailed as a magic link via msmtp (-t)\n  * token expires in TOKEN_MINUTES; verifying it mints a session cookie\n  * session lasts SESSION_HOURS\n\nState persists in data/auth_state.json so logins survive restarts.\nReuses the same SMTP sender (msmtp 'hermes' / orlavid@gmail.com) and, by\ndefault, the SAME allowed-email list as Classic."
  },
  {
    "file": "/opt/alfred-v2/app/engine.py",
    "imports": [
      "__future__",
      "datetime",
      "json"
    ],
    "functions": [
      "_as_text",
      "classify_activity",
      "create_tracked_item_from_activity",
      "gather_evidence",
      "generate_forward_view",
      "_global_state_summary",
      "build_workspace",
      "get_or_build_workspace",
      "converse",
      "generate_morning_brief",
      "_prune_briefs",
      "latest_brief",
      "generate_review",
      "run_board_discussion",
      "add_intelligence",
      "archive_low_priority_intel",
      "overlap"
    ],
    "classes": [],
    "docstring": "Alfred v2 core engine.\n\nImplements the spec's behavioural rules:\n  * Classification Rules (new activity -> tracked item / project / objective / operational)\n  * Morning Brief (FIXED 6-section order, 30-day retention)\n  * Workspace generation (fixed section set, 5 types)\n  * Conversation (context inherited from workspace)\n  * Forward View (3 horizons: Tomorrow / Next 7 Days / Next 30 Days)\n  * External Intelligence (summarise / prioritise / de-noise / archive)\n  * Reviews (weekly / monthly / annual; summary editable, evidence not)\n  * Board Discussion (all enabled agents; auto draft minutes)\n\nHuman-controlled write-back: nothing here writes to Obsidian. Saving is an\nexplicit, separate user action handled by app.obsidian.save()."
  },
  {
    "file": "/opt/alfred-v2/app/watchlist.py",
    "imports": [
      "__future__",
      "json",
      "os",
      "pathlib",
      "re"
    ],
    "functions": [
      "available",
      "_norm_summary",
      "_rank",
      "load_findings",
      "external_intelligence",
      "briefing_lines",
      "evidence_text"
    ],
    "classes": [],
    "docstring": "Watchlist bridge \u2014 connects Alfred Classic's daily watchlist to Alfred v2's\nExternal Intelligence (per the spec's External Intelligence behaviour:\nSummarise / Prioritise / Remove noise / Archive automatically).\n\nREAD-ONLY. v2 never writes to Classic's watchlist state. The watchlist is the\nlive feed; v2 derives its External Intelligence view from it at read time.\n\nSource: /opt/second-brain/state/intelligence/watchlist_state.json\n  shape: {\"findings\": {<key>: {first_seen,last_seen,seen_count,severity,\n                                status,watchlist,report_path,summary}}, \"runs\":[...]}"
  },
  {
    "file": "/opt/alfred-v2/app/obsidian.py",
    "imports": [
      "__future__",
      "datetime",
      "pathlib",
      "re"
    ],
    "functions": [
      "_slug",
      "ensure_structure",
      "_is_within",
      "save",
      "search_vault",
      "recent_notes",
      "_yaml_val"
    ],
    "classes": [],
    "docstring": "Obsidian layer for Alfred v2.\n\nREAD: Alfred v2 may read the entire vault.\nWRITE: Alfred v2 may write NEW FILES ONLY, and ONLY under\n       07 AI Memory/Alfred v2/<category>/, and ONLY on explicit user approval\n       (\"Save to Obsidian\").\n\nHard guarantees enforced here (defence in depth, per spec write-back rules):\n  * Never write outside VAULT_WRITE_ROOT.\n  * Never overwrite an existing file (new files only) unless allow_overwrite.\n  * Never touch Daily Notes, existing Projects/Objectives, historical notes,\n    or source evidence."
  },
  {
    "file": "/opt/alfred-v2/app/insights.py",
    "imports": [
      "__future__",
      "datetime",
      "json"
    ],
    "functions": [
      "_today",
      "_parse_insights_json",
      "_store",
      "_degraded_item",
      "_daily_evidence",
      "_objective_project_state",
      "generate_daily_insights",
      "generate_weekly_insights",
      "generate_monthly_insights",
      "unconsumed_daily_insights",
      "mark_consumed",
      "recent"
    ],
    "classes": [],
    "docstring": "Alfred v2 Insight Engine.\n\nInsights are the OUTPUT of the overnight batch and the INPUT to the Morning\nBrief. They are first-class, drillable, save-able objects generated on three\ncadences, each with its own specification:\n\n  DAILY   \u2014 runs every night. Examines: yesterday's daily notes, new/changed\n            tracked items, open loops, and active external intelligence.\n            Produces: tactical \"what changed / what needs attention today\"\n            insights. These FEED that morning's brief (feeds_brief=1).\n\n  WEEKLY  \u2014 rolls up the last 7 days of DAILY insights + objective/project\n            health + the week's tracked-item closures. Produces pattern-level\n            insights (drift, recurring risk, momentum). Feeds the Weekly Review\n            and Monday's brief.\n\n  MONTHLY \u2014 rolls up the month's WEEKLY insights + objective progress vs intent.\n            Produces strategic insights. Feeds the Monthly Review.\n\nCascade: weekly consumes daily; monthly consumes weekly. Every insight records\n`rolled_up_from` (source insight ids) so the derivation is drillable.\n\nAll generation is evidence-led and degrades gracefully (explicitly labelled) if\nthe Hermes/OpenRouter path is unavailable \u2014 never fabricated."
  },
  {
    "file": "/opt/alfred-v2/app/agents.py",
    "imports": [
      "__future__",
      "json"
    ],
    "functions": [
      "seed_agents",
      "enabled_agents",
      "_prompt",
      "run_agent",
      "run_panel",
      "outputs_for"
    ],
    "classes": [],
    "docstring": "Agent framework for Alfred v2.\n\nCore Agents (spec): Alfred, Chief of Staff, Risk, Governance, Delivery,\nIntelligence, Knowledge, Strategy, Architecture, Compliance.\nUsers may create additional agents.\n\nEach agent produces drillable outputs: observations, recommendations, risks,\nchallenges, minority views. Outputs are persisted per object so individual\nagent opinions are drillable."
  },
  {
    "file": "/opt/alfred-v2/app/__init__.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": "Alfred v2 application package."
  },
  {
    "file": "/opt/alfred-v2/app/db.py",
    "imports": [
      "__future__",
      "contextlib",
      "datetime",
      "json",
      "pathlib",
      "sqlite3",
      "typing"
    ],
    "functions": [
      "now",
      "connect",
      "init_db",
      "insert",
      "update",
      "get",
      "query",
      "all_rows",
      "jdump",
      "jload"
    ],
    "classes": [],
    "docstring": "SQLite runtime state for Alfred v2.\n\nPer spec: SQLite = Runtime State, and Alfred v2 uses a SEPARATE runtime\ndatabase from Alfred Classic. This file is the only writer of that DB.\n\nSchema covers every Core Object and feature in the spec:\n  objectives, projects, tracked_items (with classification), operational_items,\n  agents, agent_outputs (observations/recommendations/risks/challenges/minority\n  views \u2014 drillable per agent), workspaces, conversation_messages,\n  reviews (weekly/monthly/annual), board_discussions + board_minutes,\n  forward_view, external_intelligence, morning_briefs (30-day retention),\n  writeback_log (audit of every Save to Obsidian)."
  },
  {
    "file": "/opt/alfred-v2/app/hermes.py",
    "imports": [
      "__future__",
      "json",
      "os",
      "pathlib",
      "urllib"
    ],
    "functions": [
      "_load_env",
      "available",
      "_call",
      "generate"
    ],
    "classes": [],
    "docstring": "Hermes processing layer for Alfred v2.\n\nReuses the SAME OpenRouter convention as the existing Classic hybrid router\n(/opt/second-brain/scripts/hybrid_openrouter.py): same endpoint, same model\nlanes, same fallback discipline, same /root/.openrouter.env credentials.\n\nPer spec: 'Evidence before conclusions' and 'Simplicity over complexity'.\nIf the model path is unavailable the system DEGRADES GRACEFULLY rather than\nfabricating conclusions \u2014 every degraded output is explicitly labelled."
  },
  {
    "file": "/opt/alfred-v2/app/config.py",
    "imports": [
      "__future__",
      "os",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": "Alfred v2 configuration.\n\nSingle-user Executive Operating System. Runs in PARALLEL with Alfred Classic.\n- Obsidian  = Memory (system of record)\n- Alfred    = User Experience (this app)\n- Hermes    = Processing Layer (OpenRouter via the proven hybrid path)\n- SQLite    = Runtime State (separate DB from Classic)"
  },
  {
    "file": "/opt/alfred-v2/app/main.py",
    "imports": [
      "__future__",
      "fastapi",
      "json",
      "pathlib"
    ],
    "functions": [
      "auth_login",
      "auth_request",
      "auth_verify",
      "auth_logout",
      "_startup",
      "page",
      "landing",
      "health",
      "v2_home",
      "v2_brief",
      "v2_brief_generate",
      "v2_object",
      "v2_rebuild",
      "v2_chat",
      "create_objective",
      "create_project",
      "create_tracked",
      "close_tracked",
      "v2_reviews",
      "gen_review",
      "v2_review",
      "edit_review",
      "v2_board",
      "create_board",
      "v2_board_detail",
      "edit_minutes",
      "v2_intel",
      "add_intel",
      "archive_low",
      "v2_search",
      "save_to_obsidian",
      "v2_writeback_log",
      "v2_insights",
      "v2_agents",
      "create_agent",
      "toggle_agent"
    ],
    "classes": [],
    "docstring": "Alfred v2 FastAPI application \u2014 routes + server-rendered UI.\n\nMounts a single landing page (Classic vs v2 selector) at /, and the full\nAlfred v2 workspace-first UX under /v2. All intelligence flows through the\nHermes processing layer; all write-back is explicit (\"Save to Obsidian\")."
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/typing_extensions.py",
    "imports": [
      "_socket",
      "abc",
      "annotationlib",
      "asyncio",
      "builtins",
      "collections",
      "contextlib",
      "enum",
      "functools",
      "inspect",
      "io",
      "keyword",
      "operator",
      "sys",
      "types",
      "typing",
      "warnings"
    ],
    "functions": [
      "IntVar",
      "_get_protocol_attrs",
      "_caller",
      "_set_default",
      "_set_module",
      "_create_concatenate_alias",
      "_concatenate_getitem",
      "_unpack_args",
      "_has_generic_or_protocol_as_origin",
      "_is_unpacked_typevartuple",
      "__repr__",
      "_should_collect_from_parameters",
      "_should_collect_from_parameters",
      "__init__",
      "__getattr__",
      "__mro_entries__",
      "__repr__",
      "__reduce__",
      "__call__",
      "__or__",
      "__ror__",
      "__instancecheck__",
      "__subclasscheck__",
      "__getitem__",
      "__repr__",
      "final",
      "disjoint_base",
      "_flatten_literal_params",
      "_value_and_type_iter",
      "overload",
      "get_overloads",
      "clear_overloads",
      "_is_dunder",
      "_allow_reckless_class_checks",
      "_no_init",
      "_type_check_issubclass_arg_1",
      "_proto_hook",
      "runtime_checkable",
      "_get_typeddict_qualifiers",
      "_create_typeddict",
      "TypedDict",
      "is_typeddict",
      "assert_type",
      "_strip_extras",
      "get_type_hints",
      "_could_be_inserted_optional",
      "_clean_optional",
      "get_origin",
      "get_args",
      "TypeAlias",
      "__instancecheck__",
      "Concatenate",
      "TypeGuard",
      "TypeIs",
      "TypeForm",
      "LiteralString",
      "Self",
      "Never",
      "Required",
      "NotRequired",
      "ReadOnly",
      "_is_unpack",
      "Unpack",
      "_is_unpack",
      "reveal_type",
      "assert_never",
      "dataclass_transform",
      "override",
      "_is_param_expr",
      "_is_param_expr",
      "_check_generic",
      "_check_generic",
      "_collect_type_vars",
      "_collect_parameters",
      "_make_nmtuple",
      "_namedtuple_mro_entries",
      "NamedTuple",
      "get_original_bases",
      "is_protocol",
      "get_protocol_members",
      "get_annotations",
      "_eval_with_owner",
      "evaluate_forward_ref",
      "__init__",
      "__repr__",
      "__getstate__",
      "type_repr",
      "__instancecheck__",
      "__repr__",
      "__new__",
      "__eq__",
      "__hash__",
      "__init__",
      "__getitem__",
      "__init__",
      "__setattr__",
      "__getitem__",
      "__new__",
      "__init__",
      "__subclasscheck__",
      "__instancecheck__",
      "__eq__",
      "__hash__",
      "__init_subclass__",
      "__int__",
      "__float__",
      "__complex__",
      "__bytes__",
      "__index__",
      "__abs__",
      "__round__",
      "read",
      "write",
      "__setattr__",
      "__new__",
      "__repr__",
      "__reduce__",
      "__new__",
      "__repr__",
      "__reduce__",
      "__new__",
      "__subclasscheck__",
      "__call__",
      "__mro_entries__",
      "__new__",
      "__init_subclass__",
      "__copy__",
      "__deepcopy__",
      "__init__",
      "__repr__",
      "__eq__",
      "__init__",
      "__repr__",
      "__eq__",
      "_type_convert",
      "__init__",
      "__repr__",
      "__hash__",
      "__call__",
      "__parameters__",
      "copy_with",
      "__getitem__",
      "__call__",
      "__init__",
      "__typing_unpacked_tuple_args__",
      "__typing_is_unpacked_typevartuple__",
      "__getitem__",
      "decorator",
      "__init__",
      "__call__",
      "__new__",
      "__call__",
      "__init__",
      "__mro_entries__",
      "__repr__",
      "__reduce__",
      "_is_unionable",
      "_is_unionable",
      "__init__",
      "__setattr__",
      "__delattr__",
      "_raise_attribute_error",
      "__repr__",
      "_check_parameters",
      "__getitem__",
      "__reduce__",
      "__init_subclass__",
      "__call__",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__call__",
      "__or__",
      "__ror__",
      "_tvar_prepare_subst",
      "__new__",
      "__init_subclass__",
      "args",
      "kwargs",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__reduce__",
      "__call__",
      "copy_with",
      "__getitem__",
      "__new__",
      "__init_subclass__",
      "__iter__",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__reduce__",
      "__init_subclass__",
      "__or__",
      "__ror__",
      "__getattr__",
      "_check_single_param",
      "__or__",
      "__ror__",
      "__annotate__",
      "_paramspec_prepare_subst",
      "_typevartuple_prepare_subst",
      "__init_subclass__",
      "__new__",
      "__init_subclass__",
      "__init_subclass__",
      "wrapper"
    ],
    "classes": [
      "_Sentinel",
      "_SpecialForm",
      "_ExtensionsSpecialForm",
      "_DefaultMixin",
      "_TypeVarLikeMeta",
      "_EllipsisDummy",
      "Sentinel",
      "_AnyMeta",
      "Any",
      "_LiteralGenericAlias",
      "_LiteralForm",
      "_SpecialGenericAlias",
      "_ProtocolMeta",
      "Protocol",
      "SupportsInt",
      "SupportsFloat",
      "SupportsComplex",
      "SupportsBytes",
      "SupportsIndex",
      "SupportsAbs",
      "SupportsRound",
      "Reader",
      "Writer",
      "SingletonMeta",
      "NoDefaultType",
      "NoExtraItemsType",
      "_TypedDictMeta",
      "_TypedDictSpecialForm",
      "TypeVar",
      "_Immutable",
      "ParamSpecArgs",
      "ParamSpecKwargs",
      "_ConcatenateGenericAlias",
      "_TypeFormForm",
      "_UnpackSpecialForm",
      "_UnpackAlias",
      "deprecated",
      "_NamedTupleMeta",
      "Buffer",
      "NewType",
      "TypeAliasType",
      "Doc",
      "Format",
      "ParamSpec",
      "ParamSpec",
      "_ConcatenateGenericAlias",
      "TypeVarTuple",
      "TypeVarTuple",
      "_TypeAliasGenericAlias",
      "Dummy"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/concurrency.py",
    "imports": [
      "__future__",
      "anyio",
      "functools",
      "sys",
      "typing",
      "typing_extensions",
      "warnings"
    ],
    "functions": [
      "_next"
    ],
    "classes": [
      "_StopIteration"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/routing.py",
    "imports": [
      "__future__",
      "contextlib",
      "enum",
      "functools",
      "inspect",
      "re",
      "starlette",
      "traceback",
      "types",
      "typing",
      "warnings"
    ],
    "functions": [
      "iscoroutinefunction_or_partial",
      "request_response",
      "websocket_session",
      "get_name",
      "replace_params",
      "compile_path",
      "_wrap_gen_lifespan_context",
      "__init__",
      "matches",
      "url_path_for",
      "__init__",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "routes",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "routes",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "wrapper",
      "__init__",
      "__call__",
      "__init__",
      "url_path_for",
      "__eq__",
      "mount",
      "host",
      "add_route",
      "add_websocket_route",
      "route",
      "websocket_route",
      "add_event_handler",
      "on_event",
      "decorator",
      "decorator",
      "decorator"
    ],
    "classes": [
      "NoMatchFound",
      "Match",
      "BaseRoute",
      "Route",
      "WebSocketRoute",
      "Mount",
      "Host",
      "_AsyncLiftContextManager",
      "_DefaultLifespan",
      "Router"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/templating.py",
    "imports": [
      "__future__",
      "jinja2",
      "os",
      "starlette",
      "typing",
      "warnings"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "_create_env",
      "_setup_env_defaults",
      "get_template",
      "TemplateResponse",
      "TemplateResponse",
      "TemplateResponse",
      "url_for"
    ],
    "classes": [
      "_TemplateResponse",
      "Jinja2Templates"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/requests.py",
    "imports": [
      "__future__",
      "anyio",
      "http",
      "json",
      "multipart",
      "python_multipart",
      "starlette",
      "typing"
    ],
    "functions": [
      "cookie_parser",
      "__init__",
      "__getitem__",
      "__iter__",
      "__len__",
      "app",
      "url",
      "base_url",
      "headers",
      "query_params",
      "path_params",
      "cookies",
      "client",
      "session",
      "auth",
      "user",
      "state",
      "url_for",
      "__init__",
      "method",
      "receive",
      "form"
    ],
    "classes": [
      "ClientDisconnect",
      "HTTPConnection",
      "Request"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/schemas.py",
    "imports": [
      "__future__",
      "inspect",
      "re",
      "starlette",
      "typing",
      "yaml"
    ],
    "functions": [
      "render",
      "get_schema",
      "get_endpoints",
      "_remove_converter",
      "parse_docstring",
      "OpenAPIResponse",
      "__init__",
      "get_schema"
    ],
    "classes": [
      "OpenAPIResponse",
      "EndpointInfo",
      "BaseSchemaGenerator",
      "SchemaGenerator"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/_utils.py",
    "imports": [
      "__future__",
      "contextlib",
      "exceptiongroup",
      "functools",
      "inspect",
      "starlette",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "is_async_callable",
      "is_async_callable",
      "is_async_callable",
      "collapse_excgroups",
      "get_route_path",
      "__init__",
      "__await__"
    ],
    "classes": [
      "AwaitableOrContextManager",
      "SupportsAsyncClose",
      "AwaitableOrContextManagerWrapper"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/status.py",
    "imports": [
      "__future__"
    ],
    "functions": [],
    "classes": [],
    "docstring": "HTTP codes\nSee HTTP Status Code Registry:\nhttps://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml\n\nAnd RFC 2324 - https://tools.ietf.org/html/rfc2324"
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/websockets.py",
    "imports": [
      "__future__",
      "enum",
      "json",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "_raise_on_disconnect",
      "__init__"
    ],
    "classes": [
      "WebSocketState",
      "WebSocketDisconnect",
      "WebSocket",
      "WebSocketClose"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/__init__.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/applications.py",
    "imports": [
      "__future__",
      "starlette",
      "sys",
      "typing",
      "typing_extensions",
      "warnings"
    ],
    "functions": [
      "__init__",
      "build_middleware_stack",
      "routes",
      "url_path_for",
      "on_event",
      "mount",
      "host",
      "add_middleware",
      "add_exception_handler",
      "add_event_handler",
      "add_route",
      "add_websocket_route",
      "exception_handler",
      "route",
      "websocket_route",
      "middleware",
      "decorator",
      "decorator",
      "decorator",
      "decorator"
    ],
    "classes": [
      "Starlette"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/authentication.py",
    "imports": [
      "__future__",
      "functools",
      "inspect",
      "starlette",
      "sys",
      "typing",
      "typing_extensions",
      "urllib"
    ],
    "functions": [
      "has_required_scope",
      "requires",
      "decorator",
      "__init__",
      "is_authenticated",
      "display_name",
      "identity",
      "__init__",
      "is_authenticated",
      "display_name",
      "is_authenticated",
      "display_name",
      "sync_wrapper"
    ],
    "classes": [
      "AuthenticationError",
      "AuthenticationBackend",
      "AuthCredentials",
      "BaseUser",
      "SimpleUser",
      "UnauthenticatedUser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/_exception_handler.py",
    "imports": [
      "__future__",
      "starlette",
      "typing"
    ],
    "functions": [
      "_lookup_exception_handler",
      "wrap_app_handling_exceptions"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/datastructures.py",
    "imports": [
      "__future__",
      "shlex",
      "starlette",
      "typing",
      "urllib"
    ],
    "functions": [
      "__init__",
      "components",
      "scheme",
      "netloc",
      "path",
      "query",
      "fragment",
      "username",
      "password",
      "hostname",
      "port",
      "is_secure",
      "replace",
      "include_query_params",
      "replace_query_params",
      "remove_query_params",
      "__eq__",
      "__str__",
      "__repr__",
      "__new__",
      "__init__",
      "make_absolute_url",
      "__init__",
      "__repr__",
      "__str__",
      "__bool__",
      "__init__",
      "__len__",
      "__getitem__",
      "__iter__",
      "__repr__",
      "__str__",
      "__init__",
      "getlist",
      "keys",
      "values",
      "items",
      "multi_items",
      "__getitem__",
      "__contains__",
      "__iter__",
      "__len__",
      "__eq__",
      "__repr__",
      "__setitem__",
      "__delitem__",
      "pop",
      "popitem",
      "poplist",
      "clear",
      "setdefault",
      "setlist",
      "append",
      "update",
      "__init__",
      "__str__",
      "__repr__",
      "__init__",
      "content_type",
      "_in_memory",
      "__repr__",
      "__init__",
      "__init__",
      "raw",
      "keys",
      "values",
      "items",
      "getlist",
      "mutablecopy",
      "__getitem__",
      "__contains__",
      "__iter__",
      "__len__",
      "__eq__",
      "__repr__",
      "__setitem__",
      "__delitem__",
      "__ior__",
      "__or__",
      "raw",
      "setdefault",
      "update",
      "append",
      "add_vary_header",
      "__init__",
      "__setattr__",
      "__getattr__",
      "__delattr__"
    ],
    "classes": [
      "Address",
      "URL",
      "URLPath",
      "Secret",
      "CommaSeparatedStrings",
      "ImmutableMultiDict",
      "MultiDict",
      "QueryParams",
      "UploadFile",
      "FormData",
      "Headers",
      "MutableHeaders",
      "State"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/types.py",
    "imports": [
      "starlette",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/exceptions.py",
    "imports": [
      "__future__",
      "collections",
      "http"
    ],
    "functions": [
      "__init__",
      "__str__",
      "__repr__",
      "__init__",
      "__str__",
      "__repr__"
    ],
    "classes": [
      "HTTPException",
      "WebSocketException"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/formparsers.py",
    "imports": [
      "__future__",
      "dataclasses",
      "enum",
      "multipart",
      "python_multipart",
      "starlette",
      "tempfile",
      "typing",
      "urllib"
    ],
    "functions": [
      "_user_safe_decode",
      "__init__",
      "__init__",
      "on_field_start",
      "on_field_name",
      "on_field_data",
      "on_field_end",
      "on_end",
      "__init__",
      "on_part_begin",
      "on_part_data",
      "on_part_end",
      "on_header_field",
      "on_header_value",
      "on_header_end",
      "on_headers_finished",
      "on_end"
    ],
    "classes": [
      "FormMessage",
      "MultipartPart",
      "MultiPartException",
      "FormParser",
      "MultiPartParser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/config.py",
    "imports": [
      "__future__",
      "os",
      "pathlib",
      "typing",
      "warnings"
    ],
    "functions": [
      "__init__",
      "__getitem__",
      "__setitem__",
      "__delitem__",
      "__iter__",
      "__len__",
      "__init__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "get",
      "_read_file",
      "_perform_cast"
    ],
    "classes": [
      "undefined",
      "EnvironError",
      "Environ",
      "Config"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/background.py",
    "imports": [
      "__future__",
      "starlette",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__init__",
      "__init__",
      "add_task"
    ],
    "classes": [
      "BackgroundTask",
      "BackgroundTasks"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/endpoints.py",
    "imports": [
      "__future__",
      "json",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__await__",
      "__init__",
      "__await__"
    ],
    "classes": [
      "HTTPEndpoint",
      "WebSocketEndpoint"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/testclient.py",
    "imports": [
      "__future__",
      "anyio",
      "concurrent",
      "contextlib",
      "httpx",
      "inspect",
      "io",
      "json",
      "math",
      "starlette",
      "sys",
      "types",
      "typing",
      "typing_extensions",
      "urllib",
      "warnings"
    ],
    "functions": [
      "_is_asgi3",
      "__init__",
      "__init__",
      "__init__",
      "__enter__",
      "__exit__",
      "_raise_on_close",
      "send",
      "send_text",
      "send_bytes",
      "send_json",
      "close",
      "receive",
      "receive_text",
      "receive_bytes",
      "receive_json",
      "__init__",
      "handle_request",
      "__init__",
      "_portal_factory",
      "request",
      "get",
      "options",
      "head",
      "post",
      "put",
      "patch",
      "delete",
      "websocket_connect",
      "__enter__",
      "__exit__",
      "reset_portal",
      "wait_shutdown"
    ],
    "classes": [
      "_WrapASGI2",
      "_AsyncBackend",
      "_Upgrade",
      "WebSocketDenialResponse",
      "WebSocketTestSession",
      "_TestClientTransport",
      "TestClient"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/responses.py",
    "imports": [
      "__future__",
      "anyio",
      "datetime",
      "email",
      "functools",
      "hashlib",
      "http",
      "json",
      "mimetypes",
      "os",
      "re",
      "secrets",
      "starlette",
      "stat",
      "typing",
      "urllib",
      "warnings"
    ],
    "functions": [
      "__init__",
      "render",
      "init_headers",
      "headers",
      "set_cookie",
      "delete_cookie",
      "__init__",
      "render",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "set_stat_headers",
      "_should_use_range",
      "_parse_range_header",
      "generate_multipart"
    ],
    "classes": [
      "Response",
      "HTMLResponse",
      "PlainTextResponse",
      "JSONResponse",
      "RedirectResponse",
      "StreamingResponse",
      "MalformedRangeHeader",
      "RangeNotSatisfiable",
      "FileResponse"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/convertors.py",
    "imports": [
      "__future__",
      "math",
      "typing",
      "uuid"
    ],
    "functions": [
      "register_url_convertor",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string"
    ],
    "classes": [
      "Convertor",
      "StringConvertor",
      "PathConvertor",
      "IntegerConvertor",
      "FloatConvertor",
      "UUIDConvertor"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/starlette/staticfiles.py",
    "imports": [
      "__future__",
      "anyio",
      "email",
      "errno",
      "importlib",
      "os",
      "starlette",
      "stat",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "get_directories",
      "get_path",
      "lookup_path",
      "file_response",
      "is_not_modified"
    ],
    "classes": [
      "NotModifiedResponse",
      "StaticFiles"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/annotated_types/__init__.py",
    "imports": [
      "dataclasses",
      "datetime",
      "math",
      "sys",
      "types",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__gt__",
      "__ge__",
      "__lt__",
      "__le__",
      "__mod__",
      "__div__",
      "__is_annotated_types_grouped_metadata__",
      "__iter__",
      "__iter__",
      "__iter__",
      "__repr__",
      "__call__",
      "__init_subclass__",
      "__iter__",
      "doc"
    ],
    "classes": [
      "SupportsGt",
      "SupportsGe",
      "SupportsLt",
      "SupportsLe",
      "SupportsMod",
      "SupportsDiv",
      "BaseMetadata",
      "Gt",
      "Ge",
      "Lt",
      "Le",
      "GroupedMetadata",
      "Interval",
      "MultipleOf",
      "MinLen",
      "MaxLen",
      "Len",
      "Timezone",
      "Unit",
      "Predicate",
      "Not",
      "DocInfo"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/annotated_types/test_cases.py",
    "imports": [
      "annotated_types",
      "datetime",
      "decimal",
      "math",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "cases",
      "__iter__"
    ],
    "classes": [
      "Case",
      "MyCustomGroupedMetadata"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/_yaml/__init__.py",
    "imports": [
      "sys",
      "warnings",
      "yaml"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/events.py",
    "imports": [],
    "functions": [
      "__init__",
      "__repr__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "Event",
      "NodeEvent",
      "CollectionStartEvent",
      "CollectionEndEvent",
      "StreamStartEvent",
      "StreamEndEvent",
      "DocumentStartEvent",
      "DocumentEndEvent",
      "AliasEvent",
      "ScalarEvent",
      "SequenceStartEvent",
      "SequenceEndEvent",
      "MappingStartEvent",
      "MappingEndEvent"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/nodes.py",
    "imports": [],
    "functions": [
      "__init__",
      "__repr__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "Node",
      "ScalarNode",
      "CollectionNode",
      "SequenceNode",
      "MappingNode"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/parser.py",
    "imports": [
      "error",
      "events",
      "scanner",
      "tokens"
    ],
    "functions": [
      "__init__",
      "dispose",
      "check_event",
      "peek_event",
      "get_event",
      "parse_stream_start",
      "parse_implicit_document_start",
      "parse_document_start",
      "parse_document_end",
      "parse_document_content",
      "process_directives",
      "parse_block_node",
      "parse_flow_node",
      "parse_block_node_or_indentless_sequence",
      "parse_node",
      "parse_block_sequence_first_entry",
      "parse_block_sequence_entry",
      "parse_indentless_sequence_entry",
      "parse_block_mapping_first_key",
      "parse_block_mapping_key",
      "parse_block_mapping_value",
      "parse_flow_sequence_first_entry",
      "parse_flow_sequence_entry",
      "parse_flow_sequence_entry_mapping_key",
      "parse_flow_sequence_entry_mapping_value",
      "parse_flow_sequence_entry_mapping_end",
      "parse_flow_mapping_first_key",
      "parse_flow_mapping_key",
      "parse_flow_mapping_value",
      "parse_flow_mapping_empty_value",
      "process_empty_scalar"
    ],
    "classes": [
      "ParserError",
      "Parser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/tokens.py",
    "imports": [],
    "functions": [
      "__init__",
      "__repr__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "Token",
      "DirectiveToken",
      "DocumentStartToken",
      "DocumentEndToken",
      "StreamStartToken",
      "StreamEndToken",
      "BlockSequenceStartToken",
      "BlockMappingStartToken",
      "BlockEndToken",
      "FlowSequenceStartToken",
      "FlowMappingStartToken",
      "FlowSequenceEndToken",
      "FlowMappingEndToken",
      "KeyToken",
      "ValueToken",
      "BlockEntryToken",
      "FlowEntryToken",
      "AliasToken",
      "AnchorToken",
      "TagToken",
      "ScalarToken"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/emitter.py",
    "imports": [
      "error",
      "events"
    ],
    "functions": [
      "__init__",
      "__init__",
      "dispose",
      "emit",
      "need_more_events",
      "need_events",
      "increase_indent",
      "expect_stream_start",
      "expect_nothing",
      "expect_first_document_start",
      "expect_document_start",
      "expect_document_end",
      "expect_document_root",
      "expect_node",
      "expect_alias",
      "expect_scalar",
      "expect_flow_sequence",
      "expect_first_flow_sequence_item",
      "expect_flow_sequence_item",
      "expect_flow_mapping",
      "expect_first_flow_mapping_key",
      "expect_flow_mapping_key",
      "expect_flow_mapping_simple_value",
      "expect_flow_mapping_value",
      "expect_block_sequence",
      "expect_first_block_sequence_item",
      "expect_block_sequence_item",
      "expect_block_mapping",
      "expect_first_block_mapping_key",
      "expect_block_mapping_key",
      "expect_block_mapping_simple_value",
      "expect_block_mapping_value",
      "check_empty_sequence",
      "check_empty_mapping",
      "check_empty_document",
      "check_simple_key",
      "process_anchor",
      "process_tag",
      "choose_scalar_style",
      "process_scalar",
      "prepare_version",
      "prepare_tag_handle",
      "prepare_tag_prefix",
      "prepare_tag",
      "prepare_anchor",
      "analyze_scalar",
      "flush_stream",
      "write_stream_start",
      "write_stream_end",
      "write_indicator",
      "write_indent",
      "write_line_break",
      "write_version_directive",
      "write_tag_directive",
      "write_single_quoted",
      "write_double_quoted",
      "determine_block_hints",
      "write_folded",
      "write_literal",
      "write_plain"
    ],
    "classes": [
      "EmitterError",
      "ScalarAnalysis",
      "Emitter"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/scanner.py",
    "imports": [
      "error",
      "tokens"
    ],
    "functions": [
      "__init__",
      "__init__",
      "check_token",
      "peek_token",
      "get_token",
      "need_more_tokens",
      "fetch_more_tokens",
      "next_possible_simple_key",
      "stale_possible_simple_keys",
      "save_possible_simple_key",
      "remove_possible_simple_key",
      "unwind_indent",
      "add_indent",
      "fetch_stream_start",
      "fetch_stream_end",
      "fetch_directive",
      "fetch_document_start",
      "fetch_document_end",
      "fetch_document_indicator",
      "fetch_flow_sequence_start",
      "fetch_flow_mapping_start",
      "fetch_flow_collection_start",
      "fetch_flow_sequence_end",
      "fetch_flow_mapping_end",
      "fetch_flow_collection_end",
      "fetch_flow_entry",
      "fetch_block_entry",
      "fetch_key",
      "fetch_value",
      "fetch_alias",
      "fetch_anchor",
      "fetch_tag",
      "fetch_literal",
      "fetch_folded",
      "fetch_block_scalar",
      "fetch_single",
      "fetch_double",
      "fetch_flow_scalar",
      "fetch_plain",
      "check_directive",
      "check_document_start",
      "check_document_end",
      "check_block_entry",
      "check_key",
      "check_value",
      "check_plain",
      "scan_to_next_token",
      "scan_directive",
      "scan_directive_name",
      "scan_yaml_directive_value",
      "scan_yaml_directive_number",
      "scan_tag_directive_value",
      "scan_tag_directive_handle",
      "scan_tag_directive_prefix",
      "scan_directive_ignored_line",
      "scan_anchor",
      "scan_tag",
      "scan_block_scalar",
      "scan_block_scalar_indicators",
      "scan_block_scalar_ignored_line",
      "scan_block_scalar_indentation",
      "scan_block_scalar_breaks",
      "scan_flow_scalar",
      "scan_flow_scalar_non_spaces",
      "scan_flow_scalar_spaces",
      "scan_flow_scalar_breaks",
      "scan_plain",
      "scan_plain_spaces",
      "scan_tag_handle",
      "scan_tag_uri",
      "scan_uri_escapes",
      "scan_line_break"
    ],
    "classes": [
      "ScannerError",
      "SimpleKey",
      "Scanner"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/representer.py",
    "imports": [
      "datetime",
      "error",
      "nodes"
    ],
    "functions": [
      "__init__",
      "represent",
      "represent_data",
      "add_representer",
      "add_multi_representer",
      "represent_scalar",
      "represent_sequence",
      "represent_mapping",
      "ignore_aliases",
      "ignore_aliases",
      "represent_none",
      "represent_str",
      "represent_binary",
      "represent_bool",
      "represent_int",
      "represent_float",
      "represent_list",
      "represent_dict",
      "represent_set",
      "represent_date",
      "represent_datetime",
      "represent_yaml_object",
      "represent_undefined",
      "represent_complex",
      "represent_tuple",
      "represent_name",
      "represent_module",
      "represent_object",
      "represent_ordered_dict"
    ],
    "classes": [
      "RepresenterError",
      "BaseRepresenter",
      "SafeRepresenter",
      "Representer"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/resolver.py",
    "imports": [
      "error",
      "nodes",
      "re"
    ],
    "functions": [
      "__init__",
      "add_implicit_resolver",
      "add_path_resolver",
      "descend_resolver",
      "ascend_resolver",
      "check_resolver_prefix",
      "resolve"
    ],
    "classes": [
      "ResolverError",
      "BaseResolver",
      "Resolver"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/__init__.py",
    "imports": [
      "cyaml",
      "dumper",
      "error",
      "events",
      "io",
      "loader",
      "nodes",
      "tokens"
    ],
    "functions": [
      "warnings",
      "scan",
      "parse",
      "compose",
      "compose_all",
      "load",
      "load_all",
      "full_load",
      "full_load_all",
      "safe_load",
      "safe_load_all",
      "unsafe_load",
      "unsafe_load_all",
      "emit",
      "serialize_all",
      "serialize",
      "dump_all",
      "dump",
      "safe_dump_all",
      "safe_dump",
      "add_implicit_resolver",
      "add_path_resolver",
      "add_constructor",
      "add_multi_constructor",
      "add_representer",
      "add_multi_representer",
      "__init__",
      "from_yaml",
      "to_yaml"
    ],
    "classes": [
      "YAMLObjectMetaclass",
      "YAMLObject"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/serializer.py",
    "imports": [
      "error",
      "events",
      "nodes"
    ],
    "functions": [
      "__init__",
      "open",
      "close",
      "serialize",
      "anchor_node",
      "generate_anchor",
      "serialize_node"
    ],
    "classes": [
      "SerializerError",
      "Serializer"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/constructor.py",
    "imports": [
      "collections",
      "error",
      "nodes"
    ],
    "functions": [
      "__init__",
      "check_data",
      "check_state_key",
      "get_data",
      "get_single_data",
      "construct_document",
      "construct_object",
      "construct_scalar",
      "construct_sequence",
      "construct_mapping",
      "construct_pairs",
      "add_constructor",
      "add_multi_constructor",
      "construct_scalar",
      "flatten_mapping",
      "construct_mapping",
      "construct_yaml_null",
      "construct_yaml_bool",
      "construct_yaml_int",
      "construct_yaml_float",
      "construct_yaml_binary",
      "construct_yaml_timestamp",
      "construct_yaml_omap",
      "construct_yaml_pairs",
      "construct_yaml_set",
      "construct_yaml_str",
      "construct_yaml_seq",
      "construct_yaml_map",
      "construct_yaml_object",
      "construct_undefined",
      "get_state_keys_blacklist",
      "get_state_keys_blacklist_regexp",
      "construct_python_str",
      "construct_python_unicode",
      "construct_python_bytes",
      "construct_python_long",
      "construct_python_complex",
      "construct_python_tuple",
      "find_python_module",
      "find_python_name",
      "construct_python_name",
      "construct_python_module",
      "make_python_instance",
      "set_python_instance_state",
      "construct_python_object",
      "construct_python_object_apply",
      "construct_python_object_new",
      "find_python_module",
      "find_python_name",
      "make_python_instance",
      "set_python_instance_state"
    ],
    "classes": [
      "ConstructorError",
      "BaseConstructor",
      "SafeConstructor",
      "FullConstructor",
      "UnsafeConstructor",
      "Constructor"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/loader.py",
    "imports": [
      "composer",
      "constructor",
      "parser",
      "reader",
      "resolver",
      "scanner"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "BaseLoader",
      "FullLoader",
      "SafeLoader",
      "Loader",
      "UnsafeLoader"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/error.py",
    "imports": [],
    "functions": [
      "__init__",
      "get_snippet",
      "__str__",
      "__init__",
      "__str__"
    ],
    "classes": [
      "Mark",
      "YAMLError",
      "MarkedYAMLError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/composer.py",
    "imports": [
      "error",
      "events",
      "nodes"
    ],
    "functions": [
      "__init__",
      "check_node",
      "get_node",
      "get_single_node",
      "compose_document",
      "compose_node",
      "compose_scalar_node",
      "compose_sequence_node",
      "compose_mapping_node"
    ],
    "classes": [
      "ComposerError",
      "Composer"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/reader.py",
    "imports": [
      "codecs",
      "error"
    ],
    "functions": [
      "__init__",
      "__str__",
      "__init__",
      "peek",
      "prefix",
      "forward",
      "get_mark",
      "determine_encoding",
      "check_printable",
      "update",
      "update_raw"
    ],
    "classes": [
      "ReaderError",
      "Reader"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/dumper.py",
    "imports": [
      "emitter",
      "representer",
      "resolver",
      "serializer"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "BaseDumper",
      "SafeDumper",
      "Dumper"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/yaml/cyaml.py",
    "imports": [
      "constructor",
      "representer",
      "resolver",
      "serializer",
      "yaml"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__"
    ],
    "classes": [
      "CBaseLoader",
      "CSafeLoader",
      "CFullLoader",
      "CUnsafeLoader",
      "CLoader",
      "CBaseDumper",
      "CSafeDumper",
      "CDumper"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/pydantic_core/core_schema.py",
    "imports": [
      "__future__",
      "collections",
      "datetime",
      "decimal",
      "pydantic_core",
      "re",
      "sys",
      "typing",
      "typing_extensions",
      "warnings"
    ],
    "functions": [
      "simple_ser_schema",
      "plain_serializer_function_ser_schema",
      "wrap_serializer_function_ser_schema",
      "format_ser_schema",
      "to_string_ser_schema",
      "model_ser_schema",
      "invalid_schema",
      "computed_field",
      "any_schema",
      "none_schema",
      "bool_schema",
      "int_schema",
      "float_schema",
      "decimal_schema",
      "complex_schema",
      "str_schema",
      "bytes_schema",
      "date_schema",
      "time_schema",
      "datetime_schema",
      "timedelta_schema",
      "literal_schema",
      "enum_schema",
      "missing_sentinel_schema",
      "is_instance_schema",
      "is_subclass_schema",
      "callable_schema",
      "uuid_schema",
      "filter_seq_schema",
      "list_schema",
      "tuple_positional_schema",
      "tuple_variable_schema",
      "tuple_schema",
      "set_schema",
      "frozenset_schema",
      "generator_schema",
      "filter_dict_schema",
      "dict_schema",
      "no_info_before_validator_function",
      "with_info_before_validator_function",
      "no_info_after_validator_function",
      "with_info_after_validator_function",
      "no_info_wrap_validator_function",
      "with_info_wrap_validator_function",
      "no_info_plain_validator_function",
      "with_info_plain_validator_function",
      "with_default_schema",
      "nullable_schema",
      "union_schema",
      "tagged_union_schema",
      "chain_schema",
      "lax_or_strict_schema",
      "json_or_python_schema",
      "typed_dict_field",
      "typed_dict_schema",
      "model_field",
      "model_fields_schema",
      "model_schema",
      "dataclass_field",
      "dataclass_args_schema",
      "dataclass_schema",
      "arguments_parameter",
      "arguments_schema",
      "arguments_v3_parameter",
      "arguments_v3_schema",
      "call_schema",
      "custom_error_schema",
      "json_schema",
      "url_schema",
      "multi_host_url_schema",
      "definitions_schema",
      "definition_reference_schema",
      "_dict_not_none",
      "iter_union_choices",
      "field_before_validator_function",
      "general_before_validator_function",
      "field_after_validator_function",
      "general_after_validator_function",
      "field_wrap_validator_function",
      "general_wrap_validator_function",
      "field_plain_validator_function",
      "general_plain_validator_function",
      "__getattr__",
      "include",
      "exclude",
      "context",
      "mode",
      "by_alias",
      "exclude_unset",
      "exclude_defaults",
      "exclude_none",
      "exclude_computed_fields",
      "serialize_as_any",
      "polymorphic_serialization",
      "round_trip",
      "mode_is_json",
      "__str__",
      "__repr__",
      "field_name",
      "context",
      "config",
      "mode",
      "data",
      "field_name",
      "__call__",
      "__call__"
    ],
    "classes": [
      "CoreConfig",
      "SerializationInfo",
      "FieldSerializationInfo",
      "ValidationInfo",
      "SimpleSerSchema",
      "PlainSerializerFunctionSerSchema",
      "SerializerFunctionWrapHandler",
      "WrapSerializerFunctionSerSchema",
      "FormatSerSchema",
      "ToStringSerSchema",
      "ModelSerSchema",
      "InvalidSchema",
      "ComputedField",
      "AnySchema",
      "NoneSchema",
      "BoolSchema",
      "IntSchema",
      "FloatSchema",
      "DecimalSchema",
      "ComplexSchema",
      "StringSchema",
      "BytesSchema",
      "DateSchema",
      "TimeSchema",
      "DatetimeSchema",
      "TimedeltaSchema",
      "LiteralSchema",
      "EnumSchema",
      "MissingSentinelSchema",
      "IsInstanceSchema",
      "IsSubclassSchema",
      "CallableSchema",
      "UuidSchema",
      "IncExSeqSerSchema",
      "ListSchema",
      "TupleSchema",
      "SetSchema",
      "FrozenSetSchema",
      "GeneratorSchema",
      "IncExDictSerSchema",
      "DictSchema",
      "NoInfoValidatorFunctionSchema",
      "WithInfoValidatorFunctionSchema",
      "_ValidatorFunctionSchema",
      "BeforeValidatorFunctionSchema",
      "AfterValidatorFunctionSchema",
      "ValidatorFunctionWrapHandler",
      "NoInfoWrapValidatorFunctionSchema",
      "WithInfoWrapValidatorFunctionSchema",
      "WrapValidatorFunctionSchema",
      "PlainValidatorFunctionSchema",
      "WithDefaultSchema",
      "NullableSchema",
      "UnionSchema",
      "TaggedUnionSchema",
      "ChainSchema",
      "LaxOrStrictSchema",
      "JsonOrPythonSchema",
      "TypedDictField",
      "TypedDictSchema",
      "ModelField",
      "ModelFieldsSchema",
      "ModelSchema",
      "DataclassField",
      "DataclassArgsSchema",
      "DataclassSchema",
      "ArgumentsParameter",
      "ArgumentsSchema",
      "ArgumentsV3Parameter",
      "ArgumentsV3Schema",
      "CallSchema",
      "CustomErrorSchema",
      "JsonSchema",
      "UrlSchema",
      "MultiHostUrlSchema",
      "DefinitionsSchema",
      "DefinitionReferenceSchema"
    ],
    "docstring": "This module contains definitions to build schemas which `pydantic_core` can\nvalidate and serialize."
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/pydantic_core/__init__.py",
    "imports": [
      "__future__",
      "_pydantic_core",
      "core_schema",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [],
    "classes": [
      "ErrorDetails",
      "InitErrorDetails",
      "ErrorTypeInfo",
      "MultiHostHost"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/concurrency.py",
    "imports": [
      "anyio",
      "contextlib",
      "starlette",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/routing.py",
    "imports": [
      "asyncio",
      "contextlib",
      "dataclasses",
      "email",
      "enum",
      "fastapi",
      "inspect",
      "json",
      "pydantic",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "_prepare_response_content",
      "_merge_lifespan_context",
      "get_request_handler",
      "get_websocket_app",
      "__init__",
      "matches",
      "__init__",
      "get_route_handler",
      "matches",
      "__init__",
      "route",
      "add_api_route",
      "api_route",
      "add_api_websocket_route",
      "websocket",
      "websocket_route",
      "include_router",
      "get",
      "put",
      "post",
      "delete",
      "options",
      "head",
      "patch",
      "trace",
      "on_event",
      "decorator",
      "decorator",
      "decorator",
      "decorator",
      "decorator"
    ],
    "classes": [
      "APIWebSocketRoute",
      "APIRoute",
      "APIRouter"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/templating.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/exception_handlers.py",
    "imports": [
      "fastapi",
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/requests.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/logger.py",
    "imports": [
      "logging"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/cli.py",
    "imports": [
      "fastapi_cli"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/utils.py",
    "imports": [
      "dataclasses",
      "fastapi",
      "pydantic",
      "re",
      "routing",
      "typing",
      "typing_extensions",
      "warnings",
      "weakref"
    ],
    "functions": [
      "is_body_allowed_for_status_code",
      "get_path_param_names",
      "create_model_field",
      "create_cloned_field",
      "generate_operation_id_for_path",
      "generate_unique_id",
      "deep_dict_update",
      "get_value_or_default"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/param_functions.py",
    "imports": [
      "fastapi",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "Path",
      "Query",
      "Header",
      "Cookie",
      "Body",
      "Form",
      "File",
      "Depends",
      "Security"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/encoders.py",
    "imports": [
      "_compat",
      "collections",
      "dataclasses",
      "datetime",
      "decimal",
      "enum",
      "fastapi",
      "ipaddress",
      "pathlib",
      "pydantic",
      "re",
      "types",
      "typing",
      "typing_extensions",
      "uuid"
    ],
    "functions": [
      "isoformat",
      "decimal_encoder",
      "generate_encoders_by_class_tuples",
      "jsonable_encoder"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/__main__.py",
    "imports": [
      "fastapi"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/websockets.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/params.py",
    "imports": [
      "_compat",
      "enum",
      "fastapi",
      "pydantic",
      "typing",
      "typing_extensions",
      "warnings"
    ],
    "functions": [
      "__init__",
      "__repr__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__repr__",
      "__init__",
      "__init__",
      "__init__",
      "__repr__",
      "__init__"
    ],
    "classes": [
      "ParamTypes",
      "Param",
      "Path",
      "Query",
      "Header",
      "Cookie",
      "Body",
      "Form",
      "File",
      "Depends",
      "Security"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/__init__.py",
    "imports": [
      "applications",
      "background",
      "datastructures",
      "exceptions",
      "param_functions",
      "requests",
      "responses",
      "routing",
      "starlette",
      "websockets"
    ],
    "functions": [],
    "classes": [],
    "docstring": "FastAPI framework, high performance, easy to learn, fast to code, ready for production"
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/applications.py",
    "imports": [
      "enum",
      "fastapi",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__init__",
      "openapi",
      "setup",
      "add_api_route",
      "api_route",
      "add_api_websocket_route",
      "websocket",
      "include_router",
      "get",
      "put",
      "post",
      "delete",
      "options",
      "head",
      "patch",
      "trace",
      "websocket_route",
      "on_event",
      "middleware",
      "exception_handler",
      "decorator",
      "decorator",
      "decorator",
      "decorator",
      "decorator"
    ],
    "classes": [
      "FastAPI"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/datastructures.py",
    "imports": [
      "fastapi",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "Default",
      "__get_validators__",
      "validate",
      "_validate",
      "__get_pydantic_json_schema__",
      "__get_pydantic_core_schema__",
      "__init__",
      "__bool__",
      "__eq__",
      "__modify_schema__"
    ],
    "classes": [
      "UploadFile",
      "DefaultPlaceholder"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/_compat.py",
    "imports": [
      "collections",
      "copy",
      "dataclasses",
      "enum",
      "fastapi",
      "functools",
      "pydantic",
      "pydantic_core",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "_regenerate_error_with_loc",
      "_annotation_is_sequence",
      "field_annotation_is_sequence",
      "value_is_sequence",
      "_annotation_is_complex",
      "field_annotation_is_complex",
      "field_annotation_is_scalar",
      "field_annotation_is_scalar_sequence",
      "is_bytes_or_nonable_bytes_annotation",
      "is_uploadfile_or_nonable_uploadfile_annotation",
      "is_bytes_sequence_annotation",
      "is_uploadfile_sequence_annotation",
      "get_cached_model_fields",
      "get_annotation_from_field_info",
      "_normalize_errors",
      "_model_rebuild",
      "_model_dump",
      "_get_model_config",
      "get_schema_from_model_field",
      "get_compat_model_name_map",
      "get_definitions",
      "is_scalar_field",
      "is_sequence_field",
      "is_scalar_sequence_field",
      "is_bytes_field",
      "is_bytes_sequence_field",
      "copy_field_info",
      "serialize_sequence_value",
      "get_missing_field_error",
      "create_body_model",
      "get_model_fields",
      "with_info_plain_validator_function",
      "get_model_definitions",
      "is_pv1_scalar_field",
      "is_pv1_scalar_sequence_field",
      "_normalize_errors",
      "_model_rebuild",
      "_model_dump",
      "_get_model_config",
      "get_schema_from_model_field",
      "get_compat_model_name_map",
      "get_definitions",
      "is_scalar_field",
      "is_sequence_field",
      "is_scalar_sequence_field",
      "is_bytes_field",
      "is_bytes_sequence_field",
      "copy_field_info",
      "serialize_sequence_value",
      "get_missing_field_error",
      "create_body_model",
      "get_model_fields",
      "alias",
      "required",
      "default",
      "type_",
      "__post_init__",
      "get_default",
      "validate",
      "serialize",
      "__hash__"
    ],
    "classes": [
      "BaseConfig",
      "ErrorWrapper",
      "ModelField",
      "GenerateJsonSchema",
      "PydanticSchemaGenerationError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/types.py",
    "imports": [
      "enum",
      "pydantic",
      "types",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/exceptions.py",
    "imports": [
      "pydantic",
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "errors",
      "__init__",
      "__init__",
      "__str__"
    ],
    "classes": [
      "HTTPException",
      "WebSocketException",
      "FastAPIError",
      "ValidationException",
      "RequestValidationError",
      "WebSocketRequestValidationError",
      "ResponseValidationError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/background.py",
    "imports": [
      "starlette",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "add_task"
    ],
    "classes": [
      "BackgroundTasks"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/testclient.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/responses.py",
    "imports": [
      "orjson",
      "starlette",
      "typing",
      "ujson"
    ],
    "functions": [
      "render",
      "render"
    ],
    "classes": [
      "UJSONResponse",
      "ORJSONResponse"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/fastapi/staticfiles.py",
    "imports": [
      "starlette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/importer.py",
    "imports": [
      "importlib",
      "typing"
    ],
    "functions": [
      "import_from_string"
    ],
    "classes": [
      "ImportFromStringError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/__main__.py",
    "imports": [
      "uvicorn"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/__init__.py",
    "imports": [
      "uvicorn"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/logging.py",
    "imports": [
      "__future__",
      "click",
      "copy",
      "http",
      "logging",
      "sys",
      "typing"
    ],
    "functions": [
      "__init__",
      "color_level_name",
      "should_use_colors",
      "formatMessage",
      "should_use_colors",
      "get_status_code",
      "formatMessage",
      "default",
      "default"
    ],
    "classes": [
      "ColourizedFormatter",
      "DefaultFormatter",
      "AccessFormatter"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/workers.py",
    "imports": [
      "__future__",
      "asyncio",
      "gunicorn",
      "logging",
      "signal",
      "sys",
      "typing",
      "uvicorn",
      "warnings"
    ],
    "functions": [
      "__init__",
      "init_process",
      "init_signals",
      "_install_sigquit_handler",
      "run"
    ],
    "classes": [
      "UvicornWorker",
      "UvicornH11Worker"
    ],
    "docstring": null
  },
  {
    "file": "/opt/alfred-v2/venv/lib/python3.12/site-packages/uvicorn/_types.py",
    "imports": [
      "__future__",
      "sys",
      "types",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__init__"
    ],
    "classes": [
      "ASGIVersions",
      "HTTPScope",
      "WebSocketScope",
      "LifespanScope",
      "HTTPRequestEvent",
      "HTTPResponseDebugEvent",
      "HTTPResponseStartEvent",
      "HTTPResponseBodyEvent",
      "HTTPResponseTrailersEvent",
      "HTTPServerPushEvent",
      "HTTPDisconnectEvent",
      "WebSocketConnectEvent",
      "WebSocketAcceptEvent",
      "_WebSocketReceiveEventBytes",
      "_WebSocketReceiveEventText",
      "_WebSocketSendEventBytes",
      "_WebSocketSendEventText",
      "WebSocketResponseStartEvent",
      "WebSocketResponseBodyEvent",
      "WebSocketDisconnectEvent",
      "WebSocketCloseEvent",
      "LifespanStartupEvent",
      "LifespanShutdownEvent",
      "LifespanStartupCompleteEvent",
      "LifespanStartupFa
```

### python/llamaindex_python_inventory.json

Size: 13252730 bytes

```text
[
  {
    "file": "/opt/llamaindex-bakeoff/prompt_builder.py",
    "imports": [
      "pathlib"
    ],
    "functions": [
      "load",
      "build_prompt"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/people_evidence.py",
    "imports": [
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/people_summary.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_answer.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/intent_classifier.py",
    "imports": [
      "json",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "clean_entity",
      "classify"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/heading_search.py",
    "imports": [
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/routed_retrieval.py",
    "imports": [
      "llama_index",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/people_graham.py",
    "imports": [
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/filter_test.py",
    "imports": [
      "llama_index",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/app.py",
    "imports": [
      "fastapi",
      "functools",
      "html",
      "json",
      "llama_index",
      "pathlib",
      "subprocess",
      "sys",
      "urllib"
    ],
    "functions": [
      "get_retriever",
      "classify_route",
      "routed_queries",
      "allowed_by_route",
      "object_type",
      "filename_people_matches",
      "page",
      "home",
      "search",
      "view_theme",
      "view",
      "alfred_api"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/validate_retrieval.py",
    "imports": [
      "llama_index",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/ask.py",
    "imports": [
      "json",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_synthesise.py",
    "imports": [
      "pathlib",
      "prompt_builder",
      "subprocess",
      "sys"
    ],
    "functions": [
      "load_doc",
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/people_summarise.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_summary.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/review_answer.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_evidence_v2.py",
    "imports": [
      "entity_config",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_evidence.py",
    "imports": [
      "entity_config",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/improve_answer.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/test_index.py",
    "imports": [
      "llama_index"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/alfred.py",
    "imports": [
      "contextlib",
      "json",
      "llama_index",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/entity_config.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.modewire.20260627-120237.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/ask.pre-intent.20260627-181815.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/alfred.gate.20260627-190548.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys",
      "tempfile"
    ],
    "functions": [
      "run"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/alfred.pre-json.20260627-221612.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys",
      "tempfile"
    ],
    "functions": [
      "run"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/app.pre-json-alfred.20260627-221612.py",
    "imports": [
      "fastapi",
      "functools",
      "html",
      "llama_index",
      "pathlib",
      "subprocess",
      "urllib"
    ],
    "functions": [
      "get_retriever",
      "classify_route",
      "routed_queries",
      "allowed_by_route",
      "object_type",
      "filename_people_matches",
      "page",
      "home",
      "search",
      "view_theme",
      "view",
      "alfred_api"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_answer.cli.20260627-120653.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.pre-governance.20260627-182938.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/improve_answer.truth.20260627-185943.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/app.pre-alfred-api.20260627-212408.py",
    "imports": [
      "fastapi",
      "functools",
      "html",
      "llama_index",
      "pathlib",
      "subprocess",
      "urllib"
    ],
    "functions": [
      "get_retriever",
      "classify_route",
      "routed_queries",
      "allowed_by_route",
      "object_type",
      "filename_people_matches",
      "page",
      "home",
      "search",
      "view_theme",
      "view"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/review_answer.fix.20260627-185314.py",
    "imports": [
      "json",
      "os",
      "pathlib",
      "requests",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.debug.20260627-183128.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "load_doc",
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/review_answer.pre-openrouter.20260627-184743.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/alfred.pre-self-improve.20260627-185615.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "run"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.pre-promptbuilder.20260627-183612.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "load_doc",
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/alfred.pipeline.20260627-185649.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "run"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.reasoning.20260627-120155.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_answer.pre-intent.20260627-181815.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_answer.debug.20260627-190216.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/entity_synthesise.cli.20260627-120653.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/review_answer.pre-openrouter-reuse.20260627-184928.py",
    "imports": [
      "json",
      "os",
      "pathlib",
      "requests",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/entity_answer.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/routed_retrieval.py",
    "imports": [
      "llama_index",
      "pathlib"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/app.py",
    "imports": [
      "fastapi",
      "functools",
      "html",
      "llama_index",
      "pathlib",
      "subprocess",
      "urllib"
    ],
    "functions": [
      "get_retriever",
      "classify_route",
      "routed_queries",
      "allowed_by_route",
      "object_type",
      "filename_people_matches",
      "page",
      "home",
      "search",
      "view_theme",
      "view"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/entity_synthesise.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/baseline-20260627-113531/entity_evidence_v2.py",
    "imports": [
      "entity_config",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-evidence-contract-20260627-114554/entity_answer.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-evidence-contract-20260627-114554/entity_synthesise.py",
    "imports": [
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-evidence-contract-20260627-114554/entity_evidence_v2.py",
    "imports": [
      "entity_config",
      "pathlib",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-evidence-contract-20260627-114554/entity_config.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/prompt_builder.py",
    "imports": [
      "pathlib"
    ],
    "functions": [
      "load",
      "build_prompt"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/entity_answer.py",
    "imports": [
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/intent_classifier.py",
    "imports": [
      "json",
      "pathlib",
      "re",
      "sys"
    ],
    "functions": [
      "clean_entity",
      "classify"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/ask.py",
    "imports": [
      "json",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/entity_synthesise.py",
    "imports": [
      "pathlib",
      "prompt_builder",
      "subprocess",
      "sys"
    ],
    "functions": [
      "load_doc",
      "executive_reasoning_mode"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/releases/pre-alfred-runtime-20260627-184554/review_answer.py",
    "imports": [
      "json",
      "pathlib",
      "subprocess",
      "sys"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/isympy.py",
    "imports": [
      "IPython",
      "argparse",
      "os",
      "sympy",
      "sys"
    ],
    "functions": [
      "main"
    ],
    "classes": [],
    "docstring": "Python shell for SymPy.\n\nThis is just a normal Python shell (IPython shell if you have the\nIPython package installed), that executes the following commands for\nthe user:\n\n    >>> from __future__ import division\n    >>> from sympy import *\n    >>> x, y, z, t = symbols('x y z t')\n    >>> k, m, n = symbols('k m n', integer=True)\n    >>> f, g, h = symbols('f g h', cls=Function)\n    >>> init_printing()\n\nSo starting 'isympy' is equivalent to starting Python (or IPython) and\nexecuting the above commands by hand.  It is intended for easy and quick\nexperimentation with SymPy.  isympy is a good way to use SymPy as an\ninteractive calculator. If you have IPython and Matplotlib installed, then\ninteractive plotting is enabled by default.\n\nCOMMAND LINE OPTIONS\n--------------------\n\n-c CONSOLE, --console=CONSOLE\n\n     Use the specified shell (Python or IPython) shell as the console\n     backend instead of the default one (IPython if present, Python\n     otherwise), e.g.:\n\n        $isympy -c python\n\n    CONSOLE must be one of 'ipython' or 'python'\n\n-p PRETTY, --pretty PRETTY\n\n    Setup pretty-printing in SymPy. When pretty-printing is enabled,\n    expressions can be printed with Unicode or ASCII. The default is\n    to use pretty-printing (with Unicode if the terminal supports it).\n    When this option is 'no', expressions will not be pretty-printed\n    and ASCII will be used:\n\n        $isympy -p no\n\n    PRETTY must be one of 'unicode', 'ascii', or 'no'\n\n-t TYPES, --types=TYPES\n\n    Setup the ground types for the polys.  By default, gmpy ground types\n    are used if gmpy2 or gmpy is installed, otherwise it falls back to python\n    ground types, which are a little bit slower.  You can manually\n    choose python ground types even if gmpy is installed (e.g., for\n    testing purposes):\n\n        $isympy -t python\n\n    TYPES must be one of 'gmpy', 'gmpy1' or 'python'\n\n    Note that the ground type gmpy1 is primarily intended for testing; it\n    forces the use of gmpy version 1 even if gmpy2 is available.\n\n    This is the same as setting the environment variable\n    SYMPY_GROUND_TYPES to the given ground type (e.g.,\n    SYMPY_GROUND_TYPES='gmpy')\n\n    The ground types can be determined interactively from the variable\n    sympy.polys.domains.GROUND_TYPES.\n\n-o ORDER, --order ORDER\n\n    Setup the ordering of terms for printing.  The default is lex, which\n    orders terms lexicographically (e.g., x**2 + x + 1). You can choose\n    other orderings, such as rev-lex, which will use reverse\n    lexicographic ordering (e.g., 1 + x + x**2):\n\n        $isympy -o rev-lex\n\n    ORDER must be one of 'lex', 'rev-lex', 'grlex', 'rev-grlex',\n    'grevlex', 'rev-grevlex', 'old', or 'none'.\n\n    Note that for very large expressions, ORDER='none' may speed up\n    printing considerably but the terms will have no canonical order.\n\n-q, --quiet\n\n    Print only Python's and SymPy's versions to stdout at startup.\n\n-d, --doctest\n\n    Use the same format that should be used for doctests.  This is\n    equivalent to -c python -p no.\n\n-C, --no-cache\n\n    Disable the caching mechanism.  Disabling the cache may slow certain\n    operations down considerably.  This is useful for testing the cache,\n    or for benchmarking, as the cache can result in deceptive timings.\n\n    This is equivalent to setting the environment variable\n    SYMPY_USE_CACHE to 'no'.\n\n-a, --auto-symbols (requires at least IPython 0.11)\n\n    Automatically create missing symbols.  Normally, typing a name of a\n    Symbol that has not been instantiated first would raise NameError,\n    but with this option enabled, any undefined name will be\n    automatically created as a Symbol.\n\n    Note that this is intended only for interactive, calculator style\n    usage. In a script that uses SymPy, Symbols should be instantiated\n    at the top, so that it's clear what they are.\n\n    This will not override any names that are already defined, which\n    includes the single character letters represented by the mnemonic\n    QCOSINE (see the \"Gotchas and Pitfalls\" document in the\n    documentation). You can delete existing names by executing \"del\n    name\".  If a name is defined, typing \"'name' in dir()\" will return True.\n\n    The Symbols that are created using this have default assumptions.\n    If you want to place assumptions on symbols, you should create them\n    using symbols() or var().\n\n    Finally, this only works in the top level namespace. So, for\n    example, if you define a function in isympy with an undefined\n    Symbol, it will not work.\n\n    See also the -i and -I options.\n\n-i, --int-to-Integer (requires at least IPython 0.11)\n\n    Automatically wrap int literals with Integer.  This makes it so that\n    things like 1/2 will come out as Rational(1, 2), rather than 0.5.  This\n    works by preprocessing the source and wrapping all int literals with\n    Integer.  Note that this will not change the behavior of int literals\n    assigned to variables, and it also won't change the behavior of functions\n    that return int literals.\n\n    If you want an int, you can wrap the literal in int(), e.g. int(3)/int(2)\n    gives 1.5 (with division imported from __future__).\n\n-I, --interactive (requires at least IPython 0.11)\n\n    This is equivalent to --auto-symbols --int-to-Integer.  Future options\n    designed for ease of interactive use may be added to this.\n\n-D, --debug\n\n    Enable debugging output.  This is the same as setting the\n    environment variable SYMPY_DEBUG to 'True'.  The debug status is set\n    in the variable SYMPY_DEBUG within isympy.\n\n-- IPython options\n\n    Additionally you can pass command line options directly to the IPython\n    interpreter (the standard Python shell is not supported).  However you\n    need to add the '--' separator between two types of options, e.g the\n    startup banner option and the colors option. You need to enter the\n    options as required by the version of IPython that you are using, too:\n\n    in IPython 0.11,\n\n        $isympy -q -- --colors=NoColor\n\n    or older versions of IPython,\n\n        $isympy -q -- -colors NoColor\n\nSee also isympy --help."
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/threadpoolctl.py",
    "imports": [
      "abc",
      "argparse",
      "contextlib",
      "ctypes",
      "functools",
      "importlib",
      "itertools",
      "json",
      "os",
      "pyodide_js",
      "re",
      "sys",
      "textwrap",
      "typing",
      "warnings"
    ],
    "functions": [
      "register",
      "_format_docstring",
      "_realpath",
      "threadpool_info",
      "_main",
      "__init__",
      "info",
      "set_additional_attributes",
      "num_threads",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_find_affixes",
      "_get_symbol",
      "_find_affixes",
      "set_additional_attributes",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_get_threading_layer",
      "_get_architecture",
      "set_additional_attributes",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_get_threading_layer",
      "_get_architecture",
      "loaded_backends",
      "current_backend",
      "info",
      "set_additional_attributes",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_get_backend_list",
      "_get_current_backend",
      "switch_backend",
      "set_additional_attributes",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "_get_threading_layer",
      "get_num_threads",
      "set_num_threads",
      "get_version",
      "decorator",
      "__init__",
      "__enter__",
      "__exit__",
      "wrap",
      "restore_original_limits",
      "get_original_num_threads",
      "_check_params",
      "_set_threadpool_limits",
      "__init__",
      "__enter__",
      "__init__",
      "wrap",
      "__init__",
      "_from_controllers",
      "info",
      "select",
      "_get_params_for_sequential_blas_under_openmp",
      "limit",
      "wrap",
      "__len__",
      "_load_libraries",
      "_find_libraries_with_dl_iterate_phdr",
      "_find_libraries_with_dyld",
      "_find_libraries_with_enum_process_module_ex",
      "_find_libraries_pyodide",
      "_make_controller_from_path",
      "_check_prefix",
      "_warn_if_incompatible_openmp",
      "_get_libc",
      "_get_windll",
      "match_library_callback"
    ],
    "classes": [
      "_dl_phdr_info",
      "LibController",
      "OpenBLASController",
      "BLISController",
      "FlexiBLASController",
      "MKLController",
      "OpenMPController",
      "_ThreadpoolLimiter",
      "_ThreadpoolLimiterDecorator",
      "threadpool_limits",
      "ThreadpoolController"
    ],
    "docstring": "threadpoolctl\n\nThis module provides utilities to introspect native libraries that relies on\nthread pools (notably BLAS and OpenMP implementations) and dynamically set the\nmaximal number of threads they can use."
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/typing_inspect.py",
    "imports": [
      "collections",
      "mypy_extensions",
      "sys",
      "types",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "_gorg",
      "is_generic_type",
      "is_callable_type",
      "is_tuple_type",
      "is_optional_type",
      "is_final_type",
      "is_union_type",
      "is_literal_type",
      "is_typevar",
      "is_classvar",
      "is_new_type",
      "is_forward_ref",
      "get_last_origin",
      "get_origin",
      "get_parameters",
      "get_last_args",
      "_eval_args",
      "get_args",
      "get_bound",
      "get_constraints",
      "get_generic_type",
      "get_generic_bases",
      "typed_dict_keys",
      "get_forward_arg",
      "_replace_arg",
      "_remove_dups_flatten",
      "_subs_tree",
      "_union_subs_tree",
      "_generic_subs_tree",
      "_tuple_subs_tree",
      "_has_type_var",
      "_union_has_type_var",
      "_tuple_has_type_var",
      "_callable_has_type_var",
      "_generic_has_type_var",
      "_get_origin",
      "_get_args"
    ],
    "classes": [],
    "docstring": "Defines experimental API for runtime inspection of types defined\nin the standard \"typing\" module.\n\nExample usage::\n    from typing_inspect import is_generic_type"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/typing_extensions.py",
    "imports": [
      "_socket",
      "abc",
      "annotationlib",
      "asyncio",
      "builtins",
      "collections",
      "contextlib",
      "enum",
      "functools",
      "inspect",
      "io",
      "keyword",
      "operator",
      "sys",
      "types",
      "typing",
      "warnings"
    ],
    "functions": [
      "IntVar",
      "_get_protocol_attrs",
      "_caller",
      "_set_default",
      "_set_module",
      "_create_concatenate_alias",
      "_concatenate_getitem",
      "_unpack_args",
      "_has_generic_or_protocol_as_origin",
      "_is_unpacked_typevartuple",
      "__repr__",
      "_should_collect_from_parameters",
      "_should_collect_from_parameters",
      "__init__",
      "__getattr__",
      "__mro_entries__",
      "__repr__",
      "__reduce__",
      "__call__",
      "__or__",
      "__ror__",
      "__instancecheck__",
      "__subclasscheck__",
      "__getitem__",
      "__repr__",
      "final",
      "disjoint_base",
      "_flatten_literal_params",
      "_value_and_type_iter",
      "overload",
      "get_overloads",
      "clear_overloads",
      "_is_dunder",
      "_allow_reckless_class_checks",
      "_no_init",
      "_type_check_issubclass_arg_1",
      "_proto_hook",
      "runtime_checkable",
      "_get_typeddict_qualifiers",
      "_create_typeddict",
      "TypedDict",
      "is_typeddict",
      "assert_type",
      "_strip_extras",
      "get_type_hints",
      "_could_be_inserted_optional",
      "_clean_optional",
      "get_origin",
      "get_args",
      "TypeAlias",
      "__instancecheck__",
      "Concatenate",
      "TypeGuard",
      "TypeIs",
      "TypeForm",
      "LiteralString",
      "Self",
      "Never",
      "Required",
      "NotRequired",
      "ReadOnly",
      "_is_unpack",
      "Unpack",
      "_is_unpack",
      "reveal_type",
      "assert_never",
      "dataclass_transform",
      "override",
      "_is_param_expr",
      "_is_param_expr",
      "_check_generic",
      "_check_generic",
      "_collect_type_vars",
      "_collect_parameters",
      "_make_nmtuple",
      "_namedtuple_mro_entries",
      "NamedTuple",
      "get_original_bases",
      "is_protocol",
      "get_protocol_members",
      "get_annotations",
      "_eval_with_owner",
      "evaluate_forward_ref",
      "__init__",
      "__repr__",
      "__getstate__",
      "type_repr",
      "__instancecheck__",
      "__repr__",
      "__new__",
      "__eq__",
      "__hash__",
      "__init__",
      "__getitem__",
      "__init__",
      "__setattr__",
      "__getitem__",
      "__new__",
      "__init__",
      "__subclasscheck__",
      "__instancecheck__",
      "__eq__",
      "__hash__",
      "__init_subclass__",
      "__int__",
      "__float__",
      "__complex__",
      "__bytes__",
      "__index__",
      "__abs__",
      "__round__",
      "read",
      "write",
      "__setattr__",
      "__new__",
      "__repr__",
      "__reduce__",
      "__new__",
      "__repr__",
      "__reduce__",
      "__new__",
      "__subclasscheck__",
      "__call__",
      "__mro_entries__",
      "__new__",
      "__init_subclass__",
      "__copy__",
      "__deepcopy__",
      "__init__",
      "__repr__",
      "__eq__",
      "__init__",
      "__repr__",
      "__eq__",
      "_type_convert",
      "__init__",
      "__repr__",
      "__hash__",
      "__call__",
      "__parameters__",
      "copy_with",
      "__getitem__",
      "__call__",
      "__init__",
      "__typing_unpacked_tuple_args__",
      "__typing_is_unpacked_typevartuple__",
      "__getitem__",
      "decorator",
      "__init__",
      "__call__",
      "__new__",
      "__call__",
      "__init__",
      "__mro_entries__",
      "__repr__",
      "__reduce__",
      "_is_unionable",
      "_is_unionable",
      "__init__",
      "__setattr__",
      "__delattr__",
      "_raise_attribute_error",
      "__repr__",
      "_check_parameters",
      "__getitem__",
      "__reduce__",
      "__init_subclass__",
      "__call__",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__call__",
      "__or__",
      "__ror__",
      "_tvar_prepare_subst",
      "__new__",
      "__init_subclass__",
      "args",
      "kwargs",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__reduce__",
      "__call__",
      "copy_with",
      "__getitem__",
      "__new__",
      "__init_subclass__",
      "__iter__",
      "__init__",
      "__repr__",
      "__hash__",
      "__eq__",
      "__reduce__",
      "__init_subclass__",
      "__or__",
      "__ror__",
      "__getattr__",
      "_check_single_param",
      "__or__",
      "__ror__",
      "__annotate__",
      "_paramspec_prepare_subst",
      "_typevartuple_prepare_subst",
      "__init_subclass__",
      "__new__",
      "__init_subclass__",
      "__init_subclass__",
      "wrapper"
    ],
    "classes": [
      "_Sentinel",
      "_SpecialForm",
      "_ExtensionsSpecialForm",
      "_DefaultMixin",
      "_TypeVarLikeMeta",
      "_EllipsisDummy",
      "Sentinel",
      "_AnyMeta",
      "Any",
      "_LiteralGenericAlias",
      "_LiteralForm",
      "_SpecialGenericAlias",
      "_ProtocolMeta",
      "Protocol",
      "SupportsInt",
      "SupportsFloat",
      "SupportsComplex",
      "SupportsBytes",
      "SupportsIndex",
      "SupportsAbs",
      "SupportsRound",
      "Reader",
      "Writer",
      "SingletonMeta",
      "NoDefaultType",
      "NoExtraItemsType",
      "_TypedDictMeta",
      "_TypedDictSpecialForm",
      "TypeVar",
      "_Immutable",
      "ParamSpecArgs",
      "ParamSpecKwargs",
      "_ConcatenateGenericAlias",
      "_TypeFormForm",
      "_UnpackSpecialForm",
      "_UnpackAlias",
      "deprecated",
      "_NamedTupleMeta",
      "Buffer",
      "NewType",
      "TypeAliasType",
      "Doc",
      "Format",
      "ParamSpec",
      "ParamSpec",
      "_ConcatenateGenericAlias",
      "TypeVarTuple",
      "TypeVarTuple",
      "_TypeAliasGenericAlias",
      "Dummy"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/mypy_extensions.py",
    "imports": [
      "sys",
      "typing",
      "warnings"
    ],
    "functions": [
      "_check_fails",
      "_dict_new",
      "_typeddict_new",
      "Arg",
      "DefaultArg",
      "NamedArg",
      "DefaultNamedArg",
      "VarArg",
      "KwArg",
      "trait",
      "mypyc_attr",
      "_warn_deprecation",
      "__getattr__",
      "__new__",
      "__init__",
      "__getitem__",
      "__getitem__",
      "__instancecheck__",
      "__new__",
      "__new__",
      "__new__",
      "__new__"
    ],
    "classes": [
      "_TypedDictMeta",
      "_DEPRECATED_NoReturn",
      "_FlexibleAliasClsApplied",
      "_FlexibleAliasCls",
      "_NativeIntMeta",
      "i64",
      "i32",
      "i16",
      "u8"
    ],
    "docstring": "Defines experimental extensions to the standard \"typing\" module that are\nsupported by the mypy typechecker.\n\nExample usage:\n    from mypy_extensions import TypedDict"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/nest_asyncio.py",
    "imports": [
      "asyncio",
      "contextlib",
      "heapq",
      "os",
      "sys",
      "threading",
      "tornado"
    ],
    "functions": [
      "apply",
      "_patch_asyncio",
      "_patch_policy",
      "_patch_loop",
      "_patch_tornado",
      "run",
      "_get_event_loop",
      "get_event_loop",
      "run_forever",
      "run_until_complete",
      "_run_once",
      "manage_run",
      "manage_asyncgens",
      "_check_running"
    ],
    "classes": [],
    "docstring": "Patch asyncio to allow nested event loops."
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/concurrency.py",
    "imports": [
      "__future__",
      "anyio",
      "collections",
      "functools",
      "starlette",
      "typing",
      "warnings"
    ],
    "functions": [
      "_next"
    ],
    "classes": [
      "_StopIteration"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/routing.py",
    "imports": [
      "__future__",
      "collections",
      "contextlib",
      "enum",
      "functools",
      "inspect",
      "re",
      "starlette",
      "traceback",
      "types",
      "typing",
      "warnings"
    ],
    "functions": [
      "request_response",
      "websocket_session",
      "get_name",
      "replace_params",
      "compile_path",
      "_wrap_gen_lifespan_context",
      "__init__",
      "matches",
      "url_path_for",
      "__init__",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "routes",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "routes",
      "matches",
      "url_path_for",
      "__eq__",
      "__repr__",
      "__init__",
      "wrapper",
      "__init__",
      "__call__",
      "__init__",
      "url_path_for",
      "__eq__",
      "mount",
      "host",
      "add_route",
      "add_websocket_route"
    ],
    "classes": [
      "NoMatchFound",
      "Match",
      "BaseRoute",
      "Route",
      "WebSocketRoute",
      "Mount",
      "Host",
      "_AsyncLiftContextManager",
      "_DefaultLifespan",
      "Router"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/templating.py",
    "imports": [
      "__future__",
      "collections",
      "jinja2",
      "os",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "_setup_env_defaults",
      "get_template",
      "TemplateResponse",
      "url_for"
    ],
    "classes": [
      "_TemplateResponse",
      "Jinja2Templates"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/requests.py",
    "imports": [
      "__future__",
      "anyio",
      "collections",
      "http",
      "json",
      "multipart",
      "python_multipart",
      "starlette",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "cookie_parser",
      "__init__",
      "__getitem__",
      "__iter__",
      "__len__",
      "app",
      "url",
      "base_url",
      "headers",
      "query_params",
      "path_params",
      "cookies",
      "client",
      "session",
      "auth",
      "user",
      "state",
      "url_for",
      "__init__",
      "method",
      "receive",
      "form"
    ],
    "classes": [
      "ClientDisconnect",
      "HTTPConnection",
      "Request"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/schemas.py",
    "imports": [
      "__future__",
      "collections",
      "inspect",
      "re",
      "starlette",
      "typing",
      "yaml"
    ],
    "functions": [
      "render",
      "get_schema",
      "get_endpoints",
      "_remove_converter",
      "parse_docstring",
      "OpenAPIResponse",
      "__init__",
      "get_schema"
    ],
    "classes": [
      "OpenAPIResponse",
      "EndpointInfo",
      "BaseSchemaGenerator",
      "SchemaGenerator"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/_utils.py",
    "imports": [
      "__future__",
      "anyio",
      "asyncio",
      "collections",
      "contextlib",
      "exceptiongroup",
      "functools",
      "inspect",
      "starlette",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "is_async_callable",
      "is_async_callable",
      "is_async_callable",
      "get_route_path",
      "__init__",
      "__await__"
    ],
    "classes": [
      "AwaitableOrContextManager",
      "SupportsAsyncClose",
      "AwaitableOrContextManagerWrapper",
      "BaseExceptionGroup"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/status.py",
    "imports": [
      "__future__",
      "starlette",
      "warnings"
    ],
    "functions": [
      "__getattr__",
      "__dir__"
    ],
    "classes": [],
    "docstring": "HTTP codes\nSee HTTP Status Code Registry:\nhttps://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml\n\nAnd RFC 9110 - https://www.rfc-editor.org/rfc/rfc9110"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/websockets.py",
    "imports": [
      "__future__",
      "collections",
      "enum",
      "json",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "_raise_on_disconnect",
      "__init__"
    ],
    "classes": [
      "WebSocketState",
      "WebSocketDisconnect",
      "WebSocket",
      "WebSocketClose"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/__init__.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/applications.py",
    "imports": [
      "__future__",
      "collections",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "build_middleware_stack",
      "routes",
      "url_path_for",
      "mount",
      "host",
      "add_middleware",
      "add_exception_handler",
      "add_route"
    ],
    "classes": [
      "Starlette"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/authentication.py",
    "imports": [
      "__future__",
      "collections",
      "functools",
      "inspect",
      "starlette",
      "typing",
      "urllib"
    ],
    "functions": [
      "has_required_scope",
      "requires",
      "decorator",
      "__init__",
      "is_authenticated",
      "display_name",
      "identity",
      "__init__",
      "is_authenticated",
      "display_name",
      "is_authenticated",
      "display_name",
      "sync_wrapper"
    ],
    "classes": [
      "AuthenticationError",
      "AuthenticationBackend",
      "AuthCredentials",
      "BaseUser",
      "SimpleUser",
      "UnauthenticatedUser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py",
    "imports": [
      "__future__",
      "starlette",
      "typing"
    ],
    "functions": [
      "_lookup_exception_handler",
      "wrap_app_handling_exceptions"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/datastructures.py",
    "imports": [
      "__future__",
      "collections",
      "re",
      "shlex",
      "starlette",
      "typing",
      "urllib"
    ],
    "functions": [
      "__init__",
      "components",
      "scheme",
      "netloc",
      "path",
      "query",
      "fragment",
      "username",
      "password",
      "hostname",
      "port",
      "is_secure",
      "replace",
      "include_query_params",
      "replace_query_params",
      "remove_query_params",
      "__eq__",
      "__str__",
      "__repr__",
      "__new__",
      "__init__",
      "make_absolute_url",
      "__init__",
      "__repr__",
      "__str__",
      "__bool__",
      "__init__",
      "__len__",
      "__getitem__",
      "__iter__",
      "__repr__",
      "__str__",
      "__init__",
      "getlist",
      "keys",
      "values",
      "items",
      "multi_items",
      "__getitem__",
      "__contains__",
      "__iter__",
      "__len__",
      "__eq__",
      "__repr__",
      "__setitem__",
      "__delitem__",
      "pop",
      "popitem",
      "poplist",
      "clear",
      "setdefault",
      "setlist",
      "append",
      "update",
      "__init__",
      "__str__",
      "__repr__",
      "__init__",
      "content_type",
      "_in_memory",
      "_will_roll",
      "__repr__",
      "__init__",
      "__init__",
      "raw",
      "keys",
      "values",
      "items",
      "getlist",
      "mutablecopy",
      "__getitem__",
      "__contains__",
      "__iter__",
      "__len__",
      "__eq__",
      "__repr__",
      "__setitem__",
      "__delitem__",
      "__ior__",
      "__or__",
      "raw",
      "setdefault",
      "update",
      "append",
      "add_vary_header",
      "__init__",
      "__setattr__",
      "__getattr__",
      "__delattr__",
      "__getitem__",
      "__setitem__",
      "__delitem__",
      "__iter__",
      "__len__"
    ],
    "classes": [
      "Address",
      "URL",
      "URLPath",
      "Secret",
      "CommaSeparatedStrings",
      "ImmutableMultiDict",
      "MultiDict",
      "QueryParams",
      "UploadFile",
      "FormData",
      "Headers",
      "MutableHeaders",
      "State"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/types.py",
    "imports": [
      "collections",
      "contextlib",
      "starlette",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/exceptions.py",
    "imports": [
      "__future__",
      "collections",
      "http"
    ],
    "functions": [
      "__init__",
      "__str__",
      "__repr__",
      "__init__",
      "__str__",
      "__repr__"
    ],
    "classes": [
      "HTTPException",
      "WebSocketException",
      "StarletteDeprecationWarning"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/formparsers.py",
    "imports": [
      "__future__",
      "collections",
      "dataclasses",
      "enum",
      "multipart",
      "python_multipart",
      "starlette",
      "tempfile",
      "typing",
      "urllib"
    ],
    "functions": [
      "_user_safe_decode",
      "__init__",
      "__init__",
      "on_field_start",
      "on_field_name",
      "on_field_data",
      "on_field_end",
      "on_end",
      "__init__",
      "on_part_begin",
      "on_part_data",
      "on_part_end",
      "on_header_field",
      "on_header_value",
      "on_header_end",
      "on_headers_finished",
      "on_end"
    ],
    "classes": [
      "FormMessage",
      "MultipartPart",
      "MultiPartException",
      "FormParser",
      "MultiPartParser"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/config.py",
    "imports": [
      "__future__",
      "collections",
      "os",
      "pathlib",
      "typing",
      "warnings"
    ],
    "functions": [
      "__init__",
      "__getitem__",
      "__setitem__",
      "__delitem__",
      "__iter__",
      "__len__",
      "__init__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "__call__",
      "get",
      "_read_file",
      "_perform_cast"
    ],
    "classes": [
      "undefined",
      "EnvironError",
      "Environ",
      "Config"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/background.py",
    "imports": [
      "__future__",
      "collections",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "add_task"
    ],
    "classes": [
      "BackgroundTask",
      "BackgroundTasks"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/endpoints.py",
    "imports": [
      "__future__",
      "collections",
      "json",
      "starlette",
      "typing"
    ],
    "functions": [
      "__init__",
      "__await__",
      "__init__",
      "__await__"
    ],
    "classes": [
      "HTTPEndpoint",
      "WebSocketEndpoint"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/testclient.py",
    "imports": [
      "__future__",
      "anyio",
      "collections",
      "concurrent",
      "contextlib",
      "httpx",
      "httpx2",
      "inspect",
      "io",
      "json",
      "math",
      "starlette",
      "sys",
      "types",
      "typing",
      "typing_extensions",
      "urllib",
      "warnings"
    ],
    "functions": [
      "_is_asgi3",
      "__init__",
      "__init__",
      "__init__",
      "__enter__",
      "__exit__",
      "_raise_on_close",
      "send",
      "send_text",
      "send_bytes",
      "send_json",
      "close",
      "receive",
      "receive_text",
      "receive_bytes",
      "receive_json",
      "__init__",
      "handle_request",
      "__init__",
      "_portal_factory",
      "request",
      "get",
      "options",
      "head",
      "post",
      "put",
      "patch",
      "delete",
      "websocket_connect",
      "__enter__",
      "__exit__",
      "reset_portal",
      "wait_shutdown"
    ],
    "classes": [
      "_WrapASGI2",
      "_AsyncBackend",
      "_Upgrade",
      "WebSocketDenialResponse",
      "WebSocketTestSession",
      "_TestClientTransport",
      "TestClient"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/responses.py",
    "imports": [
      "__future__",
      "anyio",
      "collections",
      "datetime",
      "email",
      "functools",
      "hashlib",
      "http",
      "json",
      "mimetypes",
      "os",
      "secrets",
      "starlette",
      "stat",
      "sys",
      "typing",
      "urllib"
    ],
    "functions": [
      "__init__",
      "render",
      "init_headers",
      "headers",
      "set_cookie",
      "delete_cookie",
      "_wrap_websocket_denial_send",
      "__init__",
      "render",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "__init__",
      "set_stat_headers",
      "_should_use_range",
      "_parse_range_header",
      "_parse_ranges",
      "generate_multipart"
    ],
    "classes": [
      "Response",
      "HTMLResponse",
      "PlainTextResponse",
      "JSONResponse",
      "RedirectResponse",
      "StreamingResponse",
      "MalformedRangeHeader",
      "RangeNotSatisfiable",
      "FileResponse"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/convertors.py",
    "imports": [
      "__future__",
      "math",
      "typing",
      "uuid"
    ],
    "functions": [
      "register_url_convertor",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string",
      "convert",
      "to_string"
    ],
    "classes": [
      "Convertor",
      "StringConvertor",
      "PathConvertor",
      "IntegerConvertor",
      "FloatConvertor",
      "UUIDConvertor"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/starlette/staticfiles.py",
    "imports": [
      "__future__",
      "anyio",
      "email",
      "errno",
      "importlib",
      "os",
      "starlette",
      "stat",
      "typing"
    ],
    "functions": [
      "__init__",
      "__init__",
      "get_directories",
      "get_path",
      "lookup_path",
      "file_response",
      "is_not_modified"
    ],
    "classes": [
      "NotModifiedResponse",
      "StaticFiles"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/annotated_types/__init__.py",
    "imports": [
      "dataclasses",
      "datetime",
      "math",
      "sys",
      "types",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "__gt__",
      "__ge__",
      "__lt__",
      "__le__",
      "__mod__",
      "__div__",
      "__is_annotated_types_grouped_metadata__",
      "__iter__",
      "__iter__",
      "__iter__",
      "__repr__",
      "__call__",
      "__init_subclass__",
      "__iter__",
      "doc"
    ],
    "classes": [
      "SupportsGt",
      "SupportsGe",
      "SupportsLt",
      "SupportsLe",
      "SupportsMod",
      "SupportsDiv",
      "BaseMetadata",
      "Gt",
      "Ge",
      "Lt",
      "Le",
      "GroupedMetadata",
      "Interval",
      "MultipleOf",
      "MinLen",
      "MaxLen",
      "Len",
      "Timezone",
      "Unit",
      "Predicate",
      "Not",
      "DocInfo"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/annotated_types/test_cases.py",
    "imports": [
      "annotated_types",
      "datetime",
      "decimal",
      "math",
      "sys",
      "typing",
      "typing_extensions"
    ],
    "functions": [
      "cases",
      "__iter__"
    ],
    "classes": [
      "Case",
      "MyCustomGroupedMetadata"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/_utils.py",
    "imports": [
      "__future__",
      "functools",
      "language",
      "typing"
    ],
    "functions": [
      "get_iterable_path",
      "set_iterable_path",
      "is_iterable",
      "apply_with_path",
      "find_paths_if",
      "is_power_of_two",
      "validate_block_shape",
      "canonicalize_dtype",
      "canonicalize_ptr_dtype",
      "get_primitive_bitwidth",
      "is_namedtuple",
      "_tuple_create",
      "_impl"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/_filecheck.py",
    "imports": [
      "functools",
      "inspect",
      "os",
      "subprocess",
      "tempfile",
      "triton"
    ],
    "functions": [
      "run_filecheck",
      "run_parser",
      "run_filecheck_test",
      "filecheck_test",
      "__init__",
      "__str__",
      "test_fn"
    ],
    "classes": [
      "MatchError"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/__init__.py",
    "imports": [
      "compiler",
      "errors",
      "runtime"
    ],
    "functions": [
      "cdiv",
      "next_power_of_2"
    ],
    "classes": [],
    "docstring": "isort:skip_file"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/testing.py",
    "imports": [
      "contextlib",
      "functools",
      "math",
      "matplotlib",
      "numpy",
      "os",
      "pandas",
      "psutil",
      "runtime",
      "statistics",
      "subprocess",
      "sys",
      "torch",
      "typing"
    ],
    "functions": [
      "nvsmi",
      "_quantile",
      "_summarize_statistics",
      "do_bench_cudagraph",
      "do_bench",
      "assert_close",
      "perf_report",
      "get_dram_gbps",
      "get_max_tensorcore_tflops",
      "cuda_memcheck",
      "set_gpu_clock",
      "get_max_simd_tflops",
      "get_quantile",
      "__init__",
      "__init__",
      "_run",
      "run",
      "decorator",
      "wrapper"
    ],
    "classes": [
      "Benchmark",
      "Mark"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/errors.py",
    "imports": [],
    "functions": [],
    "classes": [
      "TritonError"
    ],
    "docstring": "Base class for all errors raised by Triton"
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/knobs.py",
    "imports": [
      "__future__",
      "compiler",
      "contextlib",
      "dataclasses",
      "functools",
      "importlib",
      "os",
      "pathlib",
      "re",
      "runtime",
      "subprocess",
      "sysconfig",
      "triton",
      "typing"
    ],
    "functions": [
      "setenv",
      "toenv",
      "refresh_knobs",
      "__init__",
      "__set_name__",
      "__get__",
      "get",
      "__set__",
      "__delete__",
      "transform",
      "__init__",
      "get",
      "__init__",
      "get",
      "__init__",
      "get",
      "__init__",
      "get",
      "__init__",
      "get",
      "from_path",
      "__init__",
      "get",
      "transform",
      "get",
      "get",
      "total_lowering",
      "total",
      "__call__",
      "knob_descriptors",
      "knobs",
      "copy",
      "reset",
      "scope",
      "__call__",
      "backend_dirs",
      "get_triton_dir",
      "__call__",
      "__call__",
      "__init__",
      "add",
      "remove",
      "__call__",
      "__call__",
      "__call__"
    ],
    "classes": [
      "Env",
      "env_base",
      "env_str",
      "env_str_callable_default",
      "env_bool",
      "env_int",
      "env_class",
      "NvidiaTool",
      "env_nvidia_tool",
      "env_opt_str",
      "env_opt_bool",
      "CompileTimes",
      "CompilationListener",
      "base_knobs",
      "BuildImpl",
      "build_knobs",
      "redis_knobs",
      "cache_knobs",
      "compilation_knobs",
      "autotuning_knobs",
      "LaunchHook",
      "InitHandleHook",
      "HookChain",
      "JITHookCompileInfo",
      "JITHook",
      "PipelineStagesHook",
      "runtime_knobs",
      "language_knobs",
      "nvidia_knobs",
      "amd_knobs",
      "proton_knobs"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/triton/_internal_testing.py",
    "imports": [
      "numpy",
      "os",
      "pytest",
      "re",
      "torch",
      "triton",
      "typing"
    ],
    "functions": [
      "is_interpreter",
      "get_current_target",
      "is_cuda",
      "is_ampere_or_newer",
      "is_blackwell",
      "is_blackwell_ultra",
      "is_hopper_or_newer",
      "is_hopper",
      "is_sm12x",
      "is_hip",
      "is_hip_cdna2",
      "is_hip_cdna3",
      "is_hip_cdna4",
      "is_hip_rdna3",
      "is_hip_rdna4",
      "is_hip_gfx1250",
      "is_hip_cdna",
      "is_hip_rdna",
      "get_hip_lds_size",
      "is_xpu",
      "get_arch",
      "numpy_random",
      "to_triton",
      "str_to_triton_dtype",
      "torch_dtype_name",
      "to_numpy",
      "supports_tma",
      "supports_ws",
      "tma_skip_msg",
      "default_alloc_fn",
      "unwrap_tensor",
      "_fresh_knobs_impl",
      "fresh_function",
      "reset_function"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/markup.py",
    "imports": [
      "_emoji_replace",
      "ast",
      "emoji",
      "errors",
      "operator",
      "re",
      "rich",
      "style",
      "text",
      "typing"
    ],
    "functions": [
      "escape",
      "_parse",
      "render",
      "__str__",
      "markup",
      "escape_backslashes",
      "pop_style"
    ],
    "classes": [
      "Tag"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/tree.py",
    "imports": [
      "_loop",
      "console",
      "jupyter",
      "measure",
      "rich",
      "segment",
      "style",
      "styled",
      "typing"
    ],
    "functions": [
      "__init__",
      "add",
      "__rich_console__",
      "__rich_measure__",
      "make_guide"
    ],
    "classes": [
      "Tree"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/box.py",
    "imports": [
      "_loop",
      "console",
      "rich",
      "table",
      "text",
      "typing"
    ],
    "functions": [
      "__init__",
      "__repr__",
      "__str__",
      "substitute",
      "get_plain_headed_box",
      "get_top",
      "get_row",
      "get_bottom"
    ],
    "classes": [
      "Box"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/color.py",
    "imports": [
      "_palettes",
      "color_triplet",
      "colorsys",
      "console",
      "enum",
      "functools",
      "re",
      "repr",
      "style",
      "sys",
      "table",
      "terminal_theme",
      "text",
      "typing"
    ],
    "functions": [
      "parse_rgb_hex",
      "blend_rgb",
      "__repr__",
      "__str__",
      "__repr__",
      "__rich__",
      "__rich_repr__",
      "system",
      "is_system_defined",
      "is_default",
      "get_truecolor",
      "from_ansi",
      "from_triplet",
      "from_rgb",
      "default",
      "parse",
      "get_ansi_codes",
      "downgrade"
    ],
    "classes": [
      "ColorSystem",
      "ColorType",
      "ColorParseError",
      "Color"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/json.py",
    "imports": [
      "argparse",
      "highlighter",
      "json",
      "pathlib",
      "rich",
      "sys",
      "text",
      "typing"
    ],
    "functions": [
      "__init__",
      "from_data",
      "__rich__"
    ],
    "classes": [
      "JSON"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/syntax.py",
    "imports": [
      "__future__",
      "_loop",
      "abc",
      "argparse",
      "cells",
      "color",
      "console",
      "jupyter",
      "measure",
      "os",
      "pathlib",
      "pygments",
      "re",
      "rich",
      "segment",
      "style",
      "sys",
      "text",
      "textwrap",
      "typing"
    ],
    "functions": [
      "_get_code_index_for_syntax_position",
      "get_style_for_token",
      "get_background_style",
      "__init__",
      "get_style_for_token",
      "get_background_style",
      "__init__",
      "get_style_for_token",
      "get_background_style",
      "__get__",
      "__set__",
      "get_theme",
      "__init__",
      "from_path",
      "guess_lexer",
      "_get_base_style",
      "_get_token_color",
      "lexer",
      "default_lexer",
      "highlight",
      "stylize_range",
      "_get_line_numbers_color",
      "_numbers_column_width",
      "_get_number_styles",
      "__rich_measure__",
      "__rich_console__",
      "_get_syntax",
      "_apply_stylized_ranges",
      "_process_code",
      "line_tokenize",
      "tokens_to_spans"
    ],
    "classes": [
      "SyntaxTheme",
      "PygmentsSyntaxTheme",
      "ANSISyntaxTheme",
      "_SyntaxHighlightRange",
      "PaddingProperty",
      "Syntax"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_palettes.py",
    "imports": [
      "palette"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/control.py",
    "imports": [
      "console",
      "rich",
      "segment",
      "time",
      "typing"
    ],
    "functions": [
      "strip_control_codes",
      "escape_control_codes",
      "__init__",
      "bell",
      "home",
      "move",
      "move_to_column",
      "move_to",
      "clear",
      "show_cursor",
      "alt_screen",
      "title",
      "__str__",
      "__rich_console__",
      "get_codes"
    ],
    "classes": [
      "Control"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_windows_renderer.py",
    "imports": [
      "rich",
      "typing"
    ],
    "functions": [
      "legacy_windows_render"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/markdown.py",
    "imports": [
      "__future__",
      "_loop",
      "_stack",
      "argparse",
      "console",
      "containers",
      "dataclasses",
      "io",
      "jupyter",
      "markdown_it",
      "pydoc",
      "rich",
      "rule",
      "segment",
      "style",
      "syntax",
      "sys",
      "text",
      "typing"
    ],
    "functions": [
      "create",
      "on_enter",
      "on_text",
      "on_leave",
      "on_child_close",
      "__rich_console__",
      "on_enter",
      "on_text",
      "on_leave",
      "create",
      "__init__",
      "__rich_console__",
      "create",
      "on_enter",
      "__init__",
      "__rich_console__",
      "create",
      "__init__",
      "__rich_console__",
      "__init__",
      "on_child_close",
      "__rich_console__",
      "__rich_console__",
      "__init__",
      "on_child_close",
      "__rich_console__",
      "__init__",
      "on_child_close",
      "__init__",
      "on_child_close",
      "__init__",
      "on_child_close",
      "create",
      "__init__",
      "on_text",
      "create",
      "__init__",
      "on_child_close",
      "__rich_console__",
      "__init__",
      "on_child_close",
      "render_bullet",
      "render_number",
      "create",
      "__init__",
      "create",
      "__init__",
      "on_enter",
      "__rich_console__",
      "__init__",
      "current_style",
      "on_text",
      "enter_style",
      "leave_style",
      "__init__",
      "_flatten_tokens",
      "__rich_console__"
    ],
    "classes": [
      "MarkdownElement",
      "UnknownElement",
      "TextElement",
      "Paragraph",
      "HeadingFormat",
      "Heading",
      "CodeBlock",
      "BlockQuote",
      "HorizontalRule",
      "TableElement",
      "TableHeaderElement",
      "TableBodyElement",
      "TableRowElement",
      "TableDataElement",
      "ListElement",
      "ListItem",
      "Link",
      "ImageItem",
      "MarkdownContext",
      "Markdown"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/spinner.py",
    "imports": [
      "_spinners",
      "console",
      "live",
      "measure",
      "style",
      "table",
      "text",
      "time",
      "typing"
    ],
    "functions": [
      "__init__",
      "__rich_console__",
      "__rich_measure__",
      "render",
      "update"
    ],
    "classes": [
      "Spinner"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/default_styles.py",
    "imports": [
      "argparse",
      "io",
      "rich",
      "style",
      "typing"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/columns.py",
    "imports": [
      "align",
      "collections",
      "console",
      "constrain",
      "itertools",
      "jupyter",
      "measure",
      "operator",
      "os",
      "padding",
      "table",
      "text",
      "typing"
    ],
    "functions": [
      "__init__",
      "add_renderable",
      "__rich_console__",
      "iter_renderables"
    ],
    "classes": [
      "Columns"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/jupyter.py",
    "imports": [
      "IPython",
      "rich",
      "segment",
      "terminal_theme",
      "typing"
    ],
    "functions": [
      "_render_segments",
      "display",
      "print",
      "__init__",
      "_repr_mimebundle_",
      "_repr_mimebundle_",
      "escape"
    ],
    "classes": [
      "JupyterRenderable",
      "JupyterMixin"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/styled.py",
    "imports": [
      "console",
      "measure",
      "rich",
      "segment",
      "style",
      "typing"
    ],
    "functions": [
      "__init__",
      "__rich_console__",
      "__rich_measure__"
    ],
    "classes": [
      "Styled"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_export_format.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/diagnose.py",
    "imports": [
      "os",
      "platform",
      "rich"
    ],
    "functions": [
      "report"
    ],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_ratio.py",
    "imports": [
      "dataclasses",
      "fractions",
      "math",
      "typing"
    ],
    "functions": [
      "ratio_resolve",
      "ratio_reduce",
      "ratio_distribute"
    ],
    "classes": [
      "Edge",
      "E"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/rule.py",
    "imports": [
      "align",
      "cells",
      "console",
      "jupyter",
      "measure",
      "rich",
      "style",
      "sys",
      "text",
      "typing"
    ],
    "functions": [
      "__init__",
      "__repr__",
      "__rich_console__",
      "_rule_line",
      "__rich_measure__"
    ],
    "classes": [
      "Rule"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/padding.py",
    "imports": [
      "console",
      "jupyter",
      "measure",
      "rich",
      "segment",
      "style",
      "typing"
    ],
    "functions": [
      "__init__",
      "indent",
      "unpack",
      "__repr__",
      "__rich_console__",
      "__rich_measure__"
    ],
    "classes": [
      "Padding"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/cells.py",
    "imports": [
      "__future__",
      "functools",
      "operator",
      "rich",
      "typing"
    ],
    "functions": [
      "get_character_cell_size",
      "cached_cell_len",
      "cell_len",
      "_cell_len",
      "split_graphemes",
      "_split_text",
      "split_text",
      "set_cell_size",
      "chop_cells"
    ],
    "classes": [
      "CellTable"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/themes.py",
    "imports": [
      "default_styles",
      "theme"
    ],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_timer.py",
    "imports": [
      "contextlib",
      "time",
      "typing"
    ],
    "functions": [
      "timer"
    ],
    "classes": [],
    "docstring": "Timer context manager, only used in debug."
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/screen.py",
    "imports": [
      "_loop",
      "console",
      "rich",
      "segment",
      "style",
      "typing"
    ],
    "functions": [
      "__init__",
      "__rich_console__"
    ],
    "classes": [
      "Screen"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_emoji_codes.py",
    "imports": [],
    "functions": [],
    "classes": [],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/status.py",
    "imports": [
      "console",
      "jupyter",
      "live",
      "spinner",
      "style",
      "time",
      "types",
      "typing"
    ],
    "functions": [
      "__init__",
      "renderable",
      "console",
      "update",
      "start",
      "stop",
      "__rich__",
      "__enter__",
      "__exit__"
    ],
    "classes": [
      "Status"
    ],
    "docstring": null
  },
  {
    "file": "/opt/llamaindex-bakeoff/.venv/lib/python3.12/site-packages/rich/_win32_console.py",
    "imports": [
      "ctypes",
      "rich",
      "sys",
      "time",
      "typing"
    ],
    "functions": [
      "GetStdHandle",
      "GetConsoleMode",
      "FillConsoleOutputCharacter",
      "FillConsoleOutputAttribute",
      "SetConsoleTextAttribute",
      "GetConsoleScreenBufferInfo",
      "SetConsoleCursorPosition",
      "GetConsoleCursorInfo",
      "SetConsoleCursorInfo",
      "SetConsoleTitle",
      "from_param",
      "__init__",
      "cursor_position",
      "screen_size",
      "write_text",
      "write_styled",
      "move_cursor_to",
      "erase_line",
      "erase_end_of_line",
      "erase_start_of_line",
      "move_cursor_up",
      "move_cursor_down",
      "move_cursor_forward",
      "move_cursor_to_column",
      "move_cursor_backward",
      "hide_cursor",
      "show_cursor",
      "set_title",
      "_get_cursor_size"
    ],
    "classes": [
      "Le
```
