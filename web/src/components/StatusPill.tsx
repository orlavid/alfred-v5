type StatusPillProps = {
  value: string;
};

const CLASS_MAP: Record<string, string> = {
  high: "bg-signal/15 text-signal",
  critical: "bg-signal/15 text-signal",
  medium: "bg-accent/15 text-accent",
  low: "bg-pine/15 text-pine",
  active: "bg-pine/15 text-pine",
  watch: "bg-accent/15 text-accent",
  "at risk": "bg-signal/15 text-signal",
  supported: "bg-pine/15 text-pine",
  amber: "bg-accent/15 text-accent",
  green: "bg-pine/15 text-pine",
  red: "bg-signal/15 text-signal",
  "not defined": "bg-ink/10 text-ink",
};

export function StatusPill({ value }: StatusPillProps) {
  const key = value.toLowerCase();
  const className = CLASS_MAP[key] ?? "bg-ink/10 text-ink";
  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] ${className}`}>
      {value}
    </span>
  );
}
