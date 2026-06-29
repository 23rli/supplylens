/**
 * Props: { stats: { critical_skus, high_risk_skus, avg_days_of_supply, supplier_reliability_pct } }
 * Renders 4 KPI cards in a row.
 */
export default function KPIBar({ stats }) {
  if (!stats) return null;

  const kpis = [
    {
      label: "Critical Risk SKUs",
      value: stats.critical_skus,
      subtext: "stockout before next delivery",
      color: stats.critical_skus > 0 ? "text-red-400" : "text-green-400",
      bg: stats.critical_skus > 0 ? "border-red-500/30" : "border-green-500/30",
    },
    {
      label: "High Risk SKUs",
      value: stats.high_risk_skus,
      subtext: "within 1.5x lead time window",
      color: stats.high_risk_skus > 3 ? "text-orange-400" : "text-slate-100",
      bg: "border-slate-700",
    },
    {
      label: "Avg Days of Supply",
      value: `${stats.avg_days_of_supply}d`,
      subtext: "across all SKU-site pairs",
      color: "text-blue-400",
      bg: "border-slate-700",
    },
    {
      label: "Supplier Reliability",
      value: `${stats.supplier_reliability_pct}%`,
      subtext: "on-time delivery rate (active suppliers)",
      color: stats.supplier_reliability_pct >= 90 ? "text-green-400" : "text-yellow-400",
      bg: "border-slate-700",
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {kpis.map((kpi) => (
        <div key={kpi.label} className={`bg-slate-800 border ${kpi.bg} rounded-xl p-5`}>
          <p className="text-slate-400 text-xs font-medium uppercase tracking-wide mb-1">{kpi.label}</p>
          <p className={`text-3xl font-bold font-mono ${kpi.color} mb-1`}>{kpi.value}</p>
          <p className="text-slate-500 text-xs">{kpi.subtext}</p>
        </div>
      ))}
    </div>
  );
}
