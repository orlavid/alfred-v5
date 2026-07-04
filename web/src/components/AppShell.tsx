import { NavLink, useNavigate } from "react-router-dom";
import { PropsWithChildren, useState } from "react";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { CONTROL_SECTIONS } from "@/navigation";

type AppShellProps = PropsWithChildren<{
  askQuery: string;
  onAskQueryChange: (value: string) => void;
}>;

export function AppShell({ children, askQuery, onAskQueryChange }: AppShellProps) {
  const [expanded, setExpanded] = useState(false);
  const navigate = useNavigate();

  function submitAsk() {
    navigate("/ask-alfred");
  }

  return (
    <div className="min-h-screen bg-canvas text-ink">
      <div className="mx-auto flex min-h-screen max-w-[1600px] flex-col gap-6 px-4 py-4 md:flex-row md:px-6">
        <aside
          onMouseEnter={() => setExpanded(true)}
          onMouseLeave={() => setExpanded(false)}
          className={`rounded-[2rem] border border-white/60 bg-ink px-3 py-5 text-white shadow-panel transition-[width] duration-300 md:sticky md:top-4 md:h-[calc(100vh-2rem)] md:flex-none ${
            expanded ? "md:w-[19.5rem]" : "md:w-[4.75rem]"
          }`}
        >
          <div className="flex h-full gap-3">
            <div className="flex w-10 flex-col items-center justify-between py-1">
              {CONTROL_SECTIONS.map((section) => (
                <NavLink
                  key={section.title}
                  to={section.items[0].path}
                  className={`flex h-8 w-8 items-center justify-center rounded-xl text-xs font-semibold shadow-sm transition hover:scale-105 ${section.color}`}
                  title={section.title}
                >
                  {section.rail}
                </NavLink>
              ))}
            </div>
            <div className={`min-w-0 flex-1 overflow-hidden transition-all duration-300 ${expanded ? "opacity-100" : "pointer-events-none opacity-0"}`}>
              <div className="mb-4">
                <p className="text-xs uppercase tracking-[0.35em] text-white/60">Alfred</p>
                <h1 className="mt-2 font-serif text-2xl">CONTROL</h1>
                <p className="mt-2 text-xs leading-5 text-white/70">Permanent executive navigation for command, context, and controlled execution.</p>
              </div>
              <nav className="space-y-2">
                {CONTROL_SECTIONS.map((section) => (
                  <div key={section.title} className="rounded-2xl bg-white/5 p-2.5">
                    <div className="mb-2 flex items-center gap-2">
                      <span className={`flex h-7 w-7 items-center justify-center rounded-lg text-[11px] font-semibold ${section.color}`}>
                        {section.rail}
                      </span>
                      <NavLink to={section.items[0].path} className="text-[11px] font-semibold uppercase tracking-[0.2em] text-white/70 transition hover:text-white">
                        {section.title}
                      </NavLink>
                    </div>
                    <div className="grid grid-cols-2 gap-1">
                      {section.items.map((item) => (
                        <NavLink
                          key={item.path}
                          to={item.path}
                          end={item.path === "/"}
                          className={({ isActive }) =>
                            `block rounded-xl px-3 py-1.5 text-xs font-medium transition ${
                              isActive ? "bg-white text-ink" : "text-white/75 hover:bg-white/10 hover:text-white"
                            }`
                          }
                        >
                          {item.label}
                        </NavLink>
                      ))}
                    </div>
                  </div>
                ))}
              </nav>
              <div className="mt-3 rounded-2xl bg-white/5 p-3 text-xs leading-5 text-white/70">
                <p className="font-semibold text-white">Behaviour</p>
                <p className="mt-1">Thin rail by default. Expands on hover. Preserves page context. No click required.</p>
              </div>
            </div>
          </div>
        </aside>
        <main className="flex-1 pb-32">
          <Breadcrumbs />
          {children}
        </main>
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
