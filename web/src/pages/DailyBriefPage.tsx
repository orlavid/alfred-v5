import { SectionCard } from "@/components/SectionCard";
import type { DashboardPayload } from "@/types";

const SECTIONS: Array<[string, keyof DashboardPayload["daily_brief"]]> = [
  ["Executive Health", "executive_health"],
  ["Overnight Changes", "overnight_changes"],
  ["Top Three Priorities", "top_three_priorities"],
  ["Meetings Requiring Preparation", "meetings_requiring_preparation"],
  ["Follow-ups Due Today", "followups_due_today"],
  ["Open Loops Blocking Progress", "open_loops_blocking_progress"],
  ["Risks Escalating", "risks_escalating"],
  ["Decisions Awaiting You", "decisions_awaiting_you"],
  ["Recommended Agenda", "recommended_agenda"],
  ["One-page Executive Summary", "one_page_executive_summary"],
];

export function DailyBriefPage({ data }: { data: DashboardPayload }) {
  return (
    <div className="grid gap-6 xl:grid-cols-2">
      {SECTIONS.map(([title, key]) => (
        <SectionCard key={key} title={title} kicker="Daily Brief">
          <ul className="space-y-2 text-sm leading-6 text-ink/80">
            {data.daily_brief[key].map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </SectionCard>
      ))}
    </div>
  );
}
