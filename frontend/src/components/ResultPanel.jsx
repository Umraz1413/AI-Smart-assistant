export default function ResultPanel({ loading, error, result }) {
  if (loading) {
    return (
      <div className="readout readout--loading" role="status" aria-live="polite">
        <span className="pulse-dot" aria-hidden="true" />
        Thinking…
      </div>
    );
  }

  if (error) {
    return (
      <div className="readout readout--error" role="alert">
        <strong>Something went wrong.</strong>
        <p>{error}</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="readout readout--empty">
        Output will appear here once you run this module.
      </div>
    );
  }

  return (
    <div className="readout">
      <pre className="readout__text">{result.result}</pre>
      <div className="readout__meta">
        <span>{result.model}</span>
        {result.input_tokens != null && (
          <span>
            {result.input_tokens} in / {result.output_tokens} out tokens
          </span>
        )}
      </div>
    </div>
  );
}
