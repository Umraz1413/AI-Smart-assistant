import { useEffect, useState } from "react";
import { checkHealth } from "../api/client";

export default function StatusBadge() {
  const [status, setStatus] = useState("checking"); // checking | ok | misconfigured | offline

  useEffect(() => {
    let cancelled = false;
    checkHealth()
      .then((data) => {
        if (cancelled) return;
        setStatus(data.api_key_configured ? "ok" : "misconfigured");
      })
      .catch(() => {
        if (!cancelled) setStatus("offline");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const copy = {
    checking: "Checking backend…",
    ok: "Backend connected",
    misconfigured: "Backend up, API key missing",
    offline: "Backend unreachable",
  }[status];

  return (
    <div className={`status-badge status-badge--${status}`}>
      <span className="status-badge__dot" />
      {copy}
    </div>
  );
}
