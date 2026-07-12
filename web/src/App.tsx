import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "@/components/AppShell";
import { SectionCard } from "@/components/SectionCard";
import { DashboardPage } from "@/pages/DashboardPage";
import { ObjectivesPage } from "@/pages/ObjectivesPage";
import { ObjectiveDetailPage } from "@/pages/ObjectiveDetailPage";
import { ProjectsPage } from "@/pages/ProjectsPage";
import { ProjectDetailPage } from "@/pages/ProjectDetailPage";
import { DecisionsPage } from "@/pages/DecisionsPage";
import { DecisionDetailPage } from "@/pages/DecisionDetailPage";
import { MeetingsPage } from "@/pages/MeetingsPage";
import { BoardPage } from "@/pages/BoardPage";
import { AskAlfredPage } from "@/pages/AskAlfredPage";
import { DailyBriefPage } from "@/pages/DailyBriefPage";
import { KnowledgePage } from "@/pages/KnowledgePage";
import { HelpPage } from "@/pages/HelpPage";
import { AdminSecurityPage } from "@/pages/AdminSecurityPage";
import { FollowupsPage } from "@/pages/FollowupsPage";
import { OpenLoopsPage } from "@/pages/OpenLoopsPage";
import { ActionsPage } from "@/pages/ActionsPage";
import { ExecutiveSummaryPage } from "@/pages/ExecutiveSummaryPage";
import { PlaceholderPage } from "@/pages/PlaceholderPage";
import { loadDashboard, loadRefreshStatus, requestRefreshNow } from "@/lib/loadDashboard";
import type { DashboardBootstrapPayload, SnapshotInfo } from "@/types";
import { startTransition, useEffect, useState } from "react";

