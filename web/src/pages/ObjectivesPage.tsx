import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardPayload } from "@/types";

export function ObjectivesPage({ data }: { data: DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Objectives" kicker="Lifecycle">
        <div className="grid gap-4 md:grid-cols-3">
          {Object.entries(data.objectives.health).map(([key, value]) => (
            <div key={key} className="rounded-2xl bg-white/70 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-accent">{key.replace("_", " ")}</p>
              <p className="mt-3 font-serif text-3xl">{value}</p>
            </div>
          ))}
        </div>
      </SectionCard>
      <div className="grid gap-6 lg:grid-cols-2">
        {data.objectives.items.map((item) => (
          <SectionCard key={item.title} title={item.title} kicker="Objective">
            <div className="space-y-4 text-sm leading-6 text-ink/80">
              <div className="flex flex-wrap gap-3">
                <StatusPill value={item.lifecycle} />
                <StatusPill value={item.confidence} />
                {item.stale_evidence ? <StatusPill value="Stale" /> : null}
              </div>
              <p><span className="font-semibold text-ink">Supporting Projects:</span> {item.supporting_projects.join(", ") || "None"}</p>
              <p><span className="font-semibold text-ink">Linked Decisions:</span> {item.linked_decisions.join(", ") || "None"}</p>
              <p><span className="font-semibold text-ink">Next Action:</span> {item.recommended_next_action}</p>
            </div>
          </SectionCard>
        ))}
      </div>
    </div>
  );
}
