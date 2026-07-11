import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardPayload } from "@/types";

export function FollowupsPage({ data }: { data: DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Follow-ups" kicker="Management View">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Overdue</p>
            <p className="mt-3 font-serif text-3xl">{data.operating_picture.followup_pressure.overdue}</p>
          </div>
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Due Today</p>
            <p className="mt-3 font-serif text-3xl">{data.operating_picture.followup_pressure.due_today}</p>
          </div>
          <div className="rounded-2xl bg-white/70 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-accent">High Priority</p>
            <p className="mt-3 font-serif text-3xl">{data.operating_picture.followup_pressure.high_priority}</p>
          </div>
        </div>
      </SectionCard>
      <SectionCard title="Priority Now" kicker="Daily Brief">
        <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {data.daily_brief.followups_due_today.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
          <div className="rounded-2xl border border-ink/10 bg-white/70 p-4 text-sm leading-6 text-ink/80">
            <p><span className="font-semibold text-ink">Full Canonical Count:</span> {data.followups.counts.total}</p>
            <p><span className="font-semibold text-ink">Due This Week:</span> {data.followups.counts.due_this_week}</p>
            <p><span className="font-semibold text-ink">Waiting On Others:</span> {data.followups.counts.waiting_on_others}</p>
          </div>
        </div>
      </SectionCard>
      <SectionCard title="Full Follow-up Collection" kicker="Canonical">
        <div className="space-y-4">
          {data.followups.items.map((item) => (
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
                  <p><span className="font-semibold text-ink">Due Date:</span> {item.due_date}</p>
                  <p><span className="font-semibold text-ink">Source Date:</span> {item.source_date}</p>
                  <p><span className="font-semibold text-ink">Buckets:</span> {item.buckets.join(", ") || "Not defined"}</p>
                </div>
              </div>
              <div className="mt-4 grid gap-4 md:grid-cols-2">
                <div className="rounded-2xl bg-paper p-4 text-sm leading-6 text-ink/80">
                  <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">Evidence</p>
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
