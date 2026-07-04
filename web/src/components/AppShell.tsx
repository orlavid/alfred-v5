import { NavLink } from "react-router-dom";
import { PropsWithChildren } from "react";

const NAV_ITEMS = [
  ["Dashboard", "/"],
  ["Objectives", "/objectives"],
  ["Projects", "/projects"],
  ["Meetings", "/meetings"],
  ["Board", "/board"],
  ["Ask Alfred", "/ask-alfred"],
  ["Daily Brief", "/daily-brief"],
  ["Knowledge", "/knowledge"],
] as const;

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen bg-canvas text-ink">
      <div className="mx-auto flex min-h-screen max-w-[1600px] flex-col gap-6 px-4 py-4 md:flex-row md:px-6">
        <aside className="rounded-[2rem] border border-white/60 bg-ink px-5 py-6 text-white shadow-panel md:sticky md:top-4 md:h-[calc(100vh-2rem)] md:w-72 md:flex-none">
          <div className="mb-8">
            <p className="text-xs uppercase tracking-[0.35em] text-white/60">Alfred</p>
            <h1 className="mt-3 font-serif text-3xl">Executive UI</h1>
            <p className="mt-3 text-sm text-white/70">A read-only operating surface built from the canonical dashboard API.</p>
          </div>
          <nav className="flex gap-2 overflow-x-auto md:flex-col">
            {NAV_ITEMS.map(([label, to]) => (
              <NavLink
                key={to}
                to={to}
                end={to === "/"}
                className={({ isActive }) =>
                  `rounded-2xl px-4 py-3 text-sm font-medium transition ${
                    isActive ? "bg-white text-ink" : "bg-white/5 text-white/75 hover:bg-white/10 hover:text-white"
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="mt-8 hidden rounded-3xl bg-white/5 p-4 text-sm text-white/70 md:block">
            <p className="font-semibold text-white">Mandate</p>
            <p className="mt-2">Show what matters next. Keep the frontend thin. Keep the model canonical.</p>
          </div>
        </aside>
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
