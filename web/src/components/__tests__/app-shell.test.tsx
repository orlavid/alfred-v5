import { MemoryRouter } from "react-router-dom";
import { fireEvent, render, screen } from "@testing-library/react";
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
  expect(screen.getAllByText("C").length).toBeGreaterThan(0);
  expect(screen.getAllByText("O").length).toBeGreaterThan(0);
  expect(screen.getByText("N")).toBeInTheDocument();
  expect(screen.getByText("T")).toBeInTheDocument();
  expect(screen.getByText("R")).toBeInTheDocument();
  expect(screen.getByText("L")).toBeInTheDocument();
  expect(screen.getByLabelText("Breadcrumb")).toBeInTheDocument();
  expect(screen.getByPlaceholderText("Ask: What should I do today?")).toBeInTheDocument();

  expect(screen.queryByText("Command")).not.toBeInTheDocument();

  fireEvent.mouseEnter(screen.getByLabelText("Open Command"));

  expect(screen.getByText("Command")).toBeInTheDocument();
  expect(screen.getByText("Daily Brief")).toBeInTheDocument();
  expect(screen.queryByText("Projects")).not.toBeInTheDocument();

  fireEvent.mouseEnter(screen.getByLabelText("Open Objectives"));

  expect(screen.getByText("Objectives")).toBeInTheDocument();
  expect(screen.getByText("Projects")).toBeInTheDocument();
});
