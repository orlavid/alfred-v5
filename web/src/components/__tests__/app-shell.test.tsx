import { MemoryRouter } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { AppShell } from "@/components/AppShell";

test("renders executive navigation shell", () => {
  render(
    <MemoryRouter>
      <AppShell askQuery="What should I do today?" onAskQueryChange={() => undefined}>
        <div>Child Content</div>
      </AppShell>
    </MemoryRouter>,
  );

  expect(screen.getByText("Executive UI")).toBeInTheDocument();
  expect(screen.getByRole("link", { name: "Dashboard" })).toBeInTheDocument();
  expect(screen.getByRole("link", { name: "Daily Brief" })).toBeInTheDocument();
  expect(screen.getByPlaceholderText("Ask: What should I do today?")).toBeInTheDocument();
  expect(screen.getByText("Child Content")).toBeInTheDocument();
});
