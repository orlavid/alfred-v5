import { SectionCard } from "@/components/SectionCard";
import type { DashboardPayload } from "@/types";

export function FollowupsPage({ data }: { data: DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Follow-ups" kicker="Placeholder Route">
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
      <SectionCard title="Today’s Follow-up Queue" kicker="Actionable">
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          {data.daily_brief.followups_due_today.map((item) => (
            <li key={item}>- {item}</li>
          ))}
        </ul>
      </SectionCard>
    </div>
  );
}
