import type {
  DashboardBootstrapPayload,
  DecisionsDomainPayload,
  FollowupsDomainPayload,
  ExecutiveMatterDetail,
  MattersDomainPayload,
  ObjectiveDetail,
  ObjectivesDomainPayload,
  OpenLoopsDomainPayload,
  ProjectDetail,
  ProjectsDomainPayload,
  SnapshotInfo,
} from "@/types";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to load ${path}: ${response.status}`);
  }
  return (await response.json()) as T;
}

export async function loadDashboard(): Promise<DashboardBootstrapPayload> {
  return fetchJson<DashboardBootstrapPayload>("/api/dashboard-home.json");
}

export async function loadObjectivesDomain(): Promise<ObjectivesDomainPayload> {
  return fetchJson<ObjectivesDomainPayload>("/api/objectives.json");
}

export async function loadObjectiveDetail(objectiveId: string): Promise<ObjectiveDetail> {
  return fetchJson<ObjectiveDetail>(`/api/objectives/${objectiveId}.json`);
}

export async function loadProjectsDomain(): Promise<ProjectsDomainPayload> {
  return fetchJson<ProjectsDomainPayload>("/api/projects.json");
}

export async function loadProjectDetail(projectId: string): Promise<ProjectDetail> {
  return fetchJson<ProjectDetail>(`/api/projects/${projectId}.json`);
}

export async function loadDecisionsDomain(): Promise<DecisionsDomainPayload> {
  return fetchJson<DecisionsDomainPayload>("/api/decisions.json");
}

export async function loadFollowupsDomain(): Promise<FollowupsDomainPayload> {
  return fetchJson<FollowupsDomainPayload>("/api/followups.json");
}

export async function loadOpenLoopsDomain(): Promise<OpenLoopsDomainPayload> {
  return fetchJson<OpenLoopsDomainPayload>("/api/open-loops.json");
}

export async function loadMattersDomain(): Promise<MattersDomainPayload> {
  return fetchJson<MattersDomainPayload>("/api/matters.json");
}

export async function loadMatterDetail(matterId: string): Promise<ExecutiveMatterDetail> {
  return fetchJson<ExecutiveMatterDetail>(`/api/matters/${matterId}.json`);
}

export async function loadRefreshStatus(): Promise<SnapshotInfo> {
  return fetchJson<SnapshotInfo>("/api/refresh-status.json");
}

export async function requestRefreshNow(): Promise<SnapshotInfo> {
  const response = await fetch("/api/refresh-now", { method: "POST" });
  if (!response.ok) {
    throw new Error(`Failed to request refresh: ${response.status}`);
  }
  const payload = (await response.json()) as { refresh: SnapshotInfo };
  return payload.refresh;
}
