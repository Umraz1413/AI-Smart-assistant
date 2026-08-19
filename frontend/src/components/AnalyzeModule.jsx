import { useState } from "react";
import { api, ApiError } from "../api/client";
import ResultPanel from "./ResultPanel";

export default function AnalyzeModule() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const canSubmit = text.trim().length > 0 && !loading;

  async function handleSubmit(e) {
    e.preventDefault();
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.analyze(text);
      setResult(res);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Unexpected error.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="module">
      <header className="module__header">
        <h2>Analyze document</h2>
        <p>Get a structured breakdown: key points, tone, entities, and gaps.</p>
      </header>

      <form onSubmit={handleSubmit} className="module__form">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste a document, report, or long email to analyze…"
          rows={10}
        />
        <div className="module__controls">
          <button type="submit" disabled={!canSubmit}>
            {loading ? "Analyzing…" : "Analyze"}
          </button>
        </div>
      </form>

      <ResultPanel loading={loading} error={error} result={result} />
    </div>
  );
}
