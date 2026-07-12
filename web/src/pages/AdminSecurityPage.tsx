import { SectionCard } from "@/components/SectionCard";
import type { AdminAction, AdminComponent, DashboardBootstrapPayload, DashboardPayload } from "@/types";

const SECTION_ORDER: Array<[string, keyof DashboardBootstrapPayload["admin_configuration"]["sections"]]> = [
  ["Core Configuration", "core_configuration"],
  ["Vault", "vault"],
  ["AI Providers", "ai_providers"],
  ["Knowledge Sources", "knowledge_sources"],
  ["Runtime", "runtime"],
  ["Services", "services"],
  ["Security", "security"],
  ["Diagnostics", "diagnostics"],
  ["Deployment", "deployment"],
  ["Required Actions", "required_actions"],
];

export function AdminSecurityPage({ data }: { data: DashboardBootstrapPayload | DashboardPayload }) {
  const admin = data.admin_configuration;

  return (
    <div className="space-y-6">
      <SectionCard title="Overview" kicker="Platform Management">
        <div className="space-y-3 text-sm leading-6 text-ink/80">
          <p>Environment Score: {admin.overview.environment_score}%</p>
          <p>Overall Health: {admin.overview.overall_health}</p>
          <p>{admin.overview.architecture_rule}</p>
          <ul className="space-y-1">
            {admin.overview.summary_lines.map((item) => (
              <li key={item}>- {item}</li>
            ))}
          </ul>
        </div>
      </SectionCard>

      <SectionCard title="Operational Actions" kicker="Commands">
        <div className="grid gap-3 md:grid-cols-2">
          {admin.actions.map((action) => (
            <ActionCard key={action.label} action={action} />
          ))}
        </div>
      </SectionCard>

      <SectionCard title="Auto Configuration" kicker="Discovered">
        <div className="space-y-3">
          {Object.entries(admin.auto_configured).map(([key, value]) => (
            <div key={key} className="rounded-2xl border border-ink/10 bg-white/70 p-4 text-sm text-ink/80">
              <p className="font-semibold text-ink">{key}</p>
              <p>Value: {value.value}</p>
              <p>Discovery Method: {value.discovery_method}</p>
              <p>Confidence: {value.confidence}</p>
              <p>Timestamp: {value.timestamp}</p>
            </div>
          ))}
        </div>
      </SectionCard>

      {SECTION_ORDER.map(([title, key]) => (
        <SectionCard key={title} title={title} kicker="Admin / Configuration">
          {key === "deployment" ? (
            <div className="grid gap-3 md:grid-cols-2">
              {(admin.sections[key] as AdminAction[]).map((action) => (
                <ActionCard key={action.label} action={action} />
              ))}
            </div>
          ) : key === "required_actions" ? (
            <ul className="space-y-2 text-sm leading-6 text-ink/80">
              {(admin.sections[key] as string[]).map((item) => (
                <li key={item}>- {item}</li>
              ))}
              {(admin.sections[key] as string[]).length === 0 ? <li>- None.</li> : null}
            </ul>
          ) : (
            <div className="space-y-3">
              {(admin.sections[key] as AdminComponent[]).map((component) => (
                <ComponentCard key={component.name} component={component} />
              ))}
            </div>
          )}
        </SectionCard>
      ))}
    </div>
  );
}

function ComponentCard({ component }: { component: AdminComponent }) {
  return (
    <div className="rounded-2xl border border-ink/10 bg-white/75 p-4 text-sm leading-6 text-ink/80">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="font-semibold text-ink">{component.name}</p>
        <div className="flex gap-2">
          <StatusPill label={component.status} />
          <StatusPill label={component.health} tone="soft" />
        </div>
      </div>
      <p>Version: {component.version || "n/a"}</p>
      <p>Detected Location: {component.install_location || "Not detected"}</p>
      <p>Configuration Source: {component.configuration_source || "Unknown"}</p>
      <p>{component.required ? "Required" : "Optional"}</p>
      <p>Next Action: {component.recommended_action}</p>
      <p>Work Instruction: {component.work_instruction_link}</p>
    </div>
  );
}

function ActionCard({ action }: { action: AdminAction }) {
  return (
    <div className="rounded-2xl border border-ink/10 bg-white/75 p-4 text-sm leading-6 text-ink/80">
      <p className="font-semibold text-ink">{action.label}</p>
      <p>{action.summary}</p>
      <p>Invocation: {action.command}</p>
      <p>Mode: {action.mode}</p>
      <p>Work Instruction: {action.work_instruction_link}</p>
    </div>
  );
}

function StatusPill({ label, tone = "solid" }: { label: string; tone?: "solid" | "soft" }) {
  const base =
    tone === "solid"
      ? "rounded-full bg-ink px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-white"
      : "rounded-full bg-sand px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-ink";
  return <span className={base}>{label}</span>;
}
