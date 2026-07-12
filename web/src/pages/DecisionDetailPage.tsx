import { Link, Navigate, useParams } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import { useMemo } from "react";
import { loadDecisionsDomain } from "@/lib/loadDashboard";
import { useDomainPayload } from "@/lib/useDomainPayload";
import type { DashboardBootstrapPayload, DashboardPayload, DecisionsDomainPayload } from "@/types";

export function DecisionDetailPage({ data }: { data: DashboardBootstrapPayload | DashboardPayload }) {
  const { decisionId } = useParams();
  const embeddedDomain = useMemo(
    () => ("items" in data.decisions ? (data.decisions as DecisionsDomainPayload) : null),
    [data.decisions],
  );
  const { data: domain, error } = useDomainPayload(embeddedDomain, loadDecisionsDomain);
  const detail = decisionId ? domain?.details?.[decisionId] : undefined;

  if (!decisionId) {
    return <Navigate to="/decisions" replace />;
  }

  if (!detail && !domain && !error) {
    return (
      <SectionCard title="Loading Decision" kicker="Decision Workspace">
        <p className="text-sm leading-6 text-ink/70">Reading the latest published decision workspace.</p>
      </SectionCard>
    );
  }

  if (!detail) {
    return (
      <SectionCard title="Decision Not Found" kicker="Decision Workspace">
        <p className="text-sm leading-6 text-ink/70">
          {error ?? "No decision detail workspace was found for this link."}
        </p>
        <Link to="/decisions" className="mt-4 inline-flex text-sm font-semibold text-accent">
          Back to decisions
        </Link>
      </SectionCard>
    );
  }

  return (
    <div className="space-y-6">
      <SectionCard
        title={detail.title}
        kicker="Decision Workspace"
        action={<Link to="/decisions" className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Back to decisions</Link>}
      >
        <div className="space-y-4 text-sm leading-6 text-ink/80">
          <div className="flex flex-wrap gap-3">
            <StatusPill value={detail.current_status} />
            <StatusPill value={detail.evidence_confidence} />
          </div>
          <p><span className="font-semibold text-ink">Rationale:</span> {detail.rationale}</p>
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <Metric label="Owner" value={detail.owner} />
            <Metric label="Decision Date" value={detail.decision_date} />
            <Metric label="Importance" value={String(detail.importance)} />
            <Metric label="Source" value={detail.source_path} />
          </div>
        </div>
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-[1.15fr_1fr]">
        <SectionCard title="Related Entities" kicker="Canonical Relationships">
          <div className="grid gap-6 xl:grid-cols-2">
            <LinkedSection title="Projects" items={detail.related_projects} />
            <LinkedSection title="Objectives" items={detail.related_objectives} />
            <LinkedSection title="People" items={detail.related_people} />
            <LinkedSection title="Companies" items={detail.related_companies} />
            <LinkedSection title="Meetings" items={detail.relevant_meetings} />
          </div>
        </SectionCard>

        <SectionCard title="Management Attention" kicker="Current State">
          <ListSection title="Missing Information" items={detail.missing_information} />
          <ListSection title="Recent Changes" items={detail.recent_changes} />
        </SectionCard>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_1fr]">
        <SectionCard title="Evidence" kicker="Source Notes">
          <ul className="space-y-3 text-sm leading-6 text-ink/80">
            {detail.evidence_sources.map((item) => (
              <li key={item.path} className="rounded-2xl border border-ink/10 bg-paper p-4">
                <p className="font-semibold text-ink">{item.label}</p>
                <p>{item.path}</p>
                <p className="text-xs text-ink/60">{item.reason}</p>
              </li>
            ))}
          </ul>
        </SectionCard>

        <SectionCard title="Related Work" kicker="Dependencies">
          <ul className="space-y-3 text-sm leading-6 text-ink/80">
            {detail.related_work_items.length ? detail.related_work_items.map((item) => (
              <li key={item.work_item_id} className="rounded-2xl border border-ink/10 bg-paper p-4">
                <p className="font-semibold text-ink">{item.title}</p>
                <p>{item.reason}</p>
                <p className="text-xs text-ink/60">{item.path}</p>
              </li>
            )) : (
              <li className="rounded-2xl border border-ink/10 bg-paper p-4">No evidence found.</li>
            )}
          </ul>
        </SectionCard>
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-paper p-4">
      <p className="text-xs uppercase tracking-[0.2em] text-accent">{label}</p>
      <p className="mt-2 text-sm font-semibold leading-6 text-ink">{value}</p>
    </div>
  );
}

function LinkedSection({ title, items }: { title: string; items: Array<{ title: string; path: string; reason: string; route: string }> }) {
  return (
    <div className="rounded-3xl bg-white/70 p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      <ul className="mt-3 space-y-2 text-sm leading-6 text-ink/80">
        {items.length ? items.map((item) => (
          <li key={`${title}-${item.title}-${item.path}`} className="rounded-2xl border border-ink/10 bg-paper p-3">
            <p className="font-semibold text-ink">{item.title}</p>
            <p>{item.reason}</p>
            <p className="text-xs text-ink/60">{item.path}</p>
          </li>
        )) : <li>No evidence found.</li>}
      </ul>
    </div>
  );
}

function ListSection({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-2xl bg-white/70 p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      <ul className="mt-3 space-y-2 text-sm leading-6 text-ink/80">
        {items.length ? items.map((item) => <li key={item}>- {item}</li>) : <li>No evidence found.</li>}
      </ul>
    </div>
  );
}
