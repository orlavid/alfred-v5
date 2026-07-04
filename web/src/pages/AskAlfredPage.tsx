import { useMemo, useState } from "react";
import { SectionCard } from "@/components/SectionCard";
import { StatusPill } from "@/components/StatusPill";
import type { DashboardPayload } from "@/types";

function normalise(value: string) {
  return value.trim().toLowerCase();
}

export function AskAlfredPage({ data }: { data: DashboardPayload }) {
  const [query, setQuery] = useState(data.ask_alfred.questions[0] ?? "");

  const selected = useMemo(() => {
    const exact = data.ask_alfred.responses.find((item) => normalise(item.question) === normalise(query));
    if (exact) {
      return exact;
    }
    return data.ask_alfred.responses[0];
  }, [data.ask_alfred.responses, query]);

  return (
    <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
      <SectionCard title="Ask Alfred" kicker="Question Panel">
        <label className="block text-sm font-medium text-ink/80" htmlFor="question-input">
          Recommended executive questions
        </label>
        <input
          id="question-input"
          className="mt-3 w-full rounded-2xl border border-ink/15 bg-white/80 px-4 py-3 text-sm text-ink outline-none transition focus:border-accent"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Type one of the recommended questions"
        />
        <div className="mt-4 flex flex-wrap gap-2">
          {data.ask_alfred.questions.map((question) => (
            <button
              key={question}
              type="button"
              onClick={() => setQuery(question)}
              className="rounded-full border border-ink/10 bg-white/70 px-4 py-2 text-sm text-ink transition hover:border-accent/40"
            >
              {question}
            </button>
          ))}
        </div>
        <p className="mt-4 text-sm leading-6 text-ink/65">
          This v1 panel is read-only and resolves against precomputed Dashboard API responses.
        </p>
      </SectionCard>
      <SectionCard title={selected.question} kicker="Executive Answer" action={<StatusPill value={selected.confidence} />}>
        <div className="space-y-5">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Answer</p>
            <ul className="mt-3 space-y-2 text-sm leading-6 text-ink/80">
              {selected.executive_answer.map((item) => (
                <li key={item}>- {item}</li>
              ))}
            </ul>
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Supporting Evidence</p>
            <ul className="mt-3 space-y-2 text-sm leading-6 text-ink/80">
              {selected.supporting_evidence.map((item) => (
                <li key={item}>- {item}</li>
              ))}
            </ul>
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-accent">Recommended Next Actions</p>
            <ul className="mt-3 space-y-2 text-sm leading-6 text-ink/80">
              {selected.recommended_next_actions.map((item) => (
                <li key={item}>- {item}</li>
              ))}
            </ul>
          </div>
        </div>
      </SectionCard>
    </div>
  );
}
