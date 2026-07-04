import { Link } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardPayload } from "@/types";

type DashboardPageProps = {
  data: DashboardPayload;
};

const PATH_MAP: Record<string, string> = {
  Priorities: "/",
  Meetings: "/meetings",
  "Follow-ups": "/daily-brief",
  "Open Loops": "/daily-brief",
  Decisions: "/daily-brief",
};

export function DashboardPage({ data }: DashboardPageProps) {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-white/70 bg-ink p-8 text-white shadow-panel">
        <p className="text-xs uppercase tracking-[0.3em] text-white/60">Executive Home</p>
        <div className="mt-4 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <h2 className="font-serif text-4xl">What do I need to focus on next?</h2>
            <p className="mt-4 text-lg text-white/75">{data.next_best_action.action}</p>
          </div>
          <div className="rounded-3xl bg-white/10 p-5">
            <p className="text-xs uppercase tracking-[0.24em] text-white/60">Interruption Policy</p>
            <p className="mt-3 text-sm font-medium text-white">{data.interruption_policy.rule}</p>
          </div>
        </div>
      </section>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <SectionCard title="Burning Fires" kicker="Home">
          <div className="space-y-4">
            {data.burning_fires.map((item) => (
              <div key={`${item.type}-${item.summary}`} className="rounded-2xl border border-ink/10 bg-white/70 p-4">
                <div className="mb-3 flex items-center justify-between gap-3">
                  <StatusPill value={item.type.replace("_", " ")} />
                </div>
                <p className="text-sm leading-6 text-ink">{item.summary}</p>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Next Best Action" kicker="Today">
          <div className="space-y-4">
            <StatusPill value={data.next_best_action.priority} />
            <h3 className="font-serif text-2xl text-ink">{data.next_best_action.action}</h3>
            <p className="text-sm leading-6 text-ink/80">{data.next_best_action.why_it_matters}</p>
            <div className="rounded-2xl bg-ink px-4 py-3 text-sm text-white">
              Confidence: {data.next_best_action.confidence}
            </div>
          </div>
        </SectionCard>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <SectionCard title="Plan Today" kicker="Execution">
          <ol className="space-y-3">
            {data.plan_today.map((item, index) => (
              <li key={item} className="flex gap-4 rounded-2xl border border-ink/10 bg-white/60 p-4">
                <span className="flex h-9 w-9 flex-none items-center justify-center rounded-full bg-accent text-sm font-semibold text-white">
                  {index + 1}
                </span>
                <p className="text-sm leading-6 text-ink">{item}</p>
              </li>
            ))}
          </ol>
        </SectionCard>

        <SectionCard title="Operating Picture" kicker="Signal">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-2xl bg-white/70 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-accent">Health</p>
              <p className="mt-3 font-serif text-3xl">{data.operating_picture.overall_health}</p>
            </div>
            <div className="rounded-2xl bg-white/70 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-accent">Meeting Focus</p>
              <p className="mt-3 font-serif text-3xl">{data.operating_picture.meeting_focus}</p>
            </div>
            <div className="rounded-2xl bg-white/70 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-accent">Follow-up Pressure</p>
              <p className="mt-3 text-sm leading-6 text-ink">
                Overdue {data.operating_picture.followup_pressure.overdue}, due today {data.operating_picture.followup_pressure.due_today}, high priority {data.operating_picture.followup_pressure.high_priority}.
              </p>
            </div>
            <div className="rounded-2xl bg-white/70 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-accent">Open Loop Pressure</p>
              <p className="mt-3 text-sm leading-6 text-ink">
                Critical {data.operating_picture.open_loop_pressure.critical}, waiting {data.operating_picture.open_loop_pressure.waiting_for}, missing owners {data.operating_picture.open_loop_pressure.missing_owners}.
              </p>
            </div>
          </div>
          <ul className="mt-4 space-y-2 text-sm leading-6 text-ink/80">
            {data.operating_picture.summary.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </SectionCard>
      </div>

      <SectionCard title="Quick Navigation" kicker="Routes">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {data.navigation_priorities.map((item) => (
            <Link
              key={item.label}
              to={PATH_MAP[item.label] ?? "/"}
              className="rounded-2xl border border-ink/10 bg-white/70 p-4 transition hover:-translate-y-0.5 hover:border-accent/30"
            >
              <p className="font-semibold text-ink">{item.label}</p>
              <p className="mt-2 text-sm leading-6 text-ink/75">{item.reason}</p>
            </Link>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
