const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function post(path, body) {
  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (networkErr) {
    throw new ApiError(
      "Can't reach the backend. Is the FastAPI server running on " + BASE_URL + "?",
      0
    );
  }

  let data;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const message =
      (data && (data.error || data.detail)) || `Request failed with status ${response.status}`;
    throw new ApiError(message, response.status);
  }

  return data;
}

export async function checkHealth() {
  const res = await fetch(`${BASE_URL}/api/health`);
  if (!res.ok) throw new ApiError("Health check failed", res.status);
  return res.json();
}

export const api = {
  summarize: (text, length) => post("/api/summarize", { text, length }),
  qa: (context, question) => post("/api/qa", { context, question }),
  generate: (prompt, content_type, tone) => post("/api/generate", { prompt, content_type, tone }),
  analyze: (text) => post("/api/analyze", { text }),
  suggest: (context) => post("/api/suggest", { context }),
};

export { ApiError };
