"use client";

interface TimeRangeSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

const TIME_RANGES = ["1h", "6h", "24h", "7d"];

export default function TimeRangeSelector({
  value,
  onChange,
}: TimeRangeSelectorProps) {
  return (
    <div className="flex space-x-1">
      {TIME_RANGES.map((range) => (
        <button
          key={range}
          onClick={() => onChange(range)}
          className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
            value === range
              ? "bg-blue-600 text-white"
              : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
          }`}
        >
          {range}
        </button>
      ))}
    </div>
  );
}
