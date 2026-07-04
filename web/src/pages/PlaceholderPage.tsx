import { SectionCard } from "@/components/SectionCard";

type PlaceholderPageProps = {
  title: string;
  kicker: string;
  summary: string;
  bullets: string[];
};

export function PlaceholderPage({ title, kicker, summary, bullets }: PlaceholderPageProps) {
  return (
    <div className="space-y-6">
      <SectionCard title={title} kicker={kicker}>
        <p className="text-sm leading-6 text-ink/75">{summary}</p>
      </SectionCard>
      <SectionCard title="Current Scope" kicker="Placeholder">
        <ul className="space-y-2 text-sm leading-6 text-ink/80">
          {bullets.map((item) => (
            <li key={item}>- {item}</li>
          ))}
        </ul>
      </SectionCard>
    </div>
  );
}
