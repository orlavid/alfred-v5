import { SectionCard } from "@/components/SectionCard";

const ADMIN_SECTIONS: Array<[string, string[]]> = [
  [
    "Production Requirement",
    [
      "Authentication will be required before production deployment.",
      "The old email authentication concept is carried forward as a requirement, not an implementation in this phase.",
    ],
  ],
  [
    "Access Model",
    [
      "Admin will eventually govern user and session management.",
      "Email allow-list rules will define which identities may access Alfred.",
      "Access logs should be visible for governance and audit review.",
    ],
  ],
  [
    "Secrets And API Controls",
    [
      "Secrets status should be visible without revealing actual secret values.",
      "Admin should control API and token limits, including deeper research budgets later.",
    ],
  ],
  [
    "Knowledge And Sync Controls",
    [
      "Admin should expose the Obsidian vault path.",
      "Admin should manage sync and write-back queue settings.",
      "Write-back itself is not implemented in this phase.",
    ],
  ],
  [
    "Research Controls",
    [
      "Deep research and token budget controls belong here in the future.",
      "Deep research is intentionally not implemented yet.",
    ],
  ],
];

export function AdminSecurityPage() {
  return (
    <div className="space-y-6">
      {ADMIN_SECTIONS.map(([title, items]) => (
        <SectionCard key={title} title={title} kicker="Admin / Security Placeholder">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {items.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </SectionCard>
      ))}
    </div>
  );
}
