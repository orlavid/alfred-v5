import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import { loadProjectsDomain } from "@/lib/loadDashboard";
import { useDomainPayload } from "@/lib/useDomainPayload";
import type { DashboardBootstrapPayload, DashboardPayload, ProjectsDomainPayload } from "@/types";

type SortOption = "attention" | "title" | "recent";

export function ProjectsPage({ data }: { data: DashboardBootstrapPayload | DashboardPayload }) {
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [sortBy, setSortBy] = useState<SortOption>("attention");
  const embeddedDomain = useMemo(
    () => ("items" in data.projects ? (data.projects as ProjectsDomainPayload) : null),
    [data.projects],
  );
  const { data: domain, error } = useDomainPayload(embeddedDomain, loadProjectsDomain);

  const filteredItems = useMemo(() => {
    if (!domain) {
      return [];
    }
    const lower = query.trim().toLowerCase();
    const items = domain.items.filter((item) => {
      if (statusFilter !== "ALL" && item.status !== statusFilter) {
        return false;
      }
      if (!lower) {
        return true;
      }
      return [
        item.title,
        item.owner,
        item.risk,
        item.recommendation,
        ...item.objective_linkage,
      ].some((value) => value.toLowerCase().includes(lower));
    });

    return items.sort((left, right) => {
      if (sortBy === "title") {
        return left.title.localeCompare(right.title);
      }
      if (sortBy === "recent") {
        return sortDate(right.last_meaningful_activity) - sortDate(left.last_meaningful_activity);
      }
      return attentionScore(right) - attentionScore(left);
    });
  }, [domain, query, sortBy, statusFilter]);

  return (
    <div className="space-y-6">
      <SectionCard title="Projects" kicker="Delivery">
        <div className="grid gap-4 md:grid-cols-4">
          {Object.entries(data.projects.health).map(([key, value]) => (
            <div key={key} className="rounded-2xl bg-white/70 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-accent">{key.replace("_", " ")}</p>
              <p className="mt-3 font-serif text-3xl">{value}</p>
            </div>
          ))}
        </div>
      </SectionCard>

      <SectionCard title="Project Register" kicker="Management Workspace">
        <div className="grid gap-4 rounded-3xl bg-white/70 p-4 lg:grid-cols-[1.2fr_0.7fr_0.7fr_auto]">
          <label className="text-sm text-ink/80">
            <span className="mb-2 block font-semibold text-ink">Search</span>
            <input
              className="w-full rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm text-ink"
              value={query}
              placeholder="Search title, owner, objective, risk"
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
              <option value="AT RISK">AT RISK</option>
              <option value="WATCH">WATCH</option>
              <option value="SUPPORTED">SUPPORTED</option>
              <option value="HOLD">HOLD</option>
              <option value="CLOSED">CLOSED</option>
            </select>
          </label>
          <label className="text-sm text-ink/80">
            <span className="mb-2 block font-semibold text-ink">Sort</span>
            <select
              className="w-full rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm text-ink"
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value as SortOption)}
            >
              <option value="attention">Needs Attention</option>
              <option value="recent">Recent Activity</option>
              <option value="title">Title</option>
            </select>
          </label>
          <div className="rounded-2xl border border-ink/10 bg-paper px-4 py-3 text-sm leading-6 text-ink/80">
            <p><span className="font-semibold text-ink">Visible:</span> {filteredItems.length}</p>
            <p><span className="font-semibold text-ink">Canonical:</span> {domain?.items.length ?? 0}</p>
          </div>
        </div>

        {error ? (
          <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm leading-6 text-red-800">
            {error}
          </div>
        ) : null}
        {!error && !domain ? (
          <div className="mt-6 rounded-2xl border border-ink/10 bg-white/70 p-4 text-sm leading-6 text-ink/70">
            Reading the latest published project register.
          </div>
        ) : null}
        <div className="mt-6 space-y-4">
          {filteredItems.map((item) => (
            <Link
              key={item.project_id}
              to={item.route}
              className="block rounded-2xl border border-ink/10 bg-white/70 p-5 transition hover:border-accent/40 hover:bg-white focus:outline-none focus:ring-2 focus:ring-accent/30"
            >
              <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <StatusPill value={item.status} />
                    <StatusPill value={item.health} />
                    <StatusPill value={item.evidence_confidence} />
                  </div>
                  <div>
                    <h3 className="font-serif text-2xl text-ink">{item.title}</h3>
                    <p className="mt-2 text-sm leading-6 text-ink/75">{item.recommendation}</p>
                  </div>
                </div>
                <div className="grid gap-3 rounded-2xl bg-paper p-4 text-sm leading-6 text-ink/80 md:grid-cols-2 xl:min-w-[24rem]">
                  <p><span className="font-semibold text-ink">Owner:</span> {item.owner}</p>
                  <p><span className="font-semibold text-ink">Last Activity:</span> {item.last_meaningful_activity}</p>
                  <p><span className="font-semibold text-ink">Next Checkpoint:</span> {item.next_checkpoint_or_deadline}</p>
                  <p><span className="font-semibold text-ink">Open Actions:</span> {item.open_action_count}</p>
                </div>
              </div>

              <div className="mt-4 grid gap-4 text-sm leading-6 text-ink/80 lg:grid-cols-2">
                <div className="rounded-2xl bg-paper p-4">
                  <p><span className="font-semibold text-ink">Objectives:</span> {item.objective_linkage.join(", ") || "No evidence found"}</p>
                  <p><span className="font-semibold text-ink">Risk / Blocker:</span> {item.risk}</p>
                </div>
                <div className="rounded-2xl bg-paper p-4">
                  <p><span className="font-semibold text-ink">Linked Decisions:</span> {item.linked_decision_count}</p>
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

function attentionScore(item: ProjectsDomainPayload["items"][number]): number {
  let score = 0;
  if (item.status === "AT RISK") {
    score += 100;
  } else if (item.status === "WATCH") {
    score += 60;
  } else if (item.status === "SUPPORTED") {
    score += 20;
  }
  score += item.open_action_count * 5;
  score += item.linked_decision_count * 3;
  if (item.owner === "Not defined") {
    score += 10;
  }
  return score;
}

function sortDate(value: string): number {
  if (!value || value === "No evidence found" || value === "Not defined") {
    return 0;
  }
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? 0 : parsed;
}
