import { SectionCard } from "@/components/SectionCard";
import {
  DEPLOYMENT_DOWNLOADS_PATH,
  DEPLOYMENT_GUIDES,
  DEPLOYMENT_INDEX_PATH,
} from "@/deploymentCatalog";

export function DeploymentLinksPage() {
  return (
    <div className="space-y-6">
      <SectionCard title="Deployment Links" kicker="Library">
        <p className="text-sm leading-6 text-ink/75">
          Alfred keeps advanced services optional and explicitly deployed. This library page collects the operating
          guidance, downloadable placeholders, and current service posture for each optional capability.
        </p>
      </SectionCard>
      <SectionCard title="Work Instructions" kicker="Library">
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          <li>- Review deployment documents before introducing optional services.</li>
          <li>- Keep Obsidian and canonical executive knowledge flows stable before layering retrieval or enrichment.</li>
          <li>- Treat every optional service as explicitly configured, validated, and reversible.</li>
          <li>- Reference index: {DEPLOYMENT_INDEX_PATH}</li>
        </ul>
      </SectionCard>
      <SectionCard title="Downloadable Files" kicker="Library">
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          <li>- Placeholder bundle directory: {DEPLOYMENT_DOWNLOADS_PATH}</li>
          <li>- This folder is reserved for install bundles, config templates, and generated deployment artefacts.</li>
          <li>- Live installers are intentionally out of scope for this phase.</li>
        </ul>
      </SectionCard>
      <SectionCard title="Service Status" kicker="Library">
        <div className="grid gap-3 md:grid-cols-2">
          {DEPLOYMENT_GUIDES.map((guide) => (
            <div key={guide.path} className="rounded-2xl border border-ink/10 bg-white/70 p-4">
              <div className="flex items-center justify-between gap-3">
                <h3 className="font-serif text-xl text-ink">{guide.title}</h3>
                <span className="rounded-full bg-ink/5 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-ink/60">
                  {guide.status}
                </span>
              </div>
              <p className="mt-2 text-sm leading-6 text-ink/70">{guide.purpose}</p>
              <p className="mt-3 text-xs uppercase tracking-[0.22em] text-accent">{guide.documentPath}</p>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
