import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardPayload } from "@/types";

export function MeetingsPage({ data }: { data: DashboardPayload }) {
  const meeting = data.meetings;
  return (
    <div className="space-y-6">
      <SectionCard title={meeting.subject} kicker="Meeting Intelligence" action={<StatusPill value={meeting.confidence} />}>
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          {meeting.executive_summary.map((item) => (
            <li key={item}>- {item}</li>
          ))}
        </ul>
      </SectionCard>
      <div className="grid gap-6 xl:grid-cols-2">
        <SectionCard title="Related Context" kicker="Links">
          <div className="space-y-3 text-sm leading-6 text-ink/80">
            <p><span className="font-semibold text-ink">People:</span> {meeting.related_people.join(", ") || "None"}</p>
            <p><span className="font-semibold text-ink">Projects:</span> {meeting.related_projects.join(", ") || "None"}</p>
            <p><span className="font-semibold text-ink">Companies:</span> {meeting.related_companies.join(", ") || "None"}</p>
            <p><span className="font-semibold text-ink">Objectives:</span> {meeting.related_objectives.join(", ") || "None"}</p>
            <p><span className="font-semibold text-ink">Decisions:</span> {meeting.related_decisions.join(", ") || "None"}</p>
          </div>
        </SectionCard>
        <SectionCard title="Discussion Setup" kicker="Readout">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {meeting.recommended_discussion.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </SectionCard>
      </div>
    </div>
  );
}
