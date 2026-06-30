import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchPartDetail, fetchPartDemand } from "../api/client";
import { StatsRowSkeleton, ChartSkeleton } from "../components/ui";
import { PageHeader, Stat, Card } from "../components/ui";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from "recharts";

export default function PartDetail() {
  const { partNumber } = useParams();
  const [p, setP] = useState(null);
  const [dem, setDem] = useState(null);
  const nav = useNavigate();
  useEffect(() => {
    fetchPartDetail(partNumber).then(setP);
    fetchPartDemand(partNumber).then(setDem).catch(() => {});
  }, [partNumber]);
  if (!p) return <div className="space-y-6"><StatsRowSkeleton count={4} /><ChartSkeleton height={320} /></div>;

  const data = p.products.map((v, w) => ({ week: w, products: v }));
  return (
    <div className="space-y-6">
      <PageHeader title={`${p.part_number} \u00b7 ${p.description}`}
        subtitle={`${p.vendor_name} \u00b7 lead ${p.lead_time_weeks}w \u00b7 EOQ ${p.eoq} \u00b7 safety ${p.safety_stock}`}
        actions={<button onClick={() => nav("/inventory/parts")} className="btn-outline">&larr; Back to Parts</button>} />
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Stat label="Weeks Understocked" value={p.weeks_understocked} tone="critical" />
        <Stat label="Weeks Overstocked" value={p.weeks_overstocked} tone="warn" />
        <Stat label="Restock Point" value={p.restock_point} tone="brand" />
        <Stat label="Overstock Point" value={p.overstock_point} />
      </div>
      <Card title="Projected On-Hand - 52 Weeks">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={data}>
            <CartesianGrid stroke="#e5e9f0" strokeDasharray="3 3" />
            <XAxis dataKey="week" tick={{ fill: "#8a94a6", fontSize: 12 }} />
            <YAxis tick={{ fill: "#8a94a6", fontSize: 12 }} />
            <Tooltip contentStyle={{ background: "#fff", border: "1px solid #e5e9f0", borderRadius: 8 }} />
            <ReferenceLine y={p.overstock_point} stroke="#ca8a04" strokeDasharray="4 4" />
            <ReferenceLine y={p.safety_stock} stroke="#d92d20" strokeDasharray="4 4" />
            <Line type="monotone" dataKey="products" stroke="#4f46e5" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
        <p className="text-xs text-ink-muted mt-2">Amber = overstock point \u00b7 Red = safety stock</p>
      </Card>

      {dem && (
        <Card title="Demand Forecast & Seasonality"
          action={dem.is_seasonal
            ? <span className="chip chip-high"><span className="chip-dot" />Seasonal +{dem.peak_pct}% (wk {dem.peak_week})</span>
            : <span className="chip chip-low"><span className="chip-dot" />Stable demand</span>}>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
            <Stat label="Avg Demand / Week" value={dem.avg_weekly} tone="brand" />
            <Stat label="Seasonal Peak" value={`+${dem.peak_pct}%`} tone="warn" />
            <Stat label="Forecast Runway" value={`${dem.seasonal_runway_weeks}w`} tone={dem.runway_risk ? "critical" : "good"} />
            <Stat label="Flat-Avg Runway" value={`${dem.flat_runway_weeks}w`} />
          </div>
          {dem.runway_risk && (
            <p className="text-sm text-[#b42318] mb-3">
              Seasonal demand exhausts stock {dem.flat_runway_weeks - dem.seasonal_runway_weeks} week(s) sooner than a flat average suggests - reorder earlier.
            </p>
          )}
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={dem.weeks}>
              <CartesianGrid stroke="#e5e9f0" strokeDasharray="3 3" />
              <XAxis dataKey="week" tick={{ fill: "#8a94a6", fontSize: 12 }} />
              <YAxis tick={{ fill: "#8a94a6", fontSize: 12 }} />
              <Tooltip contentStyle={{ background: "#fff", border: "1px solid #e5e9f0", borderRadius: 8 }} />
              <ReferenceLine y={dem.avg_weekly} stroke="#8a94a6" strokeDasharray="4 4" />
              <Line type="monotone" dataKey="demand" stroke="#0ea5e9" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-xs text-ink-muted mt-2">Projected weekly demand vs average (dashed). Forecast-adjusted runway accounts for seasonal peaks.</p>
        </Card>
      )}
    </div>
  );
}
