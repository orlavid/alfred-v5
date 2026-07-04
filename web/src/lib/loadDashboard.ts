import type { DashboardPayload } from "@/types";

export async function loadDashboard(): Promise<DashboardPayload> {
  const response = await fetch("/api/dashboard-home.json");
  if (!response.ok) {
    throw new Error(`Failed to load dashboard data: ${response.status}`);
  }
  return (await response.json()) as DashboardPayload;
}
