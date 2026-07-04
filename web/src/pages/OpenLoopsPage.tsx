import { SectionCard } from "@/components/SectionCard";
import type { DashboardPayload } from "@/types";

export function OpenLoopsPage({ data }: { data: DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Open Loops" kicker="Placeholder Route">
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
      <SectionCard title="Blocking Progress" kicker="Queue">
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          {data.daily_brief.open_loops_blocking_progress.map((item) => (
            <li key={item}>- {item}</li>
          ))}
        </ul>
      </SectionCard>
    </div>
  );
}
