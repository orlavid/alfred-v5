import { Link, Navigate, useParams } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardPayload, LinkedObjectiveItem, ObjectiveDetail, SmartAssessmentDimension } from "@/types";

export function ObjectiveDetailPage({ data }: { data: DashboardPayload }) {
  const { objectiveId } = useParams();
  const detail = objectiveId ? data.objectives.details?.[objectiveId] : undefined;

  if (!objectiveId) {
    return <Navigate to="/objectives" replace />;
  }

  if (!detail) {
    return (
      <SectionCard title="Objective Not Found" kicker="Objective Workspace">
        <p className="text-sm leading-6 text-ink/70">No objective management workspace was found for this link.</p>
        <Link to="/objectives" className="mt-4 inline-flex text-sm font-semibold text-accent">
          Back to objectives
        </Link>
      </SectionCard>
    );
  }

  return (
    <div className="space-y-6">
      <SectionCard
        title={detail.title}
        kicker="Objective Workspace"
        action={<Link to="/objectives" className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Back to objectives</Link>}
      >
        <div className="space-y-4 text-sm leading-6 text-ink/80">
          <div className="flex flex-wrap gap-3">
            <StatusPill value={detail.current_status} />
            <StatusPill value={detail.rag_rating} />
            <StatusPill value={detail.evidence_confidence} />
            {detail.stale_evidence ? <StatusPill value="Stale" /> : null}
          </div>
          <p><span className="font-semibold text-ink">Executive Definition:</span> {detail.executive_definition}</p>
          <p><span className="font-semibold text-ink">Recommended Next Action:</span> {detail.recommended_next_action}</p>
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <Metric label="Owner" value={detail.owner} />
            <Metric label="Progress" value={detail.progress_assessment} />
            <Metric label="Last Activity" value={detail.last_meaningful_activity} />
            <Metric label="Next Checkpoint" value={detail.next_checkpoint_or_deadline} />
            <Metric label="Start Date" value={detail.start_date} />
            <Metric label="Target Date" value={detail.target_date} />
            <Metric label="Last Review" value={detail.last_review_date} />
            <Metric label="Next Review" value={detail.next_review_date} />
          </div>
        </div>
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-2">
        <SectionCard title="Management Links" kicker="Connected Work">
          <div className="space-y-5 text-sm leading-6 text-ink/80">
            <LinkedList title="Supporting Projects" items={detail.supporting_projects} empty="No evidence found." />
            <LinkedList title="Linked Decisions" items={detail.linked_decisions} empty="No evidence found." />
            <LinkedList title="Risks and Blockers" items={detail.risks_and_blockers} empty="No evidence found." />
            <LinkedList title="Relevant Meetings" items={detail.relevant_meetings} empty="No evidence found." />
            <LinkedList title="Related People" items={detail.related_people} empty="No evidence found." />
          </div>
        </SectionCard>

        <SectionCard title="Actions and Evidence" kicker="Execution">
          <div className="space-y-5 text-sm leading-6 text-ink/80">
            <WorkItemList title="Open Actions" items={detail.open_actions} empty="No evidence found." />
            <WorkItemList title="Follow-ups" items={detail.follow_ups} empty="No evidence found." />
            <EvidenceList title="Evidence Sources" items={detail.evidence_sources} />
            <BulletList title="Recent Changes" items={detail.recent_changes} />
            <BulletList title="Missing Information Requiring Attention" items={detail.missing_information} />
          </div>
        </SectionCard>
      </div>

      <SectionCard title="SMART Assessment" kicker="Quality">
        <div className="grid gap-4 xl:grid-cols-2">
          {Object.entries(detail.smart_assessment).map(([dimension, value]) => (
            <SmartCard key={dimension} dimension={dimension} value={value} />
          ))}
        </div>
        <div className="mt-6 rounded-3xl bg-white/70 p-5 text-sm leading-6 text-ink/80">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Proposed SMART Refinement</p>
          <ul className="mt-3 space-y-2">
            {detail.proposed_smart_refinement.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </div>
      </SectionCard>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-white/70 p-3">
      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">{label}</p>
      <p className="mt-2 text-sm text-ink">{value}</p>
    </div>
  );
}

function LinkedList({
  title,
  items,
  empty,
}: {
  title: string;
  items: Array<LinkedObjectiveItem & { type?: string }>;
  empty: string;
}) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      {items.length ? (
        <ul className="mt-3 space-y-3">
          {items.map((item) => (
            <li key={`${title}-${item.title}-${item.path}`} className="rounded-2xl bg-white/70 p-3">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="font-semibold text-ink">{item.title}</p>
                  <p>{item.reason}</p>
                  {item.path ? <p className="text-xs text-ink/60">{item.path}</p> : null}
                </div>
                <Link to={item.route} className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">
                  Open
                </Link>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3">{empty}</p>
      )}
    </div>
  );
}

function WorkItemList({
  title,
  items,
  empty,
}: {
  title: string;
  items: ObjectiveDetail["open_actions"];
  empty: string;
}) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      {items.length ? (
        <ul className="mt-3 space-y-3">
          {items.map((item) => (
            <li key={item.work_item_id} className="rounded-2xl bg-white/70 p-3">
              <div className="flex flex-wrap gap-2">
                <StatusPill value={item.type.replace("_", " ")} />
                <StatusPill value={item.status} />
                <StatusPill value={item.priority} />
              </div>
              <p className="mt-3 font-semibold text-ink">{item.title}</p>
              <p>{item.reason}</p>
              {item.path ? <p className="text-xs text-ink/60">{item.path}</p> : null}
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3">{empty}</p>
      )}
    </div>
  );
}

function EvidenceList({ title, items }: { title: string; items: ObjectiveDetail["evidence_sources"] }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      <ul className="mt-3 space-y-3">
        {items.map((item) => (
          <li key={`${item.label}-${item.path}`} className="rounded-2xl bg-white/70 p-3">
            <p className="font-semibold text-ink">{item.label}</p>
            <p>{item.reason}</p>
            <p className="text-xs text-ink/60">{item.path}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

function BulletList({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      <ul className="mt-3 space-y-2">
        {items.map((item) => (
          <li key={`${title}-${item}`}>- {item}</li>
        ))}
      </ul>
    </div>
  );
}

function SmartCard({ dimension, value }: { dimension: string; value: SmartAssessmentDimension }) {
  return (
    <div className="rounded-3xl bg-white/70 p-5 text-sm leading-6 text-ink/80">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{dimension}</p>
      <p className="mt-2 font-semibold text-ink">{value.current_assessment}</p>
      <p className="mt-3"><span className="font-semibold text-ink">Evidence:</span> {value.evidence.join(", ")}</p>
      <p className="mt-3"><span className="font-semibold text-ink">Weak or Missing:</span> {value.missing_or_weak_definition}</p>
      <p className="mt-3"><span className="font-semibold text-ink">Suggested Improvement:</span> {value.suggested_improvement}</p>
    </div>
  );
}
