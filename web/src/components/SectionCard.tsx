import { PropsWithChildren, ReactNode } from "react";

type SectionCardProps = PropsWithChildren<{
  title: string;
  kicker?: string;
  action?: ReactNode;
  className?: string;
}>;

export function SectionCard({ title, kicker, action, className = "", children }: SectionCardProps) {
  return (
    <section className={`rounded-3xl border border-white/70 bg-paper p-6 shadow-panel ${className}`}>
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          {kicker ? <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">{kicker}</p> : null}
          <h2 className="mt-2 font-serif text-2xl text-ink">{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}
