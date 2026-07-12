import { useEffect, useMemo, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import { loadObjectivesDomain } from "@/lib/loadDashboard";
import { postObjectiveAction } from "@/lib/objectiveApi";
import { useDomainPayload } from "@/lib/useDomainPayload";
import type {
  DashboardBootstrapPayload,
  DashboardPayload,
  LinkedObjectiveItem,
  ObjectiveDetail,
  ObjectivesDomainPayload,
  SmartAssessmentDimension,
} from "@/types";

type Props = {
  data: DashboardBootstrapPayload | DashboardPayload;
  onRefresh: () => Promise<void>;
};

type FormState = {
  owner: string;
  delegates: string;
  contributors: string;
  current_status: string;
  rag_rating: string;
  progress_assessment: string;
  progress_percentage: string;
  priority: string;
  start_date: string;
  target_date: string;
  last_review_date: string;
  next_review_date: string;
  success_measures: string;
  resources: string;
  dependencies: string;
  supporting_evidence: string;
};

const EMPTY_FORM: FormState = {
  owner: "",
  delegates: "",
  contributors: "",
  current_status: "",
  rag_rating: "",
  progress_assessment: "",
  progress_percentage: "",
  priority: "",
  start_date: "",
  target_date: "",
  last_review_date: "",
  next_review_date: "",
  success_measures: "",
  resources: "",
  dependencies: "",
  supporting_evidence: "",
};

export function ObjectiveDetailPage({ data, onRefresh }: Props) {
  const { objectiveId } = useParams();
  const embeddedDomain = useMemo(
    () => ("items" in data.objectives ? (data.objectives as ObjectivesDomainPayload) : null),
    [data.objectives],
  );
  const { data: domain, error: domainError, setData: setDomain } = useDomainPayload(embeddedDomain, loadObjectivesDomain);
  const detail = objectiveId ? domain?.details?.[objectiveId] : undefined;
  const [form, setForm] = useState<FormState>(EMPTY_FORM);
  const [noteText, setNoteText] = useState("");
  const [milestoneTitle, setMilestoneTitle] = useState("");
  const [milestoneDueDate, setMilestoneDueDate] = useState("");
  const [selectedProposalFields, setSelectedProposalFields] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!detail) {
      return;
    }
    setForm({
      owner: normaliseField(detail.owner),
      delegates: detail.delegates.join(", "),
      contributors: detail.contributors.join(", "),
      current_status: normaliseField(detail.current_status),
      rag_rating: normaliseField(detail.rag_rating),
      progress_assessment: normaliseField(detail.progress_assessment),
      progress_percentage: detail.progress_percentage == null ? "" : String(detail.progress_percentage),
      priority: normaliseField(detail.priority),
      start_date: normaliseField(detail.start_date),
      target_date: normaliseField(detail.target_date),
      last_review_date: normaliseField(detail.last_review_date),
      next_review_date: normaliseField(detail.next_review_date),
      success_measures: detail.success_measures.join("\n"),
      resources: detail.resources.join("\n"),
      dependencies: detail.dependencies.join("\n"),
      supporting_evidence: detail.evidence_sources.map((item) => item.path).join("\n"),
    });
    setSelectedProposalFields(Object.keys(detail.smart_enrichment_proposal?.field_proposals ?? {}));
  }, [detail]);

  const proposalFields = useMemo(
    () => Object.entries(detail?.smart_enrichment_proposal?.field_proposals ?? {}),
    [detail],
  );

  if (!objectiveId) {
    return <Navigate to="/objectives" replace />;
  }

  if (!detail && !domain && !domainError) {
    return (
      <SectionCard title="Loading Objective" kicker="Objective Workspace">
        <p className="text-sm leading-6 text-ink/70">Reading the latest published objective workspace.</p>
      </SectionCard>
    );
  }

  if (!detail) {
    return (
      <SectionCard title="Objective Not Found" kicker="Objective Workspace">
        <p className="text-sm leading-6 text-ink/70">
          {domainError ?? "No objective management workspace was found for this link."}
        </p>
        <Link to="/objectives" className="mt-4 inline-flex text-sm font-semibold text-accent">
          Back to objectives
        </Link>
      </SectionCard>
    );
  }

  async function runAction(payload: Record<string, unknown>) {
    setBusy(true);
    setError(null);
    try {
      await postObjectiveAction(objectiveId, payload);
      await onRefresh();
      setDomain(await loadObjectivesDomain());
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Objective action failed.");
    } finally {
      setBusy(false);
    }
  }

  const saveFields = async () => {
    await runAction({
      action: "update_fields",
      reason: "Objective management fields updated from the workspace.",
      changes: {
        owner: emptyToNull(form.owner),
        delegates: parseList(form.delegates),
        contributors: parseList(form.contributors),
        current_status: emptyToNull(form.current_status),
        rag_rating: emptyToNull(form.rag_rating),
        progress_assessment: emptyToNull(form.progress_assessment),
        progress_percentage: form.progress_percentage === "" ? null : Number(form.progress_percentage),
        priority: emptyToNull(form.priority),
        start_date: emptyToNull(form.start_date),
        target_date: emptyToNull(form.target_date),
        last_review_date: emptyToNull(form.last_review_date),
        next_review_date: emptyToNull(form.next_review_date),
        success_measures: parseLines(form.success_measures),
        resources: parseLines(form.resources),
        dependencies: parseLines(form.dependencies),
        evidence_sources: parseLines(form.supporting_evidence).map((path) => ({
          label: path.split("/").at(-1) ?? path,
          path,
          reason: "User-linked supporting evidence.",
        })),
      },
    });
  };

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
            <StatusPill value={detail.priority} />
            {detail.stale_evidence ? <StatusPill value="Stale" /> : null}
          </div>
          <p><span className="font-semibold text-ink">Executive Definition:</span> {detail.executive_definition}</p>
          <p><span className="font-semibold text-ink">Recommended Next Action:</span> {detail.recommended_next_action}</p>
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <Metric label="Owner" value={detail.owner} />
            <Metric label="Progress" value={detail.progress_percentage != null ? `${detail.progress_percentage}%` : detail.progress_assessment} />
            <Metric label="Last Activity" value={detail.last_meaningful_activity} />
            <Metric label="Next Checkpoint" value={detail.next_checkpoint_or_deadline} />
            <Metric label="Start Date" value={detail.start_date} />
            <Metric label="Target Date" value={detail.target_date} />
            <Metric label="Last Review" value={detail.last_review_date} />
            <Metric label="Next Review" value={detail.next_review_date} />
          </div>
          {error ? <p className="text-sm text-red-700">{error}</p> : null}
        </div>
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_1fr]">
        <SectionCard title="Management Data" kicker="Persistent">
          <div className="grid gap-4 md:grid-cols-2">
            <Field label="Accountable Owner" value={form.owner} onChange={(value) => setForm((current) => ({ ...current, owner: value }))} />
            <Field label="Delegates" value={form.delegates} onChange={(value) => setForm((current) => ({ ...current, delegates: value }))} placeholder="Comma separated" />
            <Field label="Contributors" value={form.contributors} onChange={(value) => setForm((current) => ({ ...current, contributors: value }))} placeholder="Comma separated" />
            <SelectField label="Status" value={form.current_status} onChange={(value) => setForm((current) => ({ ...current, current_status: value }))} options={["SUPPORTED", "WATCH", "AT RISK", "HOLD", "CLOSED"]} />
            <SelectField label="RAG Rating" value={form.rag_rating} onChange={(value) => setForm((current) => ({ ...current, rag_rating: value }))} options={["GREEN", "AMBER", "RED"]} />
            <SelectField label="Priority" value={form.priority} onChange={(value) => setForm((current) => ({ ...current, priority: value }))} options={["HIGH", "MEDIUM", "LOW"]} />
            <Field label="Progress %" value={form.progress_percentage} onChange={(value) => setForm((current) => ({ ...current, progress_percentage: value }))} />
            <Field label="Progress Assessment" value={form.progress_assessment} onChange={(value) => setForm((current) => ({ ...current, progress_assessment: value }))} />
            <Field label="Start Date" type="date" value={form.start_date} onChange={(value) => setForm((current) => ({ ...current, start_date: value }))} />
            <Field label="Target Date" type="date" value={form.target_date} onChange={(value) => setForm((current) => ({ ...current, target_date: value }))} />
            <Field label="Last Review Date" type="date" value={form.last_review_date} onChange={(value) => setForm((current) => ({ ...current, last_review_date: value }))} />
            <Field label="Next Review Date" type="date" value={form.next_review_date} onChange={(value) => setForm((current) => ({ ...current, next_review_date: value }))} />
          </div>
          <div className="mt-4 grid gap-4 xl:grid-cols-3">
            <TextAreaField label="Success Measures" value={form.success_measures} onChange={(value) => setForm((current) => ({ ...current, success_measures: value }))} />
            <TextAreaField label="Resources" value={form.resources} onChange={(value) => setForm((current) => ({ ...current, resources: value }))} />
            <TextAreaField label="Dependencies" value={form.dependencies} onChange={(value) => setForm((current) => ({ ...current, dependencies: value }))} />
            <TextAreaField label="Supporting Evidence Paths" value={form.supporting_evidence} onChange={(value) => setForm((current) => ({ ...current, supporting_evidence: value }))} />
          </div>
          <div className="mt-4 flex flex-wrap gap-3">
            <ActionButton label="Save Management Data" busy={busy} onClick={saveFields} />
            <ActionButton label="Hold Objective" busy={busy} onClick={() => runAction({ action: "hold_objective", reason: "Objective placed on hold from workspace." })} />
            <ActionButton label="Close Objective" busy={busy} onClick={() => runAction({ action: "close_objective", reason: "Objective closed from workspace." })} />
            <ActionButton label="Reopen Objective" busy={busy} onClick={() => runAction({ action: "reopen_objective", reason: "Objective reopened from workspace." })} />
            <ActionButton label="Schedule Review" busy={busy} onClick={() => runAction({ action: "update_fields", changes: { next_review_date: nextReviewDate() }, reason: "Review scheduled from objective workspace." })} />
          </div>
        </SectionCard>

        <SectionCard title="SMART Assessment" kicker="Quality">
          <div className="space-y-4">
            {Object.entries(detail.smart_assessment).map(([dimension, value]) => (
              <SmartCard key={dimension} dimension={dimension} value={value} />
            ))}
          </div>
          <div className="mt-5 rounded-3xl bg-white/70 p-4 text-sm leading-6 text-ink/80">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">On-demand SMART Enrichment</p>
              <ActionButton label="Run SMART Enrichment" busy={busy} onClick={() => runAction({ action: "run_smart_enrichment", reason: "SMART refinement requested from workspace." })} />
            </div>
            <ul className="mt-3 space-y-2">
              {detail.proposed_smart_refinement.map((item) => (
                <li key={item}>- {item}</li>
              ))}
            </ul>
            {detail.smart_enrichment_proposal ? (
              <div className="mt-4 rounded-2xl border border-ink/10 bg-paper p-4">
                <p className="font-semibold text-ink">Proposal status: {detail.smart_enrichment_proposal.status}</p>
                <p className="text-xs text-ink/60">Created {detail.smart_enrichment_proposal.created_at}</p>
                {proposalFields.length ? (
                  <div className="mt-3 space-y-2">
                    {proposalFields.map(([field, value]) => (
                      <label key={field} className="flex items-start gap-3 text-sm text-ink/80">
                        <input
                          type="checkbox"
                          checked={selectedProposalFields.includes(field)}
                          onChange={() => setSelectedProposalFields((current) => current.includes(field) ? current.filter((item) => item !== field) : [...current, field])}
                        />
                        <span><span className="font-semibold text-ink">{field}</span>: {renderUnknown(value)}</span>
                      </label>
                    ))}
                  </div>
                ) : (
                  <p className="mt-3 text-sm text-ink/70">No structured field proposals were supported by the evidence.</p>
                )}
                <div className="mt-4 flex flex-wrap gap-3">
                  <ActionButton label="Accept Selected Fields" busy={busy} onClick={() => runAction({ action: "accept_smart_proposal", fields: selectedProposalFields, reason: "Accepted selected SMART proposal fields." })} />
                  <ActionButton label="Reject Proposal" busy={busy} onClick={() => runAction({ action: "reject_smart_proposal", reason: "Rejected SMART proposal from workspace." })} />
                </div>
              </div>
            ) : null}
          </div>
        </SectionCard>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <SectionCard title="Management Links" kicker="Connected Work">
          <div className="space-y-5 text-sm leading-6 text-ink/80">
            <RelationshipManager title="Supporting Projects" field="supporting_projects" items={detail.supporting_projects} options={detail.relationship_options.supporting_projects ?? []} onAction={runAction} />
            <RelationshipManager title="Linked Decisions" field="linked_decisions" items={detail.linked_decisions} options={detail.relationship_options.linked_decisions ?? []} onAction={runAction} />
            <RelationshipManager title="Open Loops" field="open_loops" items={detail.open_loops} options={detail.relationship_options.open_loops ?? []} onAction={runAction} />
            <RelationshipManager title="Follow-ups" field="follow_ups" items={detail.follow_ups} options={detail.relationship_options.follow_ups ?? []} onAction={runAction} />
            <RelationshipManager title="Relevant Meetings" field="relevant_meetings" items={detail.relevant_meetings} options={detail.relationship_options.relevant_meetings ?? []} onAction={runAction} />
            <RelationshipManager title="Related People" field="related_people" items={detail.related_people} options={detail.relationship_options.related_people ?? []} onAction={runAction} />
          </div>
        </SectionCard>

        <SectionCard title="Execution and Evidence" kicker="Workflow">
          <div className="space-y-5 text-sm leading-6 text-ink/80">
            <WorkItemList title="Open Actions" items={detail.open_actions} empty="No evidence found." />
            <EvidenceList title="Evidence Sources" items={detail.evidence_sources} />
            <BulletList title="Recent Changes" items={detail.recent_changes} />
            <BulletList title="Missing Information Requiring Attention" items={detail.missing_information} />
            <MilestoneManager
              items={detail.milestones}
              milestoneTitle={milestoneTitle}
              milestoneDueDate={milestoneDueDate}
              setMilestoneTitle={setMilestoneTitle}
              setMilestoneDueDate={setMilestoneDueDate}
              onAdd={() => runAction({ action: "add_milestone", title: milestoneTitle, due_date: milestoneDueDate || null, reason: "Milestone added from objective workspace." }).then(() => { setMilestoneTitle(""); setMilestoneDueDate(""); })}
              onComplete={(milestoneId) => runAction({ action: "complete_milestone", milestone_id: milestoneId, reason: "Milestone marked complete from objective workspace." })}
              busy={busy}
            />
            <ManagementNotes
              notes={detail.management_notes}
              noteText={noteText}
              setNoteText={setNoteText}
              onAdd={() => runAction({ action: "add_management_note", text: noteText, reason: "Management note recorded from objective workspace." }).then(() => setNoteText(""))}
              busy={busy}
            />
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Audit History" kicker="Governance">
        {detail.audit_history.length ? (
          <ul className="space-y-3 text-sm leading-6 text-ink/80">
            {detail.audit_history.map((item) => (
              <li key={item.audit_id} className="rounded-2xl bg-white/70 p-4">
                <p className="font-semibold text-ink">{item.action} · {item.field}</p>
                <p>{item.timestamp} · {item.source}</p>
                <p><span className="font-semibold text-ink">Previous:</span> {renderUnknown(item.previous_value)}</p>
                <p><span className="font-semibold text-ink">New:</span> {renderUnknown(item.new_value)}</p>
                <p><span className="font-semibold text-ink">Reason:</span> {item.reason}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm leading-6 text-ink/70">No audit history has been recorded yet.</p>
        )}
      </SectionCard>
    </div>
  );
}

function RelationshipManager({
  title,
  field,
  items,
  options,
  onAction,
}: {
  title: string;
  field: string;
  items: Array<LinkedObjectiveItem & { type?: string }>;
  options: LinkedObjectiveItem[];
  onAction: (payload: Record<string, unknown>) => Promise<void>;
}) {
  const [selected, setSelected] = useState("");

  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      {items.length ? (
        <ul className="mt-3 space-y-3">
          {items.map((item) => (
            <li key={`${title}-${item.id ?? item.work_item_id ?? item.path}-${item.title}`} className="rounded-2xl bg-white/70 p-3">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="font-semibold text-ink">{item.title}</p>
                  <p>{item.reason}</p>
                  {item.path ? <p className="text-xs text-ink/60">{item.path}</p> : null}
                </div>
                <div className="flex gap-3">
                  <Link to={item.route} className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Open</Link>
                  <button
                    type="button"
                    className="text-xs font-semibold uppercase tracking-[0.2em] text-red-700"
                    onClick={() => onAction({ action: "unlink_item", field, item_key: item.id ?? item.work_item_id ?? item.path ?? item.title, current_items: items, reason: `Removed ${title.toLowerCase()} relationship.` })}
                  >
                    Remove
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3">No evidence found.</p>
      )}
      <div className="mt-3 flex flex-wrap gap-3">
        <select value={selected} onChange={(event) => setSelected(event.target.value)} className="min-w-72 rounded-2xl border border-ink/10 bg-white/90 px-3 py-2 text-sm text-ink">
          <option value="">Select {title.toLowerCase()}</option>
          {options.map((item) => (
            <option key={item.id ?? item.path ?? item.title} value={item.id ?? item.work_item_id ?? item.path ?? item.title}>
              {item.title}
            </option>
          ))}
        </select>
        <button
          type="button"
          className="rounded-full bg-ink px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-paper"
          onClick={() => {
            const item = options.find((candidate) => (candidate.id ?? candidate.work_item_id ?? candidate.path ?? candidate.title) === selected);
            if (!item) {
              return;
            }
            onAction({ action: "link_item", field, item, current_items: items, reason: `Linked ${item.title} to objective.` }).then(() => setSelected(""));
          }}
        >
          Link
        </button>
      </div>
    </div>
  );
}

function MilestoneManager({
  items,
  milestoneTitle,
  milestoneDueDate,
  setMilestoneTitle,
  setMilestoneDueDate,
  onAdd,
  onComplete,
  busy,
}: {
  items: ObjectiveDetail["milestones"];
  milestoneTitle: string;
  milestoneDueDate: string;
  setMilestoneTitle: (value: string) => void;
  setMilestoneDueDate: (value: string) => void;
  onAdd: () => Promise<void>;
  onComplete: (milestoneId: string) => Promise<void>;
  busy: boolean;
}) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Milestones</p>
      {items.length ? (
        <ul className="mt-3 space-y-3">
          {items.map((item) => (
            <li key={item.milestone_id} className="rounded-2xl bg-white/70 p-3">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="font-semibold text-ink">{item.title}</p>
                  <p>Due {item.due_date} · {item.status}</p>
                </div>
                {item.status !== "COMPLETED" ? (
                  <button type="button" className="text-xs font-semibold uppercase tracking-[0.2em] text-accent" onClick={() => onComplete(item.milestone_id)}>
                    Mark Complete
                  </button>
                ) : null}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3">No milestones have been defined.</p>
      )}
      <div className="mt-3 grid gap-3 md:grid-cols-[1.4fr_1fr_auto]">
        <Field label="New Milestone" value={milestoneTitle} onChange={setMilestoneTitle} />
        <Field label="Due Date" type="date" value={milestoneDueDate} onChange={setMilestoneDueDate} />
        <div className="flex items-end">
          <ActionButton label="Add Milestone" busy={busy} onClick={onAdd} />
        </div>
      </div>
    </div>
  );
}

function ManagementNotes({
  notes,
  noteText,
  setNoteText,
  onAdd,
  busy,
}: {
  notes: ObjectiveDetail["management_notes"];
  noteText: string;
  setNoteText: (value: string) => void;
  onAdd: () => Promise<void>;
  busy: boolean;
}) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Management Notes</p>
      {notes.length ? (
        <ul className="mt-3 space-y-3">
          {notes.map((item) => (
            <li key={item.note_id} className="rounded-2xl bg-white/70 p-3">
              <p className="font-semibold text-ink">{item.timestamp}</p>
              <p>{item.text}</p>
              <p className="text-xs text-ink/60">{item.source} · {item.reason}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3">No management notes recorded.</p>
      )}
      <div className="mt-3 flex flex-col gap-3">
        <TextAreaField label="Add Management Note" value={noteText} onChange={setNoteText} rows={3} />
        <div>
          <ActionButton label="Add Note" busy={busy} onClick={onAdd} />
        </div>
      </div>
    </div>
  );
}

function ActionButton({ label, onClick, busy }: { label: string; onClick: () => Promise<void> | void; busy: boolean }) {
  return (
    <button
      type="button"
      disabled={busy}
      className="rounded-full bg-ink px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-paper disabled:opacity-60"
      onClick={() => void onClick()}
    >
      {label}
    </button>
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

function Field({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  placeholder?: string;
}) {
  return (
    <label className="block">
      <span className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">{label}</span>
      <input
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-2xl border border-ink/10 bg-white/90 px-3 py-2 text-sm text-ink"
      />
    </label>
  );
}

function TextAreaField({
  label,
  value,
  onChange,
  rows = 5,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  rows?: number;
}) {
  return (
    <label className="block">
      <span className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">{label}</span>
      <textarea
        value={value}
        rows={rows}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-2xl border border-ink/10 bg-white/90 px-3 py-2 text-sm text-ink"
      />
    </label>
  );
}

function SelectField({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: string[];
}) {
  return (
    <label className="block">
      <span className="text-[11px] font-semibold uppercase tracking-[0.2em] text-accent">{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-2xl border border-ink/10 bg-white/90 px-3 py-2 text-sm text-ink"
      >
        <option value="">Not defined</option>
        {options.map((option) => (
          <option key={option} value={option}>{option}</option>
        ))}
      </select>
    </label>
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

function normaliseField(value: string) {
  return value === "Not defined" ? "" : value;
}

function emptyToNull(value: string) {
  const trimmed = value.trim();
  return trimmed === "" ? null : trimmed;
}

function parseList(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function parseLines(value: string) {
  return value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

function renderUnknown(value: unknown): string {
  if (value == null) {
    return "Not defined";
  }
  if (Array.isArray(value)) {
    return value.length ? value.map(renderUnknown).join(", ") : "Not defined";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}

function nextReviewDate() {
  const next = new Date();
  next.setDate(next.getDate() + 30);
  return next.toISOString().slice(0, 10);
}
