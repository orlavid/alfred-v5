import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { KeyboardEvent, PropsWithChildren, useEffect, useLayoutEffect, useRef, useState } from "react";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { CONTROL_SECTIONS, findNavigationEntry } from "@/navigation";

type AppShellProps = PropsWithChildren<{
  askQuery: string;
  onAskQueryChange: (value: string) => void;
}>;

const FLYOUT_SAFE_MARGIN = 16;
const DEFAULT_FLYOUT_HEIGHT = 280;
const RAIL_TOP_OFFSET = 88;

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
  const [flyoutPosition, setFlyoutPosition] = useState({ left: 96, top: FLYOUT_SAFE_MARGIN });
  const navigate = useNavigate();
  const location = useLocation();
  const activeEntry = findNavigationEntry(location.pathname);
  const highlightedSection = activeEntry?.section.title;
  const buttonRefs = useRef<Record<string, HTMLAnchorElement | null>>({});
  const flyoutRef = useRef<HTMLDivElement | null>(null);

  function submitAsk() {
    navigate("/ask-alfred");
  }

  function closeFlyout() {
    setActiveSection(null);
  }

  function handleShellKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") {
      closeFlyout();
    }
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
        left: anchorRect.right + 14,
        top: getViewportSafeFlyoutTop(anchorRect.top + anchorRect.height / 2, flyoutHeight, window.innerHeight),
      });
    };

    updatePosition();
    window.addEventListener("resize", updatePosition);
    window.addEventListener("scroll", updatePosition, { passive: true });
    return () => {
      window.removeEventListener("resize", updatePosition);
      window.removeEventListener("scroll", updatePosition);
    };
  }, [activeSection]);

  useEffect(() => {
    if (!activeSection) {
      return;
    }

    const handleEscape = (event: globalThis.KeyboardEvent) => {
      if (event.key === "Escape") {
        closeFlyout();
      }
    };

    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [activeSection]);

  const visibleSection = activeSection ? CONTROL_SECTIONS.find((section) => section.title === activeSection) : null;

  return (
    <div className="min-h-screen bg-canvas text-ink" onKeyDown={handleShellKeyDown}>
      <div className="mx-auto min-h-screen max-w-[1600px] px-4 py-4 md:px-6">
        <div
          className="hidden md:block"
          onMouseLeave={closeFlyout}
        >
          <aside
            aria-label="CONTROL navigation"
            className="fixed left-6 top-[88px] z-30 rounded-[1.5rem] border border-white/70 bg-ink/96 px-2 py-2 text-white shadow-panel backdrop-blur"
            style={{ top: `${RAIL_TOP_OFFSET}px` }}
          >
            <nav className="flex flex-col items-center gap-1.5" aria-label="CONTROL rail">
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
                    aria-expanded={activeSection === section.title}
                    className={`flex h-9 w-9 items-center justify-center rounded-xl text-xs font-semibold shadow-sm transition duration-150 hover:-translate-y-0.5 ${
                      section.color
                    } ${highlightedSection === section.title ? "ring-2 ring-white ring-offset-2 ring-offset-ink" : ""}`}
                    title={section.title}
                  >
                    {section.rail}
                  </NavLink>
                </div>
              ))}
            </nav>
          </aside>
          {visibleSection ? (
            <div
              ref={flyoutRef}
              className="fixed z-40 hidden w-60 rounded-[1.5rem] border border-ink/15 bg-white/96 p-3.5 text-ink shadow-panel backdrop-blur md:block"
              style={{ left: `${flyoutPosition.left}px`, top: `${flyoutPosition.top}px` }}
              onMouseEnter={() => setActiveSection(visibleSection.title)}
            >
              <div className="mb-3 flex items-center gap-2.5 border-b border-ink/10 pb-3">
                <span className={`flex h-8 w-8 items-center justify-center rounded-xl text-xs font-semibold ${visibleSection.color}`}>
                  {visibleSection.rail}
                </span>
                <div>
                  <p className="text-[10px] uppercase tracking-[0.24em] text-ink/45">CONTROL</p>
                  <NavLink to={visibleSection.items[0].path} className="font-serif text-lg leading-none text-ink">
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
                        isActive ? "bg-ink text-white" : "text-ink/75 hover:bg-ink/5 hover:text-ink"
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
        <main className="pb-32 md:pl-[6.75rem]">
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
