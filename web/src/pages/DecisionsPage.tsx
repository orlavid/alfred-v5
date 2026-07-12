import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardPayload } from "@/types";

type SortOption = "importance" | "title" | "date";

export function DecisionsPage({ data }: { data: DashboardPayload }) {
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [sortBy, setSortBy] = useState<SortOption>("importance");

  const filteredItems = useMemo(() => {
    const lower = query.trim().toLowerCase();
    const items = data.decisions.items.filter((item) => {
      if (statusFilter !== "ALL" && item.status !== statusFilter) {
        return false;
      }
      if (!lower) {
        return true;
      }
      return [
        item.title,
        item.owner,
        item.rationale,
        item.source_path,
      ].some((value) => value.toLowerCase().includes(lower));
    });

    return items.sort((left, right) => {
      if (sortBy === "title") {
        return left.title.localeCompare(right.title);
      }
      if (sortBy === "date") {
        return sortDate(right.decision_date) - sortDate(left.decision_date);
      }
      return right.importance - left.importance;
    });
  }, [data.decisions.items, query, sortBy, statusFilter]);

  return (
    <div className="space-y-6">
      <SectionCard title="Decisions" kicker="Register">
        <div className="grid gap-4 md:grid-cols-4">
          <MetricCard label="Decisions" value={String(data.decisions.counts.total)} />
          <MetricCard label="Status Defined" value={String(data.decisions.counts.defined_status)} />
          <MetricCard label="Owner Defined" value={String(data.decisions.counts.owner_defined)} />
          <MetricCard label="Source Notes" value={String(data.decisions.counts.source_notes)} />
        </div>
      </SectionCard>

      <SectionCard title="Decision Register" kicker="Canonical">
        <div className="grid gap-4 rounded-3xl bg-white/70 p-4 lg:grid-cols-[1.2fr_0.7fr_0.7fr_auto]">
          <label className="text-sm text-ink/80">
            <span className="mb-2 block font-semibold text-ink">Search</span>
            <input
              className="w-full rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm text-ink"
              value={query}
              placeholder="Search title, owner, rationale"
              onChange={(event) => setQuery(event.target.value)}
            />
          </label>
          <label className="text-sm text-ink/80">
            <span className="mb-2 block font-semibold text-ink">Status</span>
            <select
              className="w-full rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm text-ink"
              value={statusFilter}
              onChange={(event) => setStatusFilter(event.target.value)}
            >
              <option value="ALL">All</option>
              <option value="OPEN">OPEN</option>
              <option value="SUPPORTED">SUPPORTED</option>
              <option value="WATCH">WATCH</option>
              <option value="AT RISK">AT RISK</option>
              <option value="CLOSED">CLOSED</option>
              <option value="Not defined">Not defined</option>
            </select>
          </label>
          <label className="text-sm text-ink/80">
            <span className="mb-2 block font-semibold text-ink">Sort</span>
            <select
              className="w-full rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm text-ink"
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value as SortOption)}
            >
              <option value="importance">Importance</option>
              <option value="date">Decision Date</option>
              <option value="title">Title</option>
            </select>
          </label>
          <div className="rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm leading-6 text-ink/80">
            <p><span className="font-semibold text-ink">Visible:</span> {filteredItems.length}</p>
            <p><span className="font-semibold text-ink">Canonical:</span> {data.decisions.items.length}</p>
          </div>
        </div>

        <div className="mt-6 space-y-4">
          {filteredItems.map((item) => (
            <Link
              key={item.decision_id}
              to={item.route}
              className="block rounded-2xl border border-ink/10 bg-white/70 p-5 transition hover:border-accent/40 hover:bg-white focus:outline-none focus:ring-2 focus:ring-accent/30"
            >
              <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <StatusPill value={item.status} />
                    <StatusPill value={item.evidence_confidence} />
                  </div>
                  <div>
                    <h3 className="font-serif text-2xl text-ink">{item.title}</h3>
                    <p className="mt-2 text-sm leading-6 text-ink/75">{item.rationale}</p>
                  </div>
                </div>
                <div className="grid gap-3 rounded-2xl bg-paper p-4 text-sm leading-6 text-ink/80 md:grid-cols-2 xl:min-w-[24rem]">
                  <p><span className="font-semibold text-ink">Owner:</span> {item.owner}</p>
                  <p><span className="font-semibold text-ink">Decision Date:</span> {item.decision_date}</p>
                  <p><span className="font-semibold text-ink">Projects:</span> {item.related_project_count}</p>
                  <p><span className="font-semibold text-ink">Objectives:</span> {item.related_objective_count}</p>
                </div>
              </div>

              <div className="mt-4 grid gap-4 text-sm leading-6 text-ink/80 lg:grid-cols-2">
                <div className="rounded-2xl bg-paper p-4">
                  <p><span className="font-semibold text-ink">People:</span> {item.related_people_count}</p>
                  <p><span className="font-semibold text-ink">Source:</span> {item.source_path}</p>
                </div>
                <div className="rounded-2xl bg-paper p-4">
                  <p><span className="font-semibold text-ink">Importance:</span> {item.importance}</p>
                  <p><span className="font-semibold text-ink">Missing Information:</span> {item.missing_fields[0] ?? "No material missing information identified."}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-white/70 p-4">
      <p className="text-xs uppercase tracking-[0.2em] text-accent">{label}</p>
      <p className="mt-3 font-serif text-3xl">{value}</p>
    </div>
  );
}

function sortDate(value: string): number {
  if (!value || value === "No evidence found" || value === "Not defined") {
    return 0;
  }
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? 0 : parsed;
}
