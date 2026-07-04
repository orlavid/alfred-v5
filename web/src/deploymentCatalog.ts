export type DeploymentStatus = "Not installed" | "Configured" | "Running" | "Error";

export type DeploymentGuide = {
  title: string;
  path: string;
  shortLabel: string;
  purpose: string;
  whenToUse: string[];
  prerequisites: string[];
  installSteps: string[];
  configurationSteps: string[];
  validationCommands: string[];
  troubleshooting: string[];
  downloads: string[];
  status: DeploymentStatus;
  documentPath: string;
};

export const DEPLOYMENT_GUIDES: DeploymentGuide[] = [
  {
    title: "LlamaIndex",
    path: "/llamaindex",
    shortLabel: "LlamaIndex",
    purpose:
      "Prepare Alfred for optional document indexing and retrieval workflows when richer local executive search is needed.",
    whenToUse: [
      "Use when executive knowledge volume has grown beyond simple vault scanning and needs structured retrieval support.",
      "Keep it optional until local knowledge quality and source discipline are stable.",
    ],
    prerequisites: [
      "A working Alfred local environment with `.venv` and frontend dependencies installed.",
      "A validated Obsidian vault path or evidence inventory ready for indexing.",
      "Python package installation approval for the optional retrieval stack.",
    ],
    installSteps: [
      "Review the deployment document before installing any optional packages.",
      "Create an isolated dependency list for the retrieval service rather than mixing it into core Alfred runtime requirements.",
      "Record the intended install bundle or config template under `downloads/deployment/` when the service is introduced.",
    ],
    configurationSteps: [
      "Select the vault or evidence paths that should be indexed.",
      "Define which entity classes are in scope for retrieval.",
      "Capture service settings in versioned configuration rather than frontend state.",
    ],
    validationCommands: [
      "python build_executive_knowledge.py",
      "python build_knowledge_graph.py",
      "pytest",
    ],
    troubleshooting: [
      "If retrieval quality is poor, verify canonical entity resolution before adding more indexing complexity.",
      "If indexing is slow, reduce scope to the executive vault subset first.",
    ],
    downloads: [
      "docs/deployment/LLAMAINDEX_DEPLOYMENT.md",
      "downloads/deployment/README.md",
    ],
    status: "Not installed",
    documentPath: "docs/deployment/LLAMAINDEX_DEPLOYMENT.md",
  },
  {
    title: "LLM Wiki Enrichment",
    path: "/llm-wiki-enrichment",
    shortLabel: "LLM Wiki Enrichment",
    purpose:
      "Define the optional enrichment pattern for generating wiki-style executive context around core entities without changing canonical evidence rules.",
    whenToUse: [
      "Use when concise background context would materially improve executive understanding of companies, people, or decisions.",
      "Keep it off when evidence quality is still being normalised and direct notes remain sufficient.",
    ],
    prerequisites: [
      "Canonical entities from the Executive Knowledge Builder and Entity Resolution.",
      "A clear distinction between evidence-backed knowledge and generated enrichment.",
      "An agreed output location for enrichment artefacts.",
    ],
    installSteps: [
      "Review the enrichment operating model and keep it separate from the core runtime path.",
      "Prepare placeholder templates for enriched outputs before enabling any generation.",
      "Store prospective bundles or templates under `downloads/deployment/`.",
    ],
    configurationSteps: [
      "Choose which entity types are eligible for enrichment.",
      "Set budgets or review thresholds before any generation is enabled.",
      "Define how enrichment outputs will be linked back to evidence without becoming the source of truth.",
    ],
    validationCommands: [
      "python build_executive_knowledge.py",
      "python build_knowledge_graph.py",
      "pytest",
    ],
    troubleshooting: [
      "If enriched content drifts from evidence, reduce scope and require explicit review.",
      "If duplicate pages emerge, improve canonical entity naming before expanding enrichment.",
    ],
    downloads: [
      "docs/deployment/LLM_WIKI_ENRICHMENT.md",
      "downloads/deployment/README.md",
    ],
    status: "Not installed",
    documentPath: "docs/deployment/LLM_WIKI_ENRICHMENT.md",
  },
  {
    title: "LLM APIs",
    path: "/llm-apis",
    shortLabel: "LLM APIs",
    purpose:
      "Document how Alfred should be configured to use external or local LLM endpoints without embedding secrets into the UI.",
    whenToUse: [
      "Use when Alfred needs model-backed enrichment, reasoning, or retrieval beyond the current local deterministic flows.",
      "Keep configuration explicit and auditable before enabling any model routing.",
    ],
    prerequisites: [
      "A chosen API provider or local model endpoint.",
      "A secure secret storage approach outside the frontend.",
      "Operational rules for token limits, model selection, and fallback behaviour.",
    ],
    installSteps: [
      "Document the intended provider or endpoint contract first.",
      "Create config templates without storing live credentials in the repository.",
      "Place example templates or generated artefacts in `downloads/deployment/` once approved.",
    ],
    configurationSteps: [
      "Set endpoint names, model aliases, and environment variable expectations.",
      "Expose secret status and connectivity state in Admin or System Health later, not raw values.",
      "Define safe defaults for timeouts, retries, and budget limits.",
    ],
    validationCommands: [
      "python build_dashboard_api.py",
      "python build_everything.py",
      "pytest",
    ],
    troubleshooting: [
      "If API calls fail, validate endpoint reachability and secret injection outside the browser.",
      "If outputs vary too widely, tighten model routing and prompt governance before expanding usage.",
    ],
    downloads: [
      "docs/deployment/LLM_API_CONFIGURATION.md",
      "downloads/deployment/README.md",
    ],
    status: "Not installed",
    documentPath: "docs/deployment/LLM_API_CONFIGURATION.md",
  },
  {
    title: "Deep Research",
    path: "/deep-research",
    shortLabel: "Deep Research",
    purpose:
      "Define the operating envelope for optional high-cost research workflows without enabling them in the current release.",
    whenToUse: [
      "Use only when lightweight enrichment is insufficient and the executive question justifies deeper retrieval and budget spend.",
      "Keep disabled in routine daily operation until controls, budgets, and review checkpoints exist.",
    ],
    prerequisites: [
      "A model/API configuration capable of longer-running retrieval tasks.",
      "Explicit budget and token controls.",
      "A review process for research outputs before they influence executive state.",
    ],
    installSteps: [
      "Document the control model before any implementation work starts.",
      "Prepare placeholder bundles or templates in `downloads/deployment/` rather than wiring live jobs.",
      "Keep the feature inactive until governance is approved.",
    ],
    configurationSteps: [
      "Define token budgets, concurrency limits, and approval rules.",
      "Separate research outputs from canonical evidence until explicitly reviewed.",
      "Capture monitoring and cost-reporting expectations before activation.",
    ],
    validationCommands: [
      "python build_everything.py",
      "pytest",
    ],
    troubleshooting: [
      "If research cost or latency is unclear, do not enable the workflow.",
      "If outputs cannot be audited back to sources, keep the mode disabled.",
    ],
    downloads: [
      "docs/deployment/DEEP_RESEARCH_CONFIGURATION.md",
      "downloads/deployment/README.md",
    ],
    status: "Not installed",
    documentPath: "docs/deployment/DEEP_RESEARCH_CONFIGURATION.md",
  },
];

export const DEPLOYMENT_INDEX_PATH = "docs/deployment/DEPLOYMENT_LINKS_INDEX.md";
export const DEPLOYMENT_DOWNLOADS_PATH = "downloads/deployment/README.md";
