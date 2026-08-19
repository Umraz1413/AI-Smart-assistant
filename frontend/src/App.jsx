import { useState } from "react";
import StatusBadge from "./components/StatusBadge";
import SummarizeModule from "./components/SummarizeModule";
import QAModule from "./components/QAModule";
import GenerateModule from "./components/GenerateModule";
import AnalyzeModule from "./components/AnalyzeModule";
import SuggestModule from "./components/SuggestModule";

const MODULES = [
  { id: "summarize", label: "Summarize", Component: SummarizeModule },
  { id: "qa", label: "Ask", Component: QAModule },
  { id: "generate", label: "Generate", Component: GenerateModule },
  { id: "analyze", label: "Analyze", Component: AnalyzeModule },
  { id: "suggest", label: "Suggest", Component: SuggestModule },
];

export default function App() {
  const [activeId, setActiveId] = useState(MODULES[0].id);
  const active = MODULES.find((m) => m.id === activeId);
  const ActiveComponent = active.Component;

  return (
    <div className="app">
      <header className="app__header">
        <div className="brand">
          <span className="brand__mark" aria-hidden="true" />
          <div>
            <h1>AI Smart Assistant</h1>
            <p>Your working console for text, built on Gemini</p>
          </div>
        </div>
        <StatusBadge />
      </header>

      <div className="app__body">
        <nav className="module-nav" aria-label="Modules">
          {MODULES.map((m) => (
            <button
              key={m.id}
              className={`module-nav__item ${m.id === activeId ? "is-active" : ""}`}
              onClick={() => setActiveId(m.id)}
              aria-current={m.id === activeId}
            >
              {m.label}
            </button>
          ))}
        </nav>

        <main className="app__main">
          <ActiveComponent />
        </main>
      </div>
    </div>
  );
}
