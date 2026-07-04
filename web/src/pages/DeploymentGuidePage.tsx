import { SectionCard } from "@/components/SectionCard";
import type { DeploymentGuide } from "@/deploymentCatalog";

type DeploymentGuidePageProps = {
  guide: DeploymentGuide;
};

function BulletList({ items }: { items: string[] }) {
  return (
    <ul className="space-y-2 text-sm leading-6 text-ink/80">
      {items.map((item) => (
        <li key={item}>- {item}</li>
      ))}
    </ul>
  );
}

export function DeploymentGuidePage({ guide }: DeploymentGuidePageProps) {
  return (
    <div className="space-y-6">
      <SectionCard title={guide.title} kicker="Deployment">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <p className="max-w-3xl text-sm leading-6 text-ink/75">{guide.purpose}</p>
          <div className="rounded-2xl border border-ink/10 bg-white/70 px-4 py-3 text-sm text-ink/75">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-accent">Status</p>
            <p className="mt-1 font-medium">{guide.status}</p>
          </div>
        </div>
      </SectionCard>
      <SectionCard title="When To Use" kicker="Deployment">
        <BulletList items={guide.whenToUse} />
      </SectionCard>
      <SectionCard title="Prerequisites" kicker="Deployment">
        <BulletList items={guide.prerequisites} />
      </SectionCard>
      <SectionCard title="Install Steps" kicker="Deployment">
        <BulletList items={guide.installSteps} />
      </SectionCard>
      <SectionCard title="Configuration Steps" kicker="Deployment">
        <BulletList items={guide.configurationSteps} />
      </SectionCard>
      <SectionCard title="Validation Commands" kicker="Deployment">
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          {guide.validationCommands.map((command) => (
            <li key={command}>- <code>{command}</code></li>
          ))}
        </ul>
      </SectionCard>
      <SectionCard title="Troubleshooting" kicker="Deployment">
        <BulletList items={guide.troubleshooting} />
      </SectionCard>
      <SectionCard title="Download Links" kicker="Deployment">
        <BulletList items={guide.downloads} />
      </SectionCard>
    </div>
  );
}
