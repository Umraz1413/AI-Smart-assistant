import { useState } from "react";
import { api, ApiError } from "../api/client";
import ResultPanel from "./ResultPanel";

export default function SuggestModule() {
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const canSubmit = context.trim().length > 0 && !loading;

  async function handleSubmit(e) {
    e.preventDefault();
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.suggest(context);
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
        <h2>Suggest next actions</h2>
        <p>Drop in your task list or a messy brain-dump. Get a prioritized plan.</p>
      </header>

      <form onSubmit={handleSubmit} className="module__form">
        <textarea
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="e.g. Todo: finish deck for Thursday, reply to Sam about budget, book flights, review PR…"
          rows={8}
        />
        <div className="module__controls">
          <button type="submit" disabled={!canSubmit}>
            {loading ? "Prioritizing…" : "Get suggestions"}
          </button>
        </div>
      </form>

      <ResultPanel loading={loading} error={error} result={result} />
    </div>
  );
}
