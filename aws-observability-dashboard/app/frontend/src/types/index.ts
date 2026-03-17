/** メトリクスサマリー（Overview サマリーカード用） */
export interface MetricsSummary {
  totalRequests: number;
  errorRate: number;
  avgLatency: number;
  p95Latency: number;
}

/** 時系列データポイント */
export interface TimeSeriesPoint {
  timestamp: string;
  requests: number;
  errors: number;
  avgLatency: number;
}

/** エンドポイント別メトリクス */
export interface EndpointMetrics {
  endpoint: string;
  requests: number;
  successRate: number;
  avgLatency: number;
  p95Latency: number;
  errors: number;
}

/** GET /metrics レスポンス */
export interface MetricsResponse {
  summary: MetricsSummary;
  timeSeries: TimeSeriesPoint[];
  endpoints: EndpointMetrics[];
  timeRange: string;
}

/** ログエントリ */
export interface LogEntry {
  timestamp: string;
  level: string;
  endpoint: string;
  requestId: string;
  message: string;
  statusCode?: number;
  durationMs?: number;
  errorCode?: string;
}

/** GET /logs レスポンス */
export interface LogsResponse {
  logs: LogEntry[];
  count: number;
  timeRange: string;
}
