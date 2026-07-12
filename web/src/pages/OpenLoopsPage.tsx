import { useMemo } from "react";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import { loadOpenLoopsDomain } from "@/lib/loadDashboard";
import { useDomainPayload } from "@/lib/useDomainPayload";
import type { DashboardBootstrapPayload, DashboardPayload, OpenLoopsDomainPayload } from "@/types";

export function OpenLoopsPage({ data }: { data: DashboardBootstrapPayload | DashboardPayload }) {
  const embeddedDomain = useMemo(
    () => ("items" in data.open_loops ? (data.open_loops as OpenLoopsDomainPayload) : null),
    [data.open_loops],
  );
  const { data: domain, error } = useDomainPayload(embeddedDomain, loadOpenLoopsDomain);

  return (
    <div className="space-y-6">
      <SectionCard title="Open Loops" kicker="Management View">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Critical</p>
            <p className="mt-3 font-serif text-3xl">{data.operating_picture.open_loop_pressure.critical}</p>
          </div>
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Waiting For</p>
            <p className="mt-3 font-serif text-3xl">{data.operating_picture.open_loop_pressure.waiting_for}</p>
          </div>
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Missing Owners</p>
            <p className="mt-3 font-serif text-3xl">{data.operating_picture.open_loop_pressure.missing_owners}</p>
          </div>
        </div>
      </SectionCard>
      <SectionCard title="Priority Now" kicker="Daily Brief">
        <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {data.daily_brief.open_loops_blocking_progress.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
          <div className="rounded-2xl border border-ink/10 bg-white/70 p-4 text-sm leading-6 text-ink/80">
            <p><span className="font-semibold text-ink">Full Canonical Count:</span> {data.open_loops.counts.total}</p>
            <p><span className="font-semibold text-ink">Waiting For:</span> {data.open_loops.counts.waiting_for}</p>
            <p><span className="font-semibold text-ink">Stalled Projects:</span> {data.open_loops.counts.stalled_projects}</p>
          </div>
        </div>
      </SectionCard>
      <SectionCard title="Full Open Loop Collection" kicker="Canonical">
        {error ? (
          <div className="mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm leading-6 text-red-800">
            {error}
          </div>
        ) : null}
        {!error && !domain ? (
          <div className="mb-4 rounded-2xl border border-ink/10 bg-white/70 p-4 text-sm leading-6 text-ink/70">
            Reading the latest published open-loop register.
          </div>
        ) : null}
        <div className="space-y-4">
          {domain?.items.map((item) => (
            <article key={item.work_item_id} className="rounded-2xl border border-ink/10 bg-white/70 p-5">
              <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <StatusPill value={item.classification} />
                    <StatusPill value={item.priority} />
                    <StatusPill value={item.status} />
                    <StatusPill value={item.confidence} />
                  </div>
                  <h3 className="font-serif text-2xl text-ink">{item.title}</h3>
                  <p className="text-sm leading-6 text-ink/75">{item.source_path}</p>
                </div>
                <div className="rounded-2xl bg-paper p-4 text-sm leading-6 text-ink/80 md:min-w-72">
                  <p><span className="font-semibold text-ink">Owner:</span> {item.owner}</p>
                  <p><span className="font-semibold text-ink">Status:</span> {item.status}</p>
                  <p><span className="font-semibold text-ink">Source Date:</span> {item.source_date}</p>
                  <p><span className="font-semibold text-ink">Buckets:</span> {item.buckets.join(", ") || "Not defined"}</p>
                </div>
              </div>
              <div className="mt-4 grid gap-4 md:grid-cols-2">
                <div className="rounded-2xl bg-paper p-4 text-sm leading-6 text-ink/80">
                  <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">Related Entities</p>
                  <p className="mt-2">{item.related_entities.join(", ") || "No evidence found"}</p>
                  <p className="mt-3 text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">Evidence</p>
                  <ul className="mt-2 space-y-1">
                    {item.evidence_paths.map((path) => (
                      <li key={path}>{path}</li>
                    ))}
                  </ul>
                </div>
                <div className="rounded-2xl bg-paper p-4 text-sm leading-6 text-ink/80">
                  <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">Provenance</p>
                  <ul className="mt-2 space-y-1">
                    {Object.entries(item.provenance).map(([key, paths]) => (
                      <li key={key}>
                        <span className="font-semibold text-ink">{key.replaceAll("_", " ")}:</span> {paths.join(", ")}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </article>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
