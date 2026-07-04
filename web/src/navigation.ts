export type ControlSection = {
  rail: string;
  title: string;
  color: string;
  items: Array<{
    label: string;
    path: string;
  }>;
};

export const CONTROL_SECTIONS: ControlSection[] = [
  {
    rail: "C",
    title: "Command",
    color: "bg-signal text-white",
    items: [
      { label: "Dashboard", path: "/" },
      { label: "Daily Brief", path: "/daily-brief" },
      { label: "Ask Alfred", path: "/ask-alfred" },
      { label: "Executive Summary", path: "/executive-summary" },
    ],
  },
  {
    rail: "O",
    title: "Objectives",
    color: "bg-accent text-white",
    items: [
      { label: "Objectives", path: "/objectives" },
      { label: "Projects", path: "/projects" },
      { label: "Programmes", path: "/programmes" },
      { label: "Milestones", path: "/milestones" },
    ],
  },
  {
    rail: "N",
    title: "kNowledge",
    color: "bg-pine text-white",
    items: [
      { label: "Meetings", path: "/meetings" },
      { label: "People", path: "/people" },
      { label: "Companies", path: "/companies" },
      { label: "Decisions", path: "/decisions" },
      { label: "Knowledge Graph", path: "/knowledge-graph" },
    ],
  },
  {
    rail: "T",
    title: "Tasks",
    color: "bg-ink text-white",
    items: [
      { label: "Actions", path: "/actions" },
      { label: "Follow-ups", path: "/follow-ups" },
      { label: "Open Loops", path: "/open-loops" },
      { label: "Workflow", path: "/workflow" },
    ],
  },
  {
    rail: "R",
    title: "Risks",
    color: "bg-[#7e3b3b] text-white",
    items: [
      { label: "Risks", path: "/risks" },
      { label: "Board", path: "/board" },
      { label: "Governance", path: "/governance" },
      { label: "Executive Health", path: "/executive-health" },
      { label: "Compliance", path: "/compliance" },
    ],
  },
  {
    rail: "O",
    title: "Operations",
    color: "bg-[#355c7d] text-white",
    items: [
      { label: "Admin", path: "/admin" },
      { label: "Security", path: "/security" },
      { label: "AI Models", path: "/ai-models" },
      { label: "Integrations", path: "/integrations" },
      { label: "System Health", path: "/system-health" },
    ],
  },
  {
    rail: "L",
    title: "Library",
    color: "bg-[#6b6a4f] text-white",
    items: [
      { label: "Help", path: "/help" },
      { label: "Knowledge Base", path: "/knowledge-base" },
      { label: "Obsidian", path: "/obsidian" },
      { label: "Documentation", path: "/documentation" },
      { label: "Prompt Library", path: "/prompt-library" },
      { label: "External Links", path: "/external-links" },
    ],
  },
];

export function findNavigationEntry(pathname: string) {
  const normalised = pathname === "/knowledge" ? "/knowledge-graph" : pathname;
  for (const section of CONTROL_SECTIONS) {
    const item = section.items.find((value) => value.path === normalised);
    if (item) {
      return { section, item };
    }
  }
  return null;
}
