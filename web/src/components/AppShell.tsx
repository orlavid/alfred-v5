import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { PropsWithChildren, useLayoutEffect, useRef, useState } from "react";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { CONTROL_SECTIONS, findNavigationEntry } from "@/navigation";

type AppShellProps = PropsWithChildren<{
  askQuery: string;
  onAskQueryChange: (value: string) => void;
}>;

const FLYOUT_SAFE_MARGIN = 16;
const DEFAULT_FLYOUT_HEIGHT = 280;

export function getViewportSafeFlyoutTop(
  anchorCenterY: number,
  flyoutHeight: number,
  viewportHeight: number,
  margin = FLYOUT_SAFE_MARGIN,
) {
  const preferredTop = anchorCenterY - flyoutHeight / 2;
  const maxTop = Math.max(margin, viewportHeight - flyoutHeight - margin);
  return Math.min(Math.max(preferredTop, margin), maxTop);
}

export function AppShell({ children, askQuery, onAskQueryChange }: AppShellProps) {
  const [activeSection, setActiveSection] = useState<string | null>(null);
  const [flyoutPosition, setFlyoutPosition] = useState({ left: 88, top: FLYOUT_SAFE_MARGIN });
  const navigate = useNavigate();
  const location = useLocation();
  const activeEntry = findNavigationEntry(location.pathname);
  const highlightedSection = activeEntry?.section.title;
  const buttonRefs = useRef<Record<string, HTMLAnchorElement | null>>({});
  const flyoutRef = useRef<HTMLDivElement | null>(null);

  function submitAsk() {
    navigate("/ask-alfred");
  }

  useLayoutEffect(() => {
    if (!activeSection || typeof window === "undefined") {
      return;
    }

    const anchor = buttonRefs.current[activeSection];
    if (!anchor) {
      return;
    }

    const updatePosition = () => {
      const anchorRect = anchor.getBoundingClientRect();
      const flyoutHeight = flyoutRef.current?.offsetHeight ?? DEFAULT_FLYOUT_HEIGHT;
      setFlyoutPosition({
        left: anchorRect.right + 12,
        top: getViewportSafeFlyoutTop(anchorRect.top + anchorRect.height / 2, flyoutHeight, window.innerHeight),
      });
    };

    updatePosition();
    window.addEventListener("resize", updatePosition);
    return () => window.removeEventListener("resize", updatePosition);
  }, [activeSection]);

  const visibleSection = activeSection ? CONTROL_SECTIONS.find((section) => section.title === activeSection) : null;

  return (
    <div className="min-h-screen bg-canvas text-ink">
      <div className="mx-auto min-h-screen max-w-[1600px] px-4 py-4 md:px-6">
        <aside
          onMouseLeave={() => setActiveSection(null)}
          className="relative rounded-[1.5rem] border border-white/60 bg-ink px-1.5 py-2 text-white shadow-panel md:fixed md:left-6 md:top-1/2 md:w-[3.5rem] md:-translate-y-1/2 md:px-1.5 md:py-2"
        >
          <div className="flex w-8 flex-col items-center gap-1">
            {CONTROL_SECTIONS.map((section) => (
              <div key={section.title} className="relative flex items-center">
                <NavLink
                  to={section.items[0].path}
                  onMouseEnter={() => setActiveSection(section.title)}
                  onFocus={() => setActiveSection(section.title)}
                  ref={(element) => {
                    buttonRefs.current[section.title] = element;
                  }}
                  aria-label={`Open ${section.title}`}
                  className={`flex h-7 w-7 items-center justify-center rounded-lg text-[11px] font-semibold shadow-sm transition hover:scale-105 ${
                    section.color
                  } ${highlightedSection === section.title ? "ring-2 ring-white ring-offset-2 ring-offset-ink" : ""}`}
                  title={section.title}
                >
                  {section.rail}
                </NavLink>
              </div>
            ))}
          </div>
          {visibleSection ? (
            <div
              ref={flyoutRef}
              className="absolute left-full top-0 z-30 ml-3 hidden w-56 rounded-[1.5rem] border border-white/60 bg-ink/95 p-3.5 text-white shadow-panel backdrop-blur md:block"
              style={{ left: `${flyoutPosition.left}px`, top: `${flyoutPosition.top}px`, position: "fixed" }}
            >
              <div className="mb-3 flex items-center gap-2.5">
                <span className={`flex h-7 w-7 items-center justify-center rounded-lg text-[11px] font-semibold ${visibleSection.color}`}>
                  {visibleSection.rail}
                </span>
                <div>
                  <p className="text-[10px] uppercase tracking-[0.24em] text-white/60">CONTROL</p>
                  <NavLink to={visibleSection.items[0].path} className="font-serif text-lg leading-none text-white">
                    {visibleSection.title}
                  </NavLink>
                </div>
              </div>
              <nav className="space-y-1.5">
                {visibleSection.items.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    end={item.path === "/"}
                    className={({ isActive }) =>
                      `block rounded-xl px-3 py-2 text-sm font-medium transition ${
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
        </aside>
        <main className="pb-32 md:pl-[6.25rem]">
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
