import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "@/components/AppShell";
import { SectionCard } from "@/components/SectionCard";
import { DashboardPage } from "@/pages/DashboardPage";
import { ObjectivesPage } from "@/pages/ObjectivesPage";
import { ProjectsPage } from "@/pages/ProjectsPage";
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
import { loadDashboard } from "@/lib/loadDashboard";
import type { DashboardPayload } from "@/types";
import { useEffect, useState } from "react";

export function App() {
  const [data, setData] = useState<DashboardPayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [askQuery, setAskQuery] = useState("What should I do today?");

  useEffect(() => {
    let cancelled = false;
    loadDashboard()
      .then((payload) => {
        if (!cancelled) {
          setData(payload);
          setAskQuery(payload.ask_alfred.questions[0] ?? "What should I do today?");
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
    <AppShell askQuery={askQuery} onAskQueryChange={setAskQuery}>
      {!data && !error ? <LoadingState /> : null}
      {error ? <ErrorState message={error} /> : null}
      {data ? (
        <Routes>
          <Route path="/" element={<DashboardPage data={data} />} />
          <Route path="/daily-brief" element={<DailyBriefPage data={data} />} />
          <Route path="/objectives" element={<ObjectivesPage data={data} />} />
          <Route path="/projects" element={<ProjectsPage data={data} />} />
          <Route path="/meetings" element={<MeetingsPage data={data} />} />
          <Route path="/follow-ups" element={<FollowupsPage data={data} />} />
          <Route path="/open-loops" element={<OpenLoopsPage data={data} />} />
          <Route path="/actions" element={<ActionsPage data={data} />} />
          <Route path="/board" element={<BoardPage data={data} />} />
          <Route path="/ask-alfred" element={<AskAlfredPage data={data} query={askQuery} onQueryChange={setAskQuery} />} />
          <Route path="/help" element={<HelpPage />} />
          <Route path="/admin-security" element={<AdminSecurityPage />} />
          <Route path="/knowledge" element={<KnowledgePage data={data} />} />
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
