"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchMetrics } from "@/lib/api";
import { MetricsResponse } from "@/types";
import SummaryCard from "@/components/SummaryCard";
import MetricsChart from "@/components/MetricsChart";
import TimeRangeSelector from "@/components/TimeRangeSelector";
import ReloadButton from "@/components/ReloadButton";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";

export default function OverviewPage() {
  const [timeRange, setTimeRange] = useState("1h");
  const [data, setData] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchMetrics(timeRange);
      setData(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "データの取得に失敗しました"
      );
    } finally {
      setLoading(false);
    }
  }, [timeRange]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Overview</h1>
        <div className="flex items-center gap-3">
          <TimeRangeSelector value={timeRange} onChange={setTimeRange} />
          <ReloadButton onClick={loadData} loading={loading} />
        </div>
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} />}

      {!loading && !error && data && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <SummaryCard
              title="総リクエスト数"
              value={data.summary.totalRequests.toLocaleString()}
            />
            <SummaryCard
              title="エラー率"
              value={data.summary.errorRate.toFixed(1)}
              unit="%"
            />
            <SummaryCard
              title="平均レスポンス時間"
              value={data.summary.avgLatency.toFixed(1)}
              unit="ms"
            />
            <SummaryCard
              title="p95 レイテンシ"
              value={data.summary.p95Latency.toFixed(1)}
              unit="ms"
            />
          </div>

          <MetricsChart data={data.timeSeries} />
        </>
      )}
    </div>
  );
}
