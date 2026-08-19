import { useState } from "react";
import { api, ApiError } from "../api/client";
import ResultPanel from "./ResultPanel";

const CONTENT_TYPES = [
  { value: "email", label: "Email" },
  { value: "blog_post", label: "Blog post" },
  { value: "social_post", label: "Social post" },
  { value: "outline", label: "Outline" },
  { value: "general", label: "General" },
];

export default function GenerateModule() {
  const [prompt, setPrompt] = useState("");
  const [contentType, setContentType] = useState("email");
  const [tone, setTone] = useState("professional");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const canSubmit = prompt.trim().length > 0 && !loading;

  async function handleSubmit(e) {
    e.preventDefault();
    if (!canSubmit) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.generate(prompt, contentType, tone);
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
        <h2>Generate content</h2>
        <p>Describe what you need. Pick a shape and a tone.</p>
      </header>

      <form onSubmit={handleSubmit} className="module__form">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g. Ask my team to move Friday's standup to Thursday because of the holiday…"
          rows={6}
        />
        <div className="module__controls">
          <label className="field">
            <span>Type</span>
            <select value={contentType} onChange={(e) => setContentType(e.target.value)}>
              {CONTENT_TYPES.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
          </label>
          <label className="field">
            <span>Tone</span>
            <input
              type="text"
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              placeholder="professional, casual, warm…"
            />
          </label>
          <button type="submit" disabled={!canSubmit}>
            {loading ? "Writing…" : "Generate"}
          </button>
        </div>
      </form>

      <ResultPanel loading={loading} error={error} result={result} />
    </div>
  );
}
