interface SummaryCardProps {
  title: string;
  value: string | number;
  unit?: string;
}

export default function SummaryCard({ title, value, unit }: SummaryCardProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <p className="text-sm font-medium text-gray-500">{title}</p>
      <div className="mt-2 flex items-baseline">
        <span className="text-3xl font-bold text-gray-900">{value}</span>
        {unit && (
          <span className="ml-1 text-sm text-gray-500">{unit}</span>
        )}
      </div>
    </div>
  );
}
