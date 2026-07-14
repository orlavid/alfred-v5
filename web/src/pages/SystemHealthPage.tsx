import { SectionCard } from "@/components/SectionCard";
import type { DashboardBootstrapPayload } from "@/types";

export function SystemHealthPage({ data }: { data: DashboardBootstrapPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="System Health" kicker="Administration">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Operational Health</p>
            <p className="mt-3 font-serif text-3xl">{data.system_health.refresh_status.overall_health}</p>
          </div>
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Environment Score</p>
            <p className="mt-3 font-serif text-3xl">{data.system_health.refresh_status.environment_score}</p>
          </div>
        </div>
        <ul className="mt-4 space-y-2 text-sm leading-6 text-ink/80">
          {data.system_health.summary.map((line) => (
            <li key={line}>- {line}</li>
          ))}
        </ul>
      </SectionCard>

      <SectionCard title="Data Quality and Technical Alerts" kicker="Moved Out Of Executive View">
        <div className="space-y-4">
          {data.system_health.data_quality_alerts.length ? data.system_health.data_quality_alerts.map((item) => (
            <article key={`${item.title}-${item.source_path}`} className="rounded-2xl border border-ink/10 bg-white/70 p-4 text-sm leading-6 text-ink/80">
              <p className="font-semibold text-ink">{item.title}</p>
              <p className="mt-2">{item.summary}</p>
              <p className="mt-2 text-xs uppercase tracking-[0.18em] text-accent">{item.source_path || "No source path recorded"}</p>
            </article>
          )) : <p className="text-sm leading-6 text-ink/70">No technical alerts are currently being diverted from executive view.</p>}
        </div>
      </SectionCard>
    </div>
  );
}
