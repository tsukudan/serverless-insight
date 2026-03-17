"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { fetchMetrics, fetchLogs } from "@/lib/api";
import { MetricsResponse, LogEntry } from "@/types";
import { ENDPOINT_SLUGS, slugToEndpoint } from "@/lib/endpoints";
import SummaryCard from "@/components/SummaryCard";
import MetricsChart from "@/components/MetricsChart";
import TimeRangeSelector from "@/components/TimeRangeSelector";
import ReloadButton from "@/components/ReloadButton";
import LoadingSpinner from "@/components/LoadingSpinner";
import ErrorMessage from "@/components/ErrorMessage";

export const dynamicParams = false;

export async function generateStaticParams() {
  return Object.keys(ENDPOINT_SLUGS).map((slug) => ({ id: slug }));
}

export default function EndpointDetailPage() {
  const params = useParams();
  const slug = params.id as string;
  const endpointName = slugToEndpoint(slug);

  const [timeRange, setTimeRange] = useState("1h");
  const [data, setData] = useState<MetricsResponse | null>(null);
  const [errorLogs, setErrorLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    if (!endpointName) return;
    setLoading(true);
    setError(null);
    try {
      const [metricsResult, logsResult] = await Promise.all([
        fetchMetrics(timeRange, endpointName),
        fetchLogs(timeRange, "ERROR", endpointName),
      ]);
      setData(metricsResult);
      setErrorLogs(logsResult.logs.slice(0, 20));
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "データの取得に失敗しました"
      );
    } finally {
      setLoading(false);
    }
  }, [timeRange, endpointName]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  if (!endpointName) {
    return (
      <div className="space-y-4">
        <ErrorMessage message="不明なエンドポイントです" />
        <Link
          href="/endpoints/"
          className="text-sm text-blue-600 hover:underline"
        >
          ← Endpoints に戻る
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Link
            href="/endpoints/"
            className="text-sm text-blue-600 hover:underline"
          >
            ← Endpoints に戻る
          </Link>
          <h1 className="mt-1 text-2xl font-bold text-gray-900">
            {endpointName}
          </h1>
        </div>
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
              title="リクエスト数"
              value={data.summary.totalRequests.toLocaleString()}
            />
            <SummaryCard
              title="成功率"
              value={(100 - data.summary.errorRate).toFixed(1)}
              unit="%"
            />
            <SummaryCard
              title="平均レイテンシ"
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

          <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-sm font-medium text-gray-700">
                最新エラーログ
              </h3>
            </div>
            {errorLogs.length === 0 ? (
              <p className="px-6 py-4 text-sm text-gray-500">
                エラーログはありません
              </p>
            ) : (
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      タイムスタンプ
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      メッセージ
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ステータス
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {errorLogs.map((log) => (
                    <tr key={log.requestId}>
                      <td className="px-6 py-3 whitespace-nowrap text-sm text-gray-500">
                        {new Date(log.timestamp).toLocaleString("ja-JP")}
                      </td>
                      <td className="px-6 py-3 text-sm text-gray-900">
                        {log.message}
                      </td>
                      <td className="px-6 py-3 whitespace-nowrap text-sm text-right text-red-600">
                        {log.statusCode ?? "-"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </div>
  );
}
