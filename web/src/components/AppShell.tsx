import { NavLink, useNavigate } from "react-router-dom";
import { PropsWithChildren, useState } from "react";

const NAV_ITEMS = [
  ["Dashboard", "/"],
  ["Daily Brief", "/daily-brief"],
  ["Objectives", "/objectives"],
  ["Projects", "/projects"],
  ["Meetings", "/meetings"],
  ["Follow-ups", "/follow-ups"],
  ["Open Loops", "/open-loops"],
  ["Actions", "/actions"],
  ["Board", "/board"],
  ["Ask Alfred", "/ask-alfred"],
  ["Help", "/help"],
  ["Admin / Security", "/admin-security"],
  ["Knowledge", "/knowledge"],
] as const;

type AppShellProps = PropsWithChildren<{
  askQuery: string;
  onAskQueryChange: (value: string) => void;
}>;

export function AppShell({ children, askQuery, onAskQueryChange }: AppShellProps) {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();

  function submitAsk() {
    navigate("/ask-alfred");
  }

  return (
    <div className="min-h-screen bg-canvas text-ink">
      <div className="mx-auto flex min-h-screen max-w-[1600px] flex-col gap-6 px-4 py-4 md:flex-row md:px-6">
        <aside
          className={`rounded-[2rem] border border-white/60 bg-ink px-5 py-6 text-white shadow-panel md:sticky md:top-4 md:h-[calc(100vh-2rem)] md:flex-none ${
            collapsed ? "md:w-24" : "md:w-72"
          }`}
        >
          <div className="mb-8 flex items-start justify-between gap-4">
            <div className={collapsed ? "md:hidden" : ""}>
              <p className="text-xs uppercase tracking-[0.35em] text-white/60">Alfred</p>
              <h1 className="mt-3 font-serif text-3xl">Executive UI</h1>
              <p className="mt-3 text-sm text-white/70">A read-only operating surface built from the canonical dashboard API.</p>
            </div>
            <button
              type="button"
              onClick={() => setCollapsed((value) => !value)}
              className="rounded-2xl border border-white/10 bg-white/10 px-3 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-white transition hover:bg-white/20"
            >
              {collapsed ? "Open" : "Collapse"}
            </button>
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
                title={label}
              >
                <span className={collapsed ? "md:hidden" : ""}>{label}</span>
                <span className={collapsed ? "hidden md:inline" : "hidden"}>{label[0]}</span>
              </NavLink>
            ))}
          </nav>
          <div className={`mt-8 rounded-3xl bg-white/5 p-4 text-sm text-white/70 ${collapsed ? "hidden" : "hidden md:block"}`}>
            <p className="font-semibold text-white">Mandate</p>
            <p className="mt-2">Show what matters next. Keep the frontend thin. Keep the model canonical.</p>
          </div>
        </aside>
        <main className="flex-1 pb-32">{children}</main>
      </div>
      <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-ink/10 bg-canvas/95 backdrop-blur">
        <div className="mx-auto flex max-w-[1600px] flex-col gap-3 px-4 py-4 md:flex-row md:items-center md:px-6">
          <div className="md:w-72 md:flex-none">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-accent">Ask Alfred</p>
            <p className="mt-1 text-sm text-ink/70">Persistent executive query bar. Always visible while scrolling.</p>
          </div>
          <div className="flex flex-1 gap-3">
            <input
              value={askQuery}
              onChange={(event) => onAskQueryChange(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  submitAsk();
                }
              }}
              placeholder="Ask: What should I do today?"
              className="w-full rounded-2xl border border-ink/15 bg-white/90 px-4 py-3 text-sm text-ink outline-none transition focus:border-accent"
            />
            <button
              type="button"
              onClick={submitAsk}
              className="rounded-2xl bg-ink px-5 py-3 text-sm font-semibold text-white transition hover:bg-pine"
            >
              Open
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
