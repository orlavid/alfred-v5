import { useState } from "react";
import { Link } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import { postMatterAction } from "@/lib/matterApi";
import { postObjectiveAction } from "@/lib/objectiveApi";
import { postProjectAction } from "@/lib/projectApi";
import type { DashboardBootstrapPayload, ExecutiveMatter } from "@/types";

export function DashboardPage({
  data,
  onRefresh,
}: {
  data: DashboardBootstrapPayload;
  onRefresh: () => Promise<void>;
}) {
  const [busyMatterId, setBusyMatterId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function runMatterAction(matter: ExecutiveMatter, payload: Record<string, unknown>) {
    if (!matter.route.startsWith("/matters/")) {
      return;
    }
    const matterId = matter.route.split("/").at(-1);
    if (!matterId) {
      return;
    }
    setBusyMatterId(matterId);
    setError(null);
    try {
      if (matter.action_target.kind === "objective") {
        await postObjectiveAction(matter.action_target.id, mapMatterActionToWorkspacePayload("objective", payload));
      } else if (matter.action_target.kind === "project") {
        await postProjectAction(matter.action_target.id, mapMatterActionToWorkspacePayload("project", payload));
      } else {
        await postMatterAction(matterId, payload);
      }
      await onRefresh();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Matter action failed.");
    } finally {
      setBusyMatterId(null);
    }
  }

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-white/70 bg-ink p-8 text-white shadow-panel">
        <p className="text-xs uppercase tracking-[0.3em] text-white/60">Executive Home</p>
        <div className="mt-4 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-4xl">
            <h2 className="font-serif text-4xl">{data.executive_home.headline}</h2>
            <div className="mt-4 space-y-2 text-lg text-white/75">
              {data.executive_home.summary_lines.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </div>
          </div>
          <Link to={data.executive_home.system_health_route} className="rounded-3xl bg-white/10 p-5 transition hover:bg-white/15">
            <p className="text-xs uppercase tracking-[0.24em] text-white/60">System Health</p>
            <p className="mt-3 text-sm font-medium text-white">{data.system_health.refresh_status.overall_health}</p>
          </Link>
        </div>
      </section>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {data.executive_home.kpis.map((item) => (
          <Link
            key={item.card_id}
            to={item.route}
            className="rounded-3xl border border-ink/10 bg-white/80 p-5 shadow-panel transition hover:-translate-y-0.5 hover:border-accent/30"
          >
            <p className="text-xs uppercase tracking-[0.22em] text-accent">{item.label}</p>
            <p className="mt-3 font-serif text-4xl text-ink">{item.count}</p>
            <p className="mt-3 text-sm leading-6 text-ink/75">{item.summary}</p>
          </Link>
        ))}
      </div>

      {error ? (
        <SectionCard title="Landing Action Failed" kicker="Error">
          <p className="text-sm leading-6 text-red-700">{error}</p>
        </SectionCard>
      ) : null}

      {data.executive_home.sections.map((section) => (
        <SectionCard key={section.section_id} title={section.title} kicker="Executive Engagement">
          <p className="mb-4 text-sm leading-6 text-ink/75">{section.summary}</p>
          <div className="space-y-4">
            {section.matters.map((matter) => (
              <article key={matter.matter_id} className="rounded-3xl border border-ink/10 bg-white/80 p-5 shadow-panel">
                <div className="flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
                  <div className="space-y-3">
                    <div className="flex flex-wrap gap-2">
                      <StatusPill value={matter.matter_category.replaceAll("_", " ")} />
                      <StatusPill value={matter.status} />
                      <StatusPill value={matter.priority} />
                      <StatusPill value={matter.confidence} />
                    </div>
                    <Link to={matter.route} className="block">
                      <h3 className="font-serif text-2xl text-ink hover:text-accent">{matter.business_title}</h3>
                    </Link>
                    <p className="text-sm leading-6 text-ink/80">{matter.human_summary}</p>
                    <div className="grid gap-3 md:grid-cols-2">
                      <SummaryBlock label="Why It Matters" value={matter.why_it_matters} />
                      <SummaryBlock label="Why Now" value={matter.why_now} />
                      <SummaryBlock label="Evidence Summary" value={matter.evidence_summary} />
                      <SummaryBlock label="Recommended Next Step" value={matter.recommended_next_step} />
                    </div>
                  </div>
                  <div className="xl:w-[21rem]">
                    <div className="rounded-2xl bg-paper p-4 text-sm leading-6 text-ink/80">
                      <p><span className="font-semibold text-ink">Owner:</span> {matter.owner}</p>
                      <p><span className="font-semibold text-ink">Objective:</span> {matter.related.objective || "Not defined"}</p>
                      <p><span className="font-semibold text-ink">Projects:</span> {matter.related.projects.join(", ") || "Not defined"}</p>
                      <p><span className="font-semibold text-ink">People:</span> {matter.related.people.join(", ") || "Not defined"}</p>
                      <p><span className="font-semibold text-ink">Companies:</span> {matter.related.companies.join(", ") || "Not defined"}</p>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      <Link to={matter.route} className="inline-flex rounded-full border border-accent/30 px-4 py-2 text-sm font-semibold text-accent">
                        Open detail
                      </Link>
                      {matter.available_actions.some((item) => item.action === "assign_owner") ? (
                        <ActionButton
                          label="Assign owner"
                          busy={busyMatterId === matter.matter_id}
                          onClick={() => {
                            const owner = window.prompt("Assign owner", matter.owner === "Unassigned" ? "" : matter.owner);
                            if (owner !== null) {
                              void runMatterAction(matter, { action: "set_owner", owner: owner || "Unassigned", reason: "Owner updated from executive home." });
                            }
                          }}
                        />
                      ) : null}
                      {matter.available_actions.some((item) => item.action === "change_priority") ? (
                        <ActionButton
                          label="Change priority"
                          busy={busyMatterId === matter.matter_id}
                          onClick={() => {
                            const priority = window.prompt("Set priority", matter.priority);
                            if (priority !== null) {
                              void runMatterAction(matter, { action: "set_priority", priority: priority || "MEDIUM", reason: "Priority updated from executive home." });
                            }
                          }}
                        />
                      ) : null}
                      {matter.available_actions.some((item) => item.action === "hold") ? (
                        <ActionButton label="Hold" busy={busyMatterId === matter.matter_id} onClick={() => void runMatterAction(matter, { action: "hold_matter", reason: "Matter placed on hold from executive home." })} />
                      ) : null}
                      {matter.available_actions.some((item) => item.action === "resolve") ? (
                        <ActionButton label="Resolve" busy={busyMatterId === matter.matter_id} onClick={() => void runMatterAction(matter, { action: "resolve_matter", reason: "Matter resolved from executive home." })} />
                      ) : null}
                      {matter.available_actions.some((item) => item.action === "dismiss") ? (
                        <ActionButton label="Dismiss" busy={busyMatterId === matter.matter_id} onClick={() => void runMatterAction(matter, { action: "dismiss_matter", reason: "Matter dismissed from executive home." })} />
                      ) : null}
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </SectionCard>
      ))}
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

function SummaryBlock({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-paper p-4 text-sm leading-6 text-ink/80">
      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">{label}</p>
      <p className="mt-2">{value}</p>
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