export function App() {
  const [data, setData] = useState<DashboardBootstrapPayload | null>(null);
  const [snapshot, setSnapshot] = useState<SnapshotInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [askQuery, setAskQuery] = useState("What should I do today?");

  const refreshDashboard = async () => {
    const refreshState = await requestRefreshNow();
    startTransition(() => {
      setSnapshot(refreshState);
      setError(null);
    });

    let current = refreshState;
    while (current.refresh_in_progress) {
      await new Promise((resolve) => setTimeout(resolve, 2000));
      current = await loadRefreshStatus();
      startTransition(() => setSnapshot(current));
    }

    const payload = await loadDashboard();
    startTransition(() => {
      setData(payload);
      setSnapshot(payload.snapshot);
      setAskQuery(payload.ask_alfred.questions[0] ?? "What should I do today?");
      setError(null);
    });
  };

  useEffect(() => {
    let cancelled = false;
    loadDashboard()
      .then((payload) => {
        if (!cancelled) {
          startTransition(() => {
            setData(payload);
            setSnapshot(payload.snapshot);
            setAskQuery(payload.ask_alfred.questions[0] ?? "What should I do today?");
          });
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
  }, []);

  return (
    <AppShell askQuery={askQuery} onAskQueryChange={setAskQuery} snapshot={snapshot} onRefreshNow={() => { void refreshDashboard(); }}>
      {!data && !error ? <LoadingState /> : null}
      {error ? <ErrorState message={error} /> : null}
      {data ? (
        <Routes>
          <Route path="/" element={<DashboardPage data={data} />} />
          <Route path="/daily-brief" element={<DailyBriefPage data={data} />} />
          <Route path="/executive-summary" element={<ExecutiveSummaryPage data={data} />} />
          <Route path="/objectives" element={<ObjectivesPage data={data} />} />
          <Route path="/objectives/:objectiveId" element={<ObjectiveDetailPage data={data} onRefresh={refreshDashboard} />} />
          <Route path="/projects" element={<ProjectsPage data={data} />} />
          <Route path="/projects/:projectId" element={<ProjectDetailPage data={data} onRefresh={refreshDashboard} />} />
          <Route path="/decisions" element={<DecisionsPage data={data} />} />
          <Route path="/decisions/:decisionId" element={<DecisionDetailPage data={data} />} />
          <Route
            path="/programmes"
            element={<PlaceholderPage title="Programmes" kicker="Objectives" summary="Programme navigation is reserved for grouped objective delivery views." bullets={["Programme rollups will surface after dedicated backend page shaping is added.", "Use Projects and Objectives as the current canonical views."]} />}
          />
          <Route
            path="/milestones"
            element={<PlaceholderPage title="Milestones" kicker="Objectives" summary="Milestone tracking will sit between objectives and project execution." bullets={["Milestone timelines are not shaped into the dashboard payload yet.", "Current milestone evidence should remain in Obsidian until the dedicated view is added."]} />}
          />
          <Route path="/meetings" element={<MeetingsPage data={data} />} />
          <Route
            path="/people"
            element={<PlaceholderPage title="People" kicker="kNowledge" summary="People navigation is reserved for executive relationship and stakeholder views." bullets={["Use Meeting Intelligence and Board pages for current people context.", "A dedicated people dataset should arrive through future Dashboard API shaping."]} />}
          />
          <Route
            path="/companies"
            element={<PlaceholderPage title="Companies" kicker="kNowledge" summary="Company context will eventually expose counterparties, suppliers, and governance posture." bullets={["Current supplier pressure is still visible from the dashboard and reasoning layers.", "A dedicated company route should remain read-only and backend-shaped."]} />}
          />
          <Route path="/knowledge" element={<KnowledgePage data={data} />} />
          <Route path="/knowledge-graph" element={<KnowledgePage data={data} />} />
          <Route path="/follow-ups" element={<FollowupsPage data={data} />} />
          <Route path="/open-loops" element={<OpenLoopsPage data={data} />} />
          <Route path="/actions" element={<ActionsPage data={data} />} />
          <Route
            path="/workflow"
            element={<PlaceholderPage title="Workflow" kicker="Tasks" summary="Workflow will become the action-ledger and multi-step execution surface." bullets={["Dashboard-entered work should first land in Alfred’s interaction or action ledger.", "Important items should later flow into the Obsidian write-back queue before ExecutiveState is recomputed."]} />}
          />
          <Route
            path="/risks"
            element={<PlaceholderPage title="Risks" kicker="Risks" summary="Risk navigation will collect escalations, controls, and operating threats in one read-only view." bullets={["Current risk signals remain visible in the dashboard, meetings, and Daily Brief.", "A dedicated risks page should be introduced from backend-shaped risk data only."]} />}
          />
          <Route path="/board" element={<BoardPage data={data} />} />
          <Route
            path="/governance"
            element={<PlaceholderPage title="Governance" kicker="Risks" summary="Governance navigation will surface board rights, control posture, and unresolved governance loops." bullets={["Board Governance remains the active governance source in this release.", "Dedicated governance navigation should stay tied to canonical board and control models."]} />}
          />
          <Route
            path="/executive-health"
            element={<PlaceholderPage title="Executive Health" kicker="Risks" summary="Executive health will become the focused view for posture, confidence, and pressure trends." bullets={["Current health is already rendered on the Dashboard, Daily Brief, and Executive Summary pages.", "Future detail should still come from ExecutiveState rather than client-side recomputation."]} />}
          />
          <Route
            path="/compliance"
            element={<PlaceholderPage title="Compliance" kicker="Risks" summary="Compliance navigation will later hold control status, exceptions, and audit-sensitive records." bullets={["Compliance data is intentionally placeholder-only in this phase.", "Production compliance surfaces should remain authenticated and fully backend-governed."]} />}
          />
          <Route path="/ask-alfred" element={<AskAlfredPage data={data} query={askQuery} onQueryChange={setAskQuery} />} />
          <Route
            path="/admin"
            element={<AdminSecurityPage data={data} />}
          />
          <Route
            path="/security"
            element={<AdminSecurityPage data={data} />}
          />
          <Route
            path="/ai-models"
            element={<PlaceholderPage title="AI Models" kicker="Operations" summary="AI model controls will eventually cover basic enrichment versus deeper research pathways." bullets={["Do not implement deep research in this phase.", "Model routing, research budgets, and token controls belong in Admin and backend policy layers."]} />}
          />
          <Route
            path="/integrations"
            element={<PlaceholderPage title="Integrations" kicker="Operations" summary="Integration management will later cover Telegram, hosted sync, and API-based system connectivity." bullets={["Current mode remains local Mac-first.", "Future hosted or VPS sync should be designed as backend capability, not client logic."]} />}
          />
          <Route
            path="/system-health"
            element={<PlaceholderPage title="System Health" kicker="Operations" summary="System health will present app and knowledge pipeline status from canonical backend telemetry." bullets={["Executive health is visible today, but system health remains a placeholder.", "Production system health should be authenticated and backend-shaped."]} />}
          />
          <Route path="/help" element={<HelpPage />} />
          <Route
            path="/knowledge-base"
            element={<PlaceholderPage title="Knowledge Base" kicker="Library" summary="The knowledge base route will later surface reusable executive operating guidance." bullets={["Use Help and Documentation as the current library surfaces.", "Knowledge Base entries should remain exportable and compatible with Obsidian write-back later."]} />}
          />
          <Route
            path="/obsidian"
            element={<PlaceholderPage title="Obsidian" kicker="Library" summary="Obsidian remains the source of truth for executive knowledge." bullets={["Important dashboard-entered content should eventually queue for markdown write-back.", "Current UI mode does not implement write-back yet."]} />}
          />
          <Route
            path="/documentation"
            element={<PlaceholderPage title="Documentation" kicker="Library" summary="Documentation is reserved for operating references, build notes, and UI guidance." bullets={["Use the Work Instructions page for operator guidance in this phase.", "Long-form technical material should remain documented outside page-level business logic."]} />}
          />
          <Route
            path="/prompt-library"
            element={<PlaceholderPage title="Prompt Library" kicker="Library" summary="Prompt Library will eventually collect curated executive prompts and operating patterns." bullets={["Prompt assets should remain governed and exportable.", "Do not implement prompt editing workflows in this phase."]} />}
          />
          <Route
            path="/external-links"
            element={<PlaceholderPage title="External Links" kicker="Library" summary="External links will later hold approved outbound navigation for executive workflows." bullets={["Keep the current app read-only and locally safe.", "External destinations should eventually be explicitly governed from backend or admin configuration."]} />}
          />
          <Route path="/admin-security" element={<AdminSecurityPage data={data} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      ) : null}
    </AppShell>
  );
}

function LoadingState() {
  return (
    <SectionCard title="Loading Executive Dashboard" kicker="Boot">
      <p className="text-sm leading-6 text-ink/70">Reading the latest dashboard payload from the Alfred API.</p>
    </SectionCard>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <SectionCard title="Dashboard Unavailable" kicker="Error">
      <p className="text-sm leading-6 text-ink/70">{message}</p>
      <p className="mt-3 text-sm leading-6 text-ink/70">Run `python build_dashboard_api.py` to refresh the frontend payload.</p>
    </SectionCard>
  );
}
