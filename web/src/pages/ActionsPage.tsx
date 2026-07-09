import { SectionCard } from "@/components/SectionCard";
import type { DashboardPayload } from "@/types";

export function ActionsPage({ data }: { data: DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Actions" kicker="Placeholder Route">
        <p className="text-sm leading-6 text-ink/75">
          This page is the future action ledger surface. In the interim model, dashboard-entered actions should flow into Alfred’s interaction/action ledger and then into the Obsidian write-back queue before ExecutiveState is recomputed.
        </p>
      </SectionCard>
      <div className="grid gap-6 xl:grid-cols-2">
        <SectionCard title="Plan Today" kicker="Execution">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {data.plan_today.map((item, index) => (
              <li key={`${item.type}-${index}`}>- {item.summary}</li>
            ))}
          </ul>
        </SectionCard>
        <SectionCard title="Recommended Next Actions" kicker="Reasoning">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {data.ask_alfred.responses[0]?.recommended_next_actions.map((item) => (
              <li key={item}>- {item}</li>
            )) ?? ["- No recommended actions available."]}
          </ul>
        </SectionCard>
      </div>
    </div>
  );
}
