import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardBootstrapPayload, DashboardPayload } from "@/types";

export function ExecutiveSummaryPage({ data }: { data: DashboardBootstrapPayload | DashboardPayload }) {
  return (
    <div className="space-y-6">
      <SectionCard title="Executive Summary" kicker="Command" action={<StatusPill value={data.generated_from.confidence} />}>
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          {data.operating_picture.summary.map((item) => (
            <li key={item}>- {item}</li>
          ))}
          {data.knowledge.summary.slice(0, 2).map((item) => (
            <li key={item}>- {item}</li>
          ))}
        </ul>
      </SectionCard>
    </div>
  );
}
