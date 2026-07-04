"use client";

import { useEffect, useState } from "react";

type BackendState = "checking" | "online" | "offline";

type HealthResponse = {
  status: string;
  service: string;
};

const HEALTH_URL = "http://127.0.0.1:8000/health";

export default function BackendStatus() {
  const [backendState, setBackendState] = useState<BackendState>("checking");
  const [serviceName, setServiceName] = useState("Waiting for backend health");

  useEffect(() => {
    let shouldUpdate = true;

    async function checkBackendHealth() {
      try {
        const response = await fetch(HEALTH_URL, {
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error("Backend health check failed.");
        }

        const data = (await response.json()) as HealthResponse;

        if (shouldUpdate) {
          setBackendState("online");
          setServiceName(data.service || "DevDesk Agent backend");
        }
      } catch {
        if (shouldUpdate) {
          setBackendState("offline");
          setServiceName("Backend service unavailable");
        }
      }
    }

    checkBackendHealth();

    return () => {
      shouldUpdate = false;
    };
  }, []);

  const statusText =
    backendState === "checking"
      ? "Checking..."
      : backendState === "online"
        ? "Backend Online"
        : "Backend Offline";

  const indicatorClass =
    backendState === "checking"
      ? "bg-amber-500"
      : backendState === "online"
        ? "bg-emerald-500"
        : "bg-rose-500";

  const statusClass =
    backendState === "checking"
      ? "text-amber-700"
      : backendState === "online"
        ? "text-emerald-700"
        : "text-rose-700";

  return (
    <section
      aria-label="Backend connection status"
      className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
    >
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold text-slate-950">
            Backend connection
          </p>
          <p className="mt-1 text-sm text-slate-500">{serviceName}</p>
        </div>

        <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-2">
          <span
            aria-hidden="true"
            className={`h-2.5 w-2.5 rounded-full ${indicatorClass}`}
          />
          <span className={`text-sm font-medium ${statusClass}`}>
            {statusText}
          </span>
        </div>
      </div>
    </section>
  );
}
