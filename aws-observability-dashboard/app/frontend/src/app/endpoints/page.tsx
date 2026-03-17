"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchMetrics } from "@/lib/api";
import { MetricsResponse } from "@/types";
import EndpointsTable from "@/components/EndpointsTable";
import TimeRangeSelector from "@/components/TimeRangeSelector";
import ReloadButton from "@/components/ReloadButton";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";

export default function EndpointsPage() {
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
        <h1 className="text-2xl font-bold text-gray-900">Endpoints</h1>
        <div className="flex items-center gap-3">
          <TimeRangeSelector value={timeRange} onChange={setTimeRange} />
          <ReloadButton onClick={loadData} loading={loading} />
        </div>
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} />}

      {!loading && !error && data && (
        <EndpointsTable endpoints={data.endpoints} />
      )}
    </div>
  );
}
