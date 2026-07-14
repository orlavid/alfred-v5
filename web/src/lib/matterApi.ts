type MatterActionPayload = {
  action: string;
  actor?: string;
  reason?: string;
  [key: string]: unknown;
};

export async function postMatterAction(matterId: string, payload: MatterActionPayload): Promise<void> {
  const response = await fetch(`/api/matters/${matterId}/actions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Matter action failed: ${response.status}`);
  }
}
