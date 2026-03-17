import { TimeSeriesPoint } from "@/types";

interface MetricsChartProps {
  data: TimeSeriesPoint[];
}

function formatTimestamp(ts: string): string {
  const d = new Date(ts);
  return `${d.getHours().toString().padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}`;
}

export default function MetricsChart({ data }: MetricsChartProps) {
  if (data.length === 0) {
    return (
      <p className="text-sm text-gray-500 py-4">表示するデータがありません</p>
    );
  }

  const maxRequests = Math.max(...data.map((d) => d.requests), 1);
  const maxLatency = Math.max(...data.map((d) => d.avgLatency), 1);

  const width = 800;
  const height = 240;
  const padding = { top: 20, right: 60, bottom: 30, left: 50 };
  const chartW = width - padding.left - padding.right;
  const chartH = height - padding.top - padding.bottom;

  const xStep = data.length > 1 ? chartW / (data.length - 1) : 0;

  const requestsPath = data
    .map((d, i) => {
      const x = padding.left + i * xStep;
      const y = padding.top + chartH - (d.requests / maxRequests) * chartH;
      return `${i === 0 ? "M" : "L"}${x},${y}`;
    })
    .join(" ");

  const latencyPath = data
    .map((d, i) => {
      const x = padding.left + i * xStep;
      const y = padding.top + chartH - (d.avgLatency / maxLatency) * chartH;
      return `${i === 0 ? "M" : "L"}${x},${y}`;
    })
    .join(" ");

  const labelInterval = Math.max(1, Math.floor(data.length / 6));

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <h3 className="text-sm font-medium text-gray-700 mb-4">メトリクス推移</h3>

      <div className="flex items-center gap-4 mb-3 text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <span className="inline-block w-3 h-0.5 bg-blue-500" />
          リクエスト数
        </span>
        <span className="flex items-center gap-1">
          <span className="inline-block w-3 h-0.5 bg-emerald-500" />
          平均レイテンシ (ms)
        </span>
      </div>

      <svg
        viewBox={`0 0 ${width} ${height}`}
        className="w-full h-auto"
        role="img"
        aria-label="メトリクス推移グラフ"
      >
        {/* Y軸グリッド */}
        {[0, 0.25, 0.5, 0.75, 1].map((ratio) => {
          const y = padding.top + chartH - ratio * chartH;
          return (
            <g key={ratio}>
              <line
                x1={padding.left}
                y1={y}
                x2={padding.left + chartW}
                y2={y}
                stroke="#e5e7eb"
                strokeWidth={1}
              />
              <text
                x={padding.left - 6}
                y={y + 4}
                textAnchor="end"
                className="text-[10px] fill-gray-400"
              >
                {Math.round(maxRequests * ratio)}
              </text>
              <text
                x={padding.left + chartW + 6}
                y={y + 4}
                textAnchor="start"
                className="text-[10px] fill-gray-400"
              >
                {Math.round(maxLatency * ratio)}
              </text>
            </g>
          );
        })}

        {/* X軸ラベル */}
        {data.map((d, i) =>
          i % labelInterval === 0 ? (
            <text
              key={i}
              x={padding.left + i * xStep}
              y={height - 6}
              textAnchor="middle"
              className="text-[10px] fill-gray-400"
            >
              {formatTimestamp(d.timestamp)}
            </text>
          ) : null
        )}

        {/* リクエスト数 折れ線 */}
        <path
          d={requestsPath}
          fill="none"
          stroke="#3b82f6"
          strokeWidth={2}
        />

        {/* 平均レイテンシ 折れ線 */}
        <path
          d={latencyPath}
          fill="none"
          stroke="#10b981"
          strokeWidth={2}
        />
      </svg>
    </div>
  );
}
