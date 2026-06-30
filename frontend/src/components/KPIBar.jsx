import { Stat } from "./ui";

/** Props: { stats: { critical_skus, high_risk_skus, avg_days_of_supply, supplier_reliability_pct } } */
export default function KPIBar({ stats }) {
  if (!stats) return null;
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <Stat label="Critical Risk SKUs" value={stats.critical_skus} sub="stockout before next delivery"
        tone={stats.critical_skus > 0 ? "critical" : "good"} />
      <Stat label="High Risk SKUs" value={stats.high_risk_skus} sub="within 1.5× lead time"
        tone={stats.high_risk_skus > 3 ? "high" : "neutral"} />
      <Stat label="Avg Days of Supply" value={`${stats.avg_days_of_supply}d`} sub="across all SKU-site pairs" tone="brand" />
      <Stat label="Supplier Reliability" value={`${stats.supplier_reliability_pct}%`} sub="on-time delivery rate"
        tone={stats.supplier_reliability_pct >= 90 ? "good" : "warn"} />
    </div>
  );
}
