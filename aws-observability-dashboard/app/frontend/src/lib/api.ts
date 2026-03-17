import { MetricsResponse, LogsResponse } from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";

export async function fetchMetrics(
  range: string,
  endpoint?: string
): Promise<MetricsResponse> {
  const params = new URLSearchParams({ range });
  if (endpoint) {
    params.set("endpoint", endpoint);
  }
  const res = await fetch(`${API_BASE_URL}/metrics?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`メトリクス取得に失敗しました (${res.status})`);
  }
  return res.json();
}

export async function fetchLogs(
  range: string,
  level?: string,
  endpoint?: string
): Promise<LogsResponse> {
  const params = new URLSearchParams({ range });
  if (level) {
    params.set("level", level);
  }
  if (endpoint) {
    params.set("endpoint", endpoint);
  }
  const res = await fetch(`${API_BASE_URL}/logs?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`ログ取得に失敗しました (${res.status})`);
  }
  return res.json();
}
