"use client";

import { useRouter } from "next/navigation";
import { EndpointMetrics } from "@/types";
import { endpointToSlug } from "@/lib/endpoints";

interface EndpointsTableProps {
  endpoints: EndpointMetrics[];
}

export default function EndpointsTable({ endpoints }: EndpointsTableProps) {
  const router = useRouter();

  if (endpoints.length === 0) {
    return (
      <p className="text-sm text-gray-500 py-4">
        表示するエンドポイントがありません
      </p>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              エンドポイント
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              リクエスト数
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              成功率 (%)
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              平均レイテンシ (ms)
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              p95 レイテンシ (ms)
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              エラー数
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {endpoints.map((ep) => (
            <tr
              key={ep.endpoint}
              onClick={() =>
                router.push(`/endpoints/${endpointToSlug(ep.endpoint)}/`)
              }
              className="hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                {ep.endpoint}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                {ep.requests.toLocaleString()}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                {ep.successRate.toFixed(1)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                {ep.avgLatency.toFixed(1)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                {ep.p95Latency.toFixed(1)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                {ep.errors.toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
