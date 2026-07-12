import { MemoryRouter } from "react-router-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import { AppShell, getViewportSafeFlyoutTop } from "@/components/AppShell";

test("renders executive navigation shell", () => {
  render(
    <MemoryRouter initialEntries={["/daily-brief"]}>
      <AppShell askQuery="What should I do today?" onAskQueryChange={() => undefined}>
        <div>Child Content</div>
      </AppShell>
    </MemoryRouter>,
  );

  expect(screen.getByText("Child Content")).toBeInTheDocument();
  expect(screen.getAllByText("C").length).toBeGreaterThan(0);
  expect(screen.getAllByText("O").length).toBeGreaterThan(0);
  expect(screen.getByText("N")).toBeInTheDocument();
  expect(screen.getByText("T")).toBeInTheDocument();
  expect(screen.getByText("R")).toBeInTheDocument();
  expect(screen.getByText("L")).toBeInTheDocument();
  expect(screen.getByLabelText("Breadcrumb")).toBeInTheDocument();
  expect(screen.getByPlaceholderText("Ask: What should I do today?")).toBeInTheDocument();

  fireEvent.mouseEnter(screen.getByLabelText("Open Command"));

  expect(screen.getAllByText("Command").length).toBeGreaterThan(0);
  expect(screen.getAllByText("Daily Brief").length).toBeGreaterThan(0);
  expect(screen.queryByText("Projects")).not.toBeInTheDocument();

  fireEvent.mouseEnter(screen.getByLabelText("Open Objectives"));

  expect(screen.getAllByText("Objectives").length).toBeGreaterThan(0);
  expect(screen.getByText("Projects")).toBeInTheDocument();

  fireEvent.mouseEnter(screen.getByLabelText("Open Library"));

  expect(screen.getByText("Library")).toBeInTheDocument();
  expect(screen.getByText("Prompt Library")).toBeInTheDocument();
});

test("clamps flyout position inside viewport margins", () => {
  expect(getViewportSafeFlyoutTop(40, 240, 900)).toBe(16);
  expect(getViewportSafeFlyoutTop(850, 240, 900)).toBe(644);
  expect(getViewportSafeFlyoutTop(400, 240, 900)).toBe(280);
});

test("shows snapshot status and supports manual refresh", () => {
  const onRefreshNow = vi.fn();

  render(
    <MemoryRouter>
      <AppShell
        askQuery="What should I do today?"
        onAskQueryChange={() => undefined}
        onRefreshNow={onRefreshNow}
        snapshot={{
          snapshot_version: "snap-1",
          build_timestamp: "2026-07-12T19:00:00Z",
          source_vault_timestamp: "2026-07-12T18:00:00Z",
          deployed_commit: "abc123",
          certification_status: "GREEN",
          last_successful_refresh: "2026-07-12T19:00:00Z",
          last_failed_refresh: "2026-07-12T18:30:00Z",
          last_failed_reason: "transient test failure",
          refresh_in_progress: false,
          current_snapshot_version: "snap-1",
        }}
      >
        <div>Child Content</div>
      </AppShell>
    </MemoryRouter>,
  );

  expect(screen.getByText(/Snapshot:/)).toBeInTheDocument();
  expect(screen.getByText(/Last Success:/)).toBeInTheDocument();
  expect(screen.getByText(/Last Failure:/)).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Refresh now" }));
  expect(onRefreshNow).toHaveBeenCalledTimes(1);
});
