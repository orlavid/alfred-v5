type ObjectiveActionPayload = {
  action: string;
  actor?: string;
  reason?: string;
  [key: string]: unknown;
};

export async function postObjectiveAction(objectiveId: string, payload: ObjectiveActionPayload): Promise<void> {
  const response = await fetch(`/api/objectives/${objectiveId}/actions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Objective action failed: ${response.status}`);
  }
}
