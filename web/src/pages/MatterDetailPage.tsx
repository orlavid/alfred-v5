import { useEffect, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import { loadMatterDetail } from "@/lib/loadDashboard";
import { postMatterAction } from "@/lib/matterApi";
import { postObjectiveAction } from "@/lib/objectiveApi";
import { postProjectAction } from "@/lib/projectApi";
import type { DashboardBootstrapPayload, ExecutiveMatterDetail } from "@/types";

export function MatterDetailPage({
  data,
  onRefresh,
}: {
  data: DashboardBootstrapPayload;
  onRefresh: () => Promise<void>;
}) {
  const { matterId } = useParams();
  const [detail, setDetail] = useState<ExecutiveMatterDetail | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!matterId) {
      return;
    }
    let cancelled = false;
    loadMatterDetail(matterId)
      .then((payload) => {
        if (!cancelled) {
          setDetail(payload);
          setError(null);
        }
      })
      .catch((reason: Error) => {
        if (!cancelled) {
          setError(reason.message);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [matterId]);

  if (!matterId) {
    return <Navigate to="/" replace />;
  }

  if (!detail) {
    return (
      <SectionCard title="Matter Workspace" kicker="Executive Home">
        <p className="text-sm leading-6 text-ink/70">{error ?? "Loading the matter workspace."}</p>
        <Link to="/" className="mt-4 inline-flex text-sm font-semibold text-accent">Back to executive home</Link>
      </SectionCard>
    );
  }

  async function runAction(payload: Record<string, unknown>) {
    setBusy(true);
    setError(null);
    try {
      if (detail.action_target.kind === "objective") {
        await postObjectiveAction(detail.action_target.id, mapMatterActionToWorkspacePayload("objective", payload));
      } else if (detail.action_target.kind === "project") {
        await postProjectAction(detail.action_target.id, mapMatterActionToWorkspacePayload("project", payload));
      } else {
        await postMatterAction(matterId, payload);
      }
      await onRefresh();
      setDetail(await loadMatterDetail(matterId));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Matter action failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-6">
      <SectionCard
        title={detail.business_title}
        kicker="Matter Workspace"
        action={<Link to="/" className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Back to executive home</Link>}
      >
        <div className="space-y-4 text-sm leading-6 text-ink/80">
          <div className="flex flex-wrap gap-3">
            <StatusPill value={detail.matter_category} />
            <StatusPill value={detail.status} />
            <StatusPill value={detail.priority} />
            <StatusPill value={detail.confidence} />
          </div>
          <p><span className="font-semibold text-ink">Summary:</span> {detail.human_summary}</p>
          <p><span className="font-semibold text-ink">Why It Matters:</span> {detail.why_it_matters}</p>
          <p><span className="font-semibold text-ink">Why Now:</span> {detail.why_now}</p>
          <p><span className="font-semibold text-ink">Evidence Summary:</span> {detail.evidence_summary}</p>
          <p><span className="font-semibold text-ink">Recommended Next Step:</span> {detail.recommended_next_step}</p>
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <Metric label="Owner" value={detail.owner} />
            <Metric label="Objective" value={detail.related.objective || "Not defined"} />
            <Metric label="Recent Activity" value={detail.recent_activity || "Not defined"} />
            <Metric label="Source" value={detail.source_kind.replaceAll("_", " ")} />
          </div>
        </div>
      </SectionCard>

      <SectionCard title="Workflow Actions" kicker="Engage">
        {error ? <p className="mb-3 text-sm leading-6 text-red-700">{error}</p> : null}
        <div className="flex flex-wrap gap-3">
          {detail.available_actions.some((item) => item.action === "assign_owner") ? <ActionButton label="Assign owner" busy={busy} onClick={() => {
            const owner = window.prompt("Assign owner", detail.owner === "Unassigned" ? "" : detail.owner);
            if (owner !== null) {
              void runAction({ action: "set_owner", owner: owner || "Unassigned", reason: "Owner updated from matter workspace." });
            }
          }} /> : null}
          {detail.available_actions.some((item) => item.action === "change_priority") ? <ActionButton label="Change priority" busy={busy} onClick={() => {
            const priority = window.prompt("Set priority", detail.priority);
            if (priority !== null) {
              void runAction({ action: "set_priority", priority: priority || "MEDIUM", reason: "Priority updated from matter workspace." });
            }
          }} /> : null}
          {detail.available_actions.some((item) => item.action === "hold") ? <ActionButton label="Hold" busy={busy} onClick={() => void runAction({ action: "hold_matter", reason: "Matter placed on hold from landing workspace." })} /> : null}
          {detail.available_actions.some((item) => item.action === "resolve") ? <ActionButton label="Resolve" busy={busy} onClick={() => void runAction({ action: "resolve_matter", reason: "Matter resolved from landing workspace." })} /> : null}
          {detail.available_actions.some((item) => item.action === "dismiss") ? <ActionButton label="Dismiss" busy={busy} onClick={() => void runAction({ action: "dismiss_matter", reason: "Matter dismissed from landing workspace." })} /> : null}
          {detail.action_target.kind === "matter" ? <ActionButton label="Reopen" busy={busy} onClick={() => void runAction({ action: "reopen_matter", reason: "Matter reopened from landing workspace." })} /> : null}
          <Link to={detail.authoritative_route} className="inline-flex rounded-full border border-accent/30 px-4 py-2 text-sm font-semibold text-accent">
            {detail.detail_backlink_label}
          </Link>
        </div>
      </SectionCard>

      <SectionCard title="Relationships" kicker="Context">
        <div className="grid gap-4 md:grid-cols-2">
          <RelationshipList title="Projects" items={detail.related.projects} />
          <RelationshipList title="People" items={detail.related.people} />
          <RelationshipList title="Companies" items={detail.related.companies} />
          <RelationshipList title="Missing Information" items={detail.missing_information} />
        </div>
      </SectionCard>

      <SectionCard title="Evidence and Provenance" kicker="Explain">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl bg-white/70 p-4 text-sm leading-6 text-ink/80">
            <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">Evidence</p>
            <ul className="mt-2 space-y-1">
              {detail.evidence_paths.length ? detail.evidence_paths.map((path) => <li key={path}>{path}</li>) : <li>No evidence found.</li>}
            </ul>
          </div>
          <div className="rounded-2xl bg-white/70 p-4 text-sm leading-6 text-ink/80">
            <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">Provenance</p>
            <ul className="mt-2 space-y-1">
              {Object.entries(detail.provenance).length ? Object.entries(detail.provenance).map(([key, paths]) => (
                <li key={key}>
                  <span className="font-semibold text-ink">{key.replaceAll("_", " ")}:</span> {paths.join(", ")}
                </li>
              )) : <li>No provenance recorded.</li>}
            </ul>
          </div>
        </div>
      </SectionCard>

      <SectionCard title="Audit History" kicker="Audit">
        <div className="space-y-3">
          {detail.audit_history.length ? detail.audit_history.map((entry) => (
            <article key={entry.audit_id} className="rounded-2xl bg-white/70 p-4 text-sm leading-6 text-ink/80">
              <p className="font-semibold text-ink">{entry.action}</p>
              <p>{entry.reason}</p>
              <p className="text-xs uppercase tracking-[0.18em] text-accent">{entry.timestamp}</p>
            </article>
          )) : <p className="text-sm leading-6 text-ink/70">No audit history recorded yet.</p>}
        </div>
      </SectionCard>
    </div>
  );
}

function mapMatterActionToWorkspacePayload(kind: "objective" | "project", payload: Record<string, unknown>) {
  if (payload.action === "set_owner") {
    return {
      action: "update_fields",
      reason: payload.reason,
      changes: { owner: payload.owner },
    };
  }
  if (payload.action === "set_priority") {
    return {
      action: "update_fields",
      reason: payload.reason,
      changes: { priority: payload.priority },
    };
  }
  if (payload.action === "hold_matter") {
    return {
      action: kind === "objective" ? "hold_objective" : "hold_project",
      reason: payload.reason,
    };
  }
  if (payload.action === "resolve_matter") {
    return {
      action: kind === "objective" ? "close_objective" : "close_project",
      reason: payload.reason,
    };
  }
  return payload;
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-paper p-4">
      <p className="text-xs uppercase tracking-[0.2em] text-accent">{label}</p>
      <p className="mt-2 text-sm font-semibold text-ink">{value}</p>
    </div>
  );
}

function RelationshipList({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-2xl bg-white/70 p-4 text-sm leading-6 text-ink/80">
      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      <ul className="mt-2 space-y-1">
        {items.length ? items.map((item) => <li key={item}>{item}</li>) : <li>No evidence found.</li>}
      </ul>
    </div>
  );
}

function ActionButton({ label, busy, onClick }: { label: string; busy: boolean; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={busy}
      className="rounded-full border border-ink/10 bg-white px-4 py-2 text-sm font-semibold text-ink transition hover:border-accent/30 disabled:cursor-not-allowed disabled:opacity-60"
    >
      {busy ? "Working..." : label}
    </button>
  );
}
