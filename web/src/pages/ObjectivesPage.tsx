import { Link } from "react-router-dom";
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
          <Link key={item.objective_id} to={item.route} className="block">
            <SectionCard
              title={item.title}
              kicker="Objective"
              action={<span className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Open objective</span>}
              className="h-full transition-transform hover:-translate-y-1"
            >
              <div className="space-y-4 text-sm leading-6 text-ink/80">
                <div className="flex flex-wrap gap-3">
                  <StatusPill value={item.lifecycle} />
                  <StatusPill value={item.health} />
                  <StatusPill value={item.confidence} />
                  {item.stale_evidence ? <StatusPill value="Stale" /> : null}
                </div>
                <div className="grid gap-3 sm:grid-cols-2">
                  <Metric label="Owner" value={item.owner} />
                  <Metric label="Last Activity" value={item.last_meaningful_activity} />
                  <Metric label="Next Checkpoint" value={item.next_checkpoint_or_deadline} />
                  <Metric label="Progress" value={item.progress_indicator} />
                  <Metric label="Projects" value={String(item.supporting_project_count)} />
                  <Metric label="Decisions" value={String(item.linked_decision_count)} />
                  <Metric label="Open Actions" value={String(item.open_action_count)} />
                  <Metric label="Confidence" value={item.confidence} />
                </div>
                <p><span className="font-semibold text-ink">Key Risk or Blocker:</span> {item.key_risk_or_blocker}</p>
                <p><span className="font-semibold text-ink">Next Action:</span> {item.recommended_next_action}</p>
                {item.missing_fields.length ? (
                  <p><span className="font-semibold text-ink">Missing:</span> {item.missing_fields.join(" ")}</p>
                ) : null}
              </div>
            </SectionCard>
          </Link>
        ))}
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-white/70 p-3">
      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">{label}</p>
      <p className="mt-2 text-sm text-ink">{value}</p>
    </div>
  );
}
