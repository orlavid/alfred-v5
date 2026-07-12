type ProjectActionPayload = {
  action: string;
  actor?: string;
  reason?: string;
  [key: string]: unknown;
};

export async function postProjectAction(projectId: string, payload: ProjectActionPayload): Promise<void> {
  const response = await fetch(`/api/projects/${projectId}/actions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Project action failed: ${response.status}`);
  }
}
