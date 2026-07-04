import { SectionCard } from "@/components/SectionCard";

const HELP_SECTIONS: Array<[string, string[]]> = [
  [
    "What Alfred Is",
    [
      "Alfred is an executive operating surface for prioritisation, navigation, and decision support.",
      "The UI is read-only and renders canonical backend intelligence rather than recomputing its own models.",
    ],
  ],
  [
    "Source Of Truth",
    [
      "Obsidian is the source of truth for executive knowledge.",
      "ExecutiveState is recomputed from canonical evidence after important changes are written back.",
    ],
  ],
  [
    "Dashboard Role",
    [
      "The dashboard is the interaction layer, not the primary knowledge store.",
      "It should help capture intent, navigate work, and surface what matters next.",
    ],
  ],
  [
    "Dashboard-entered Content",
    [
      "Dashboard-entered content is captured first in Alfred’s interaction/action ledger.",
      "Important content should be queued for write-back into Obsidian as markdown evidence.",
      "Write-back is not implemented in this phase.",
    ],
  ],
  [
    "Current Mode vs Future Sync",
    [
      "Current mode is local Mac-first usage.",
      "Future mode is hosted/VPS/API sync so Mac, VPS, Telegram, and browser all see the same state.",
    ],
  ],
  [
    "How Actions Are Captured",
    [
      "Interim model: Dashboard input -> Alfred interaction ledger -> Obsidian write-back queue -> markdown evidence note -> ExecutiveState recomputed.",
      "This keeps frontend capture safe while preserving canonical evidence discipline.",
    ],
  ],
  [
    "Basic Enrichment vs Deep Research",
    [
      "Basic enrichment is lightweight executive shaping and routing from existing intelligence.",
      "Deep Research is a future mode with stricter budgets and heavier retrieval; it is not implemented here.",
    ],
  ],
  [
    "How To Use Ask Alfred",
    [
      "Use the persistent Ask Alfred bar at the bottom of the app to jump to the Ask Alfred page.",
      "This v1 UI resolves against precomputed dashboard responses rather than live arbitrary query execution.",
    ],
  ],
  [
    "Troubleshooting",
    [
      "If the UI looks stale, rerun `python build_dashboard_api.py` or `python build_everything.py`.",
      "If the browser cannot load data, verify `output/Dashboard_Home.json` is being regenerated and the frontend build is current.",
    ],
  ],
];

export function HelpPage() {
  return (
    <div className="space-y-6">
      {HELP_SECTIONS.map(([title, items]) => (
        <SectionCard key={title} title={title} kicker="Work Instructions">
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
