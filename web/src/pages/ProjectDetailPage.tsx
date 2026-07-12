import { useEffect, useMemo, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import { postProjectAction } from "@/lib/projectApi";
import type { DashboardPayload, LinkedObjectiveItem, ProjectDetail } from "@/types";

type Props = {
  data: DashboardPayload;
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

export function ProjectDetailPage({ data, onRefresh }: Props) {
  const { projectId } = useParams();
  const detail = projectId ? data.projects.details?.[projectId] : undefined;
  const [form, setForm] = useState<FormState>(EMPTY_FORM);
  const [noteText, setNoteText] = useState("");
  const [milestoneTitle, setMilestoneTitle] = useState("");
  const [milestoneDueDate, setMilestoneDueDate] = useState("");
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
  }, [detail]);

  const groupedActions = useMemo(() => {
    if (!detail) {
      return { followups: [], openLoops: [] };
    }
    return {
      followups: detail.follow_ups,
      openLoops: detail.open_loops,
    };
  }, [detail]);

  if (!projectId) {
    return <Navigate to="/projects" replace />;
  }

  if (!detail) {
    return (
      <SectionCard title="Project Not Found" kicker="Project Workspace">
        <p className="text-sm leading-6 text-ink/70">No project management workspace was found for this link.</p>
        <Link to="/projects" className="mt-4 inline-flex text-sm font-semibold text-accent">
          Back to projects
        </Link>
      </SectionCard>
    );
  }

  async function runAction(payload: Record<string, unknown>) {
    setBusy(true);
    setError(null);
    try {
      await postProjectAction(projectId, payload);
      await onRefresh();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Project action failed.");
    } finally {
      setBusy(false);
    }
  }

  const saveFields = async () => {
    await runAction({
      action: "update_fields",
      reason: "Project management fields updated from the workspace.",
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
        kicker="Project Workspace"
        action={<Link to="/projects" className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Back to projects</Link>}
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
            <ActionButton label="Hold Project" busy={busy} onClick={() => runAction({ action: "hold_project", reason: "Project placed on hold from workspace." })} />
            <ActionButton label="Close Project" busy={busy} onClick={() => runAction({ action: "close_project", reason: "Project closed from workspace." })} />
            <ActionButton label="Reopen Project" busy={busy} onClick={() => runAction({ action: "reopen_project", reason: "Project reopened from workspace." })} />
          </div>
        </SectionCard>

        <SectionCard title="Management Attention" kicker="Current State">
          <ListSection title="Missing Information" items={detail.missing_information} />
          <ListSection title="Recent Changes" items={detail.recent_changes} />
          <ListSection title="Risks and Blockers" items={detail.risks_and_blockers.map((item) => `${item.title}: ${item.reason}`)} />
        </SectionCard>
      </div>

      <SectionCard title="Management Links" kicker="Canonical Relationships">
        <div className="grid gap-6 xl:grid-cols-2">
          <RelationshipManager title="Linked Objectives" field="linked_objectives" items={detail.linked_objectives} options={detail.relationship_options.linked_objectives ?? []} onAction={runAction} />
          <RelationshipManager title="Linked Decisions" field="linked_decisions" items={detail.linked_decisions} options={detail.relationship_options.linked_decisions ?? []} onAction={runAction} />
          <RelationshipManager title="Open Loops" field="open_loops" items={detail.open_loops} options={detail.relationship_options.open_loops ?? []} onAction={runAction} />
          <RelationshipManager title="Follow-ups" field="follow_ups" items={detail.follow_ups} options={detail.relationship_options.follow_ups ?? []} onAction={runAction} />
          <RelationshipManager title="Meetings" field="relevant_meetings" items={detail.relevant_meetings} options={detail.relationship_options.relevant_meetings ?? []} onAction={runAction} />
          <RelationshipManager title="Related People" field="related_people" items={detail.related_people} options={detail.relationship_options.related_people ?? []} onAction={runAction} />
          <RelationshipManager title="Related Companies" field="related_companies" items={detail.related_companies} options={detail.relationship_options.related_companies ?? []} onAction={runAction} />
        </div>
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_1fr]">
        <SectionCard title="Execution and Evidence" kicker="Workflow">
          <div className="space-y-6">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Milestones</p>
              <div className="mt-3 grid gap-3 md:grid-cols-[1.4fr_0.8fr_auto]">
                <Field label="Milestone Title" value={milestoneTitle} onChange={setMilestoneTitle} />
                <Field label="Due Date" type="date" value={milestoneDueDate} onChange={setMilestoneDueDate} />
                <div className="flex items-end">
                  <ActionButton label="Add Milestone" busy={busy} onClick={() => runAction({ action: "add_milestone", title: milestoneTitle, due_date: emptyToNull(milestoneDueDate), reason: "Project milestone added from workspace." }).then(() => { setMilestoneTitle(""); setMilestoneDueDate(""); })} />
                </div>
              </div>
              <ul className="mt-4 space-y-3">
                {detail.milestones.map((milestone) => (
                  <li key={milestone.milestone_id} className="rounded-2xl border border-ink/10 bg-paper p-4 text-sm leading-6 text-ink/80">
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div>
                        <p className="font-semibold text-ink">{milestone.title}</p>
                        <p>Due {milestone.due_date}</p>
                      </div>
                      <div className="flex items-center gap-3">
                        <StatusPill value={milestone.status} />
                        {milestone.status !== "COMPLETED" ? (
                          <button
                            type="button"
                            className="text-xs font-semibold uppercase tracking-[0.2em] text-accent"
                            onClick={() => runAction({ action: "complete_milestone", milestone_id: milestone.milestone_id, reason: "Project milestone completed from workspace." })}
                          >
                            Complete
                          </button>
                        ) : null}
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Management Notes</p>
              <TextAreaField label="New Note" value={noteText} onChange={setNoteText} />
              <div className="mt-3">
                <ActionButton label="Add Management Note" busy={busy} onClick={() => runAction({ action: "add_management_note", text: noteText, reason: "Project management note added from workspace." }).then(() => setNoteText(""))} />
              </div>
              <ul className="mt-4 space-y-3">
                {detail.management_notes.map((note) => (
                  <li key={note.note_id} className="rounded-2xl border border-ink/10 bg-paper p-4 text-sm leading-6 text-ink/80">
                    <p className="font-semibold text-ink">{note.timestamp}</p>
                    <p className="mt-1">{note.text}</p>
                    <p className="mt-2 text-xs text-ink/60">{note.reason}</p>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-3xl bg-white/70 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">Evidence Sources</p>
              <ul className="mt-3 space-y-2 text-sm leading-6 text-ink/80">
                {detail.evidence_sources.map((source) => (
                  <li key={source.path}>
                    <p className="font-semibold text-ink">{source.label}</p>
                    <p>{source.path}</p>
                    <p className="text-xs text-ink/60">{source.reason}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Audit History" kicker="Persistence">
          <ul className="space-y-3 text-sm leading-6 text-ink/80">
            {detail.audit_history.length ? detail.audit_history.map((entry) => (
              <li key={entry.audit_id} className="rounded-2xl border border-ink/10 bg-paper p-4">
                <p className="font-semibold text-ink">{entry.action}</p>
                <p>{entry.field}</p>
                <p className="text-xs text-ink/60">{entry.timestamp} · {entry.reason}</p>
              </li>
            )) : <li className="rounded-2xl border border-ink/10 bg-paper p-4">No audit entries yet.</li>}
          </ul>
        </SectionCard>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <SectionCard title="Open Actions" kicker="Current Work">
          <ListSection title="Follow-ups" items={groupedActions.followups.map((item) => `${item.title} (${item.reason})`)} />
          <ListSection title="Open Loops" items={groupedActions.openLoops.map((item) => `${item.title} (${item.reason})`)} />
        </SectionCard>
        <SectionCard title="Supporting Context" kicker="Current Network">
          <ListSection title="Related Companies" items={detail.related_companies.map((item) => `${item.title} (${item.reason})`)} />
          <ListSection title="Relevant Meetings" items={detail.relevant_meetings.map((item) => `${item.title} (${item.reason})`)} />
        </SectionCard>
      </div>
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
  items: Array<LinkedObjectiveItem | { work_item_id: string; title: string; path: string; reason: string; route: string }>;
  options: LinkedObjectiveItem[];
  onAction: (payload: Record<string, unknown>) => Promise<void>;
}) {
  const [selectedId, setSelectedId] = useState("");
  return (
    <div className="rounded-3xl bg-white/70 p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">{title}</p>
      <ul className="mt-3 space-y-2 text-sm leading-6 text-ink/80">
        {items.length ? items.map((item) => {
          const itemKey = "work_item_id" in item ? item.work_item_id : item.id ?? item.path;
          return (
            <li key={itemKey} className="rounded-2xl border border-ink/10 bg-paper p-3">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold text-ink">{item.title}</p>
                  <p>{item.reason}</p>
                  <p className="text-xs text-ink/60">{item.path}</p>
                </div>
                <button
                  type="button"
                  className="text-xs font-semibold uppercase tracking-[0.2em] text-accent"
                  onClick={() => onAction({ action: "unlink_item", field, item_key: itemKey, current_items: items, reason: `Removed ${item.title} from ${title}.` })}
                >
                  Remove
                </button>
              </div>
            </li>
          );
        }) : <li>No evidence found.</li>}
      </ul>
      <div className="mt-4 flex gap-3">
        <select
          className="min-w-0 flex-1 rounded-2xl border border-ink/10 bg-paper px-3 py-2 text-sm text-ink"
          value={selectedId}
          onChange={(event) => setSelectedId(event.target.value)}
        >
          <option value="">Link an item</option>
          {options.map((option) => (
            <option key={option.id} value={option.id}>
              {option.title}
            </option>
          ))}
        </select>
        <button
          type="button"
          className="rounded-full bg-accent px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-white disabled:cursor-not-allowed disabled:opacity-50"
          disabled={!selectedId}
          onClick={() => {
            const option = options.find((item) => item.id === selectedId);
            if (!option) {
              return;
            }
            onAction({ action: "link_item", field, item: option, current_items: items, reason: `Linked ${option.title} to ${title}.` }).then(() => setSelectedId(""));
          }}
        >
          Link
        </button>
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-paper p-4">
      <p className="text-xs uppercase tracking-[0.2em] text-accent">{label}</p>
      <p className="mt-2 text-sm font-semibold leading-6 text-ink">{renderUnknown(value)}</p>
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
    <label className="block text-sm text-ink/80">
      <span className="mb-2 block font-semibold text-ink">{label}</span>
      <input
        className="w-full rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm text-ink"
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
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
    <label className="block text-sm text-ink/80">
      <span className="mb-2 block font-semibold text-ink">{label}</span>
      <select
        className="w-full rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm text-ink"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">Not defined</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

function TextAreaField({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="block text-sm text-ink/80">
      <span className="mb-2 block font-semibold text-ink">{label}</span>
      <textarea
        className="min-h-40 w-full rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm text-ink"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

function ActionButton({ label, busy, onClick }: { label: string; busy: boolean; onClick: () => void }) {
  return (
    <button
      type="button"
      className="rounded-full bg-accent px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-white disabled:cursor-not-allowed disabled:opacity-50"
      disabled={busy}
      onClick={onClick}
    >
      {label}
    </button>
  );
}

function renderUnknown(value: string | null | undefined): string {
  if (!value || value === "Not defined" || value === "No evidence found.") {
    return value ?? "Not defined";
  }
  return value;
}

function normaliseField(value: string | null | undefined): string {
  return value === "Not defined" || value === "No evidence found." ? "" : (value ?? "");
}

function emptyToNull(value: string): string | null {
  return value.trim() ? value.trim() : null;
}

function parseList(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function parseLines(value: string): string[] {
  return value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}
