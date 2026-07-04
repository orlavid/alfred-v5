import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { PropsWithChildren, useState } from "react";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { CONTROL_SECTIONS, findNavigationEntry } from "@/navigation";

type AppShellProps = PropsWithChildren<{
  askQuery: string;
  onAskQueryChange: (value: string) => void;
}>;

export function AppShell({ children, askQuery, onAskQueryChange }: AppShellProps) {
  const [activeSection, setActiveSection] = useState<string | null>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const activeEntry = findNavigationEntry(location.pathname);
  const highlightedSection = activeEntry?.section.title;

  function submitAsk() {
    navigate("/ask-alfred");
  }

  return (
    <div className="min-h-screen bg-canvas text-ink">
      <div className="mx-auto flex min-h-screen max-w-[1600px] flex-col gap-6 px-4 py-4 md:flex-row md:px-6">
        <aside
          onMouseLeave={() => setActiveSection(null)}
          className="relative rounded-[2rem] border border-white/60 bg-ink px-3 py-5 text-white shadow-panel md:sticky md:top-4 md:h-[calc(100vh-2rem)] md:w-[4.75rem] md:flex-none"
        >
          <div className="flex h-full">
            <div className="flex w-10 flex-col items-center justify-between py-1">
              {CONTROL_SECTIONS.map((section) => (
                <div key={section.title} className="relative flex items-center">
                  <NavLink
                    to={section.items[0].path}
                    onMouseEnter={() => setActiveSection(section.title)}
                    onFocus={() => setActiveSection(section.title)}
                    aria-label={`Open ${section.title}`}
                    className={`flex h-8 w-8 items-center justify-center rounded-xl text-xs font-semibold shadow-sm transition hover:scale-105 ${
                      section.color
                    } ${highlightedSection === section.title ? "ring-2 ring-white ring-offset-2 ring-offset-ink" : ""}`}
                    title={section.title}
                  >
                    {section.rail}
                  </NavLink>
                  {activeSection === section.title ? (
                    <div className="absolute left-full top-1/2 z-30 ml-3 w-60 -translate-y-1/2 rounded-[1.75rem] border border-white/60 bg-ink/95 p-4 text-white shadow-panel backdrop-blur">
                      <div className="mb-3 flex items-center gap-3">
                        <span className={`flex h-8 w-8 items-center justify-center rounded-xl text-xs font-semibold ${section.color}`}>
                          {section.rail}
                        </span>
                        <div>
                          <p className="text-[11px] uppercase tracking-[0.24em] text-white/60">CONTROL</p>
                          <NavLink to={section.items[0].path} className="font-serif text-xl leading-none text-white">
                            {section.title}
                          </NavLink>
                        </div>
                      </div>
                      <nav className="space-y-1.5">
                        {section.items.map((item) => (
                          <NavLink
                            key={item.path}
                            to={item.path}
                            end={item.path === "/"}
                            className={({ isActive }) =>
                              `block rounded-2xl px-3 py-2 text-sm font-medium transition ${
                                isActive ? "bg-white text-ink" : "text-white/75 hover:bg-white/10 hover:text-white"
                              }`
                            }
                          >
                            {item.label}
                          </NavLink>
                        ))}
                      </nav>
                    </div>
                  ) : null}
                </div>
              ))}
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
