import { Link, useLocation } from "react-router-dom";
import { findNavigationEntry } from "@/navigation";

export function Breadcrumbs() {
  const location = useLocation();
  const entry = findNavigationEntry(location.pathname);

  if (!entry) {
    return null;
  }

  return (
    <nav aria-label="Breadcrumb" className="mb-6 flex items-center gap-3 text-sm text-ink/60">
      <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] ${entry.section.color}`}>
        {entry.section.rail}
      </span>
      <Link to={entry.section.items[0].path} className="transition hover:text-ink">
        {entry.section.title}
      </Link>
      <span>/</span>
      <span className="font-medium text-ink">{entry.item.label}</span>
    </nav>
  );
}
