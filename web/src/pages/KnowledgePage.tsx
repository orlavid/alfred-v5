import { SectionCard } from "@/components/SectionCard";
import type { DashboardPayload } from "@/types";

export function KnowledgePage({ data }: { data: DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Knowledge" kicker="Model">
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          {data.knowledge.summary.map((item) => (
            <li key={item}>- {item}</li>
          ))}
        </ul>
      </SectionCard>
      <div className="grid gap-6 lg:grid-cols-2">
        <SectionCard title="Entity Inventory" kicker="Coverage">
          <div className="grid gap-4 sm:grid-cols-2">
            {Object.entries(data.knowledge.entity_counts).map(([key, value]) => (
              <div key={key} className="rounded-2xl bg-white/70 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-accent">{key}</p>
                <p className="mt-3 font-serif text-3xl">{value}</p>
              </div>
            ))}
          </div>
        </SectionCard>
        <SectionCard title="Relationship Graph" kicker="Topology">
          <div className="grid gap-4 text-sm leading-6 text-ink/80">
            <p><span className="font-semibold text-ink">Nodes:</span> {data.knowledge.graph.node_count}</p>
            <p><span className="font-semibold text-ink">Edges:</span> {data.knowledge.graph.edge_count}</p>
            <p><span className="font-semibold text-ink">Highest Connectivity:</span> {data.knowledge.graph.top_nodes.join(", ") || "None"}</p>
          </div>
        </SectionCard>
      </div>
    </div>
  );
}
