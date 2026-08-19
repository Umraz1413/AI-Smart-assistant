import { useState } from "react";
import { api, ApiError } from "../api/client";
import ResultPanel from "./ResultPanel";

export default function SummarizeModule() {
  const [text, setText] = useState("");
  const [length, setLength] = useState("medium");
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
      const res = await api.summarize(text, length);
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
        <h2>Summarize</h2>
        <p>Paste notes, an article, or a transcript. Get the essentials back.</p>
      </header>

      <form onSubmit={handleSubmit} className="module__form">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste text to summarize…"
          rows={10}
        />
        <div className="module__controls">
          <label className="field">
            <span>Length</span>
            <select value={length} onChange={(e) => setLength(e.target.value)}>
              <option value="short">Short</option>
              <option value="medium">Medium</option>
              <option value="detailed">Detailed</option>
            </select>
          </label>
          <button type="submit" disabled={!canSubmit}>
            {loading ? "Summarizing…" : "Summarize"}
          </button>
        </div>
      </form>

      <ResultPanel loading={loading} error={error} result={result} />
    </div>
  );
}
