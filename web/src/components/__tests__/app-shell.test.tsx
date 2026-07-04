import { MemoryRouter } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { AppShell } from "@/components/AppShell";

test("renders executive navigation shell", () => {
  render(
    <MemoryRouter initialEntries={["/daily-brief"]}>
      <AppShell askQuery="What should I do today?" onAskQueryChange={() => undefined}>
        <div>Child Content</div>
      </AppShell>
    </MemoryRouter>,
  );

  expect(screen.getByText("Child Content")).toBeInTheDocument();
  expect(screen.getByText("Command")).toBeInTheDocument();
  expect(screen.getByText("Daily Brief")).toBeInTheDocument();
  expect(screen.getByLabelText("Breadcrumb")).toBeInTheDocument();
  expect(screen.getByPlaceholderText("Ask: What should I do today?")).toBeInTheDocument();
});
