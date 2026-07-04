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
          className={`rounded-[2rem] border border-white/60 bg-ink px-4 py-6 text-white shadow-panel transition-[width] duration-300 md:sticky md:top-4 md:h-[calc(100vh-2rem)] md:flex-none ${
            expanded ? "md:w-[28rem]" : "md:w-24"
          }`}
        >
          <div className="flex h-full gap-4">
            <div className="flex w-12 flex-col items-center gap-3 pt-2">
              {CONTROL_SECTIONS.map((section) => (
                <div key={section.title} className={`flex h-10 w-10 items-center justify-center rounded-2xl text-sm font-semibold shadow-sm ${section.color}`}>
                  {section.rail}
                </div>
              ))}
            </div>
            <div className={`min-w-0 flex-1 overflow-hidden transition-all duration-300 ${expanded ? "opacity-100" : "pointer-events-none opacity-0"}`}>
              <div className="mb-6">
                <p className="text-xs uppercase tracking-[0.35em] text-white/60">Alfred</p>
                <h1 className="mt-3 font-serif text-3xl">CONTROL</h1>
                <p className="mt-3 text-sm text-white/70">Permanent executive navigation for command, context, and controlled execution.</p>
              </div>
              <nav className="space-y-4">
                {CONTROL_SECTIONS.map((section) => (
                  <div key={section.title} className="rounded-3xl bg-white/5 p-3">
                    <div className="mb-3 flex items-center gap-3">
                      <span className={`flex h-8 w-8 items-center justify-center rounded-xl text-xs font-semibold ${section.color}`}>
                        {section.rail}
                      </span>
                      <span className="text-xs font-semibold uppercase tracking-[0.24em] text-white/70">{section.title}</span>
                    </div>
                    <div className="space-y-1">
                      {section.items.map((item) => (
                        <NavLink
                          key={item.path}
                          to={item.path}
                          end={item.path === "/"}
                          className={({ isActive }) =>
                            `block rounded-2xl px-4 py-2 text-sm font-medium transition ${
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
              <div className="mt-6 rounded-3xl bg-white/5 p-4 text-sm text-white/70">
                <p className="font-semibold text-white">Behaviour</p>
                <p className="mt-2">The CONTROL rail stays thin by default, expands on hover, and preserves the current page without click-driven layout toggles.</p>
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
