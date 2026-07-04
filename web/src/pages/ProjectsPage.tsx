import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardPayload } from "@/types";

export function ProjectsPage({ data }: { data: DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Projects" kicker="Delivery">
        <div className="grid gap-4 md:grid-cols-3">
          {Object.entries(data.projects.health).map(([key, value]) => (
            <div key={key} className="rounded-2xl bg-white/70 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-accent">{key.replace("_", " ")}</p>
              <p className="mt-3 font-serif text-3xl">{value}</p>
            </div>
          ))}
        </div>
      </SectionCard>
      <SectionCard title="Project Register" kicker="Status">
        <div className="space-y-4">
          {data.projects.items.map((item) => (
            <div key={item.title} className="rounded-2xl border border-ink/10 bg-white/70 p-5">
              <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                <div>
                  <h3 className="font-serif text-2xl">{item.title}</h3>
                  <p className="mt-2 text-sm leading-6 text-ink/75">{item.recommendation}</p>
                </div>
                <StatusPill value={item.status} />
              </div>
              <div className="mt-4 grid gap-4 text-sm leading-6 text-ink/80 md:grid-cols-2">
                <p><span className="font-semibold text-ink">Objective Linkage:</span> {item.objective_linkage.join(", ") || "None"}</p>
                <p><span className="font-semibold text-ink">Risk:</span> {item.risk}</p>
              </div>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
