import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardBootstrapPayload, DashboardPayload } from "@/types";

export function BoardPage({ data }: { data: DashboardBootstrapPayload | DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Board Governance" kicker="Committee">
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          {data.board.summary.map((item) => (
            <li key={item}>- {item}</li>
          ))}
        </ul>
      </SectionCard>
      <SectionCard title="Board Members" kicker="Registry">
        <div className="grid gap-4 xl:grid-cols-2">
          {data.board.members.map((member) => (
            <article key={member.name} className="rounded-2xl border border-ink/10 bg-white/70 p-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-accent">{member.role}</p>
                  <h3 className="mt-2 font-serif text-2xl">{member.name}</h3>
                </div>
                <StatusPill value={member.status} />
              </div>
              <p className="mt-3 text-sm leading-6 text-ink/80">{member.purpose}</p>
              <p className="mt-3 text-sm leading-6 text-ink/80">
                <span className="font-semibold text-ink">Responsibilities:</span> {member.responsibilities.join(", ")}
              </p>
              <p className="mt-2 text-sm leading-6 text-ink/80">
                <span className="font-semibold text-ink">Meeting Role:</span> {member.meeting_role}
              </p>
            </article>
          ))}
        </div>
      </SectionCard>
      <div className="grid gap-6 lg:grid-cols-2">
        <SectionCard title="Weekly Board Meeting" kicker="Cadence">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {data.board.weekly_meeting.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </SectionCard>
        <SectionCard title="Monthly Board Meeting" kicker="Cadence">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {data.board.monthly_meeting.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </SectionCard>
      </div>
    </div>
  );
}
