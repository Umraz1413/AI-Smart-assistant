import { useState } from "react";
import { api, ApiError } from "../api/client";
import ResultPanel from "./ResultPanel";

export default function QAModule() {
  const [context, setContext] = useState("");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const canSubmit = context.trim().length > 0 && question.trim().length > 0 && !loading;

  async function handleSubmit(e) {
    e.preventDefault();
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.qa(context, question);
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
        <h2>Ask a question</h2>
        <p>Give it source material, then ask anything about it.</p>
      </header>

      <form onSubmit={handleSubmit} className="module__form">
        <textarea
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="Paste the source material (document, notes, email thread)…"
          rows={7}
        />
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What do you want to know?"
        />
        <div className="module__controls">
          <button type="submit" disabled={!canSubmit}>
            {loading ? "Thinking…" : "Ask"}
          </button>
        </div>
      </form>

      <ResultPanel loading={loading} error={error} result={result} />
    </div>
  );
}
