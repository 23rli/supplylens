import { useEffect, useState } from "react";
import { fetchHedgingScenario, fetchPriceForecast } from "../api/client";
import { StatsRowSkeleton, ChartSkeleton } from "../components/ui";
import { PageHeader, Stat, Card } from "../components/ui";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend, LineChart, Line } from "recharts";

export default function Hedging() {
  const [s1, setS1] = useState(0.75);
  const [data, setData] = useState(null);
  const [fc, setFc] = useState([]);
  const [loading, setLoading] = useState(true);
  const s2 = +(1 - s1).toFixed(2);

  useEffect(() => {
    setLoading(true);
    fetchHedgingScenario({ s1, s2 }).then(setData).finally(() => setLoading(false));
  }, [s1]);

  useEffect(() => { fetchPriceForecast("STEEL").then(setFc).catch(() => {}); }, []);

  if (loading && !data) return <div className="space-y-6"><StatsRowSkeleton count={4} /><ChartSkeleton height={260} /></div>;

  const chart = data.oils.map((o) => ({ name: o.oil_id, Hedged: o.hedged_cost, "Spot Only": o.spot_only_cost }));
  return (
    <div className="space-y-6">
      <PageHeader title="Hedging Planner"
        subtitle={`Commodity hedged vs spot-only procurement Ã‚Â· ${data.total_mt.toLocaleString()} MT Ã‚Â· coverage ${data.all_coverage_ok ? "on plan" : "below minimum"}`} />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Stat label="Amount Saved" value={`$${(data.amount_saved / 1e6).toFixed(2)}M`} tone="good" />
        <Stat label="Saved / Ton" value={`$${data.saved_per_ton}`} tone="good" />
        <Stat label="Hedged Total" value={`$${(data.hedged_total / 1e6).toFixed(1)}M`} tone="brand" />
        <Stat label="Spot Only" value={`$${(data.spot_total / 1e6).toFixed(1)}M`} />
      </div>

      <Card title="Strategy Split" action={<span className="text-sm text-ink-soft">S1 (front-loaded) {Math.round(s1 * 100)}% Ã‚Â· S2 (systematic) {Math.round(s2 * 100)}%</span>}>
        <input type="range" min="0" max="1" step="0.05" value={s1} onChange={(e) => setS1(+e.target.value)} className="w-full accent-brand-600" />
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <Card title="Cost: Hedged vs Spot-Only">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={chart}>
              <CartesianGrid stroke="#e5e9f0" strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fill: "#8a94a6", fontSize: 12 }} />
              <YAxis tick={{ fill: "#8a94a6", fontSize: 12 }} tickFormatter={(v) => `$${(v / 1e6).toFixed(0)}M`} />
              <Tooltip contentStyle={{ background: "#fff", border: "1px solid #e5e9f0", borderRadius: 8 }} cursor={{ fill: "#f6f8fb" }} />
              <Legend />
              <Bar dataKey="Hedged" fill="#4f46e5" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Spot Only" fill="#94a3b8" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
        <Card title="STEEL Price Forecast">
          <p className="text-xs text-ink-muted mb-3 -mt-1">Monthly avg/min/max Ã¢â‚¬â€ Prophet when available, numpy fallback otherwise</p>
          <ResponsiveContainer width="100%" height={224}>
            <LineChart data={fc}>
              <CartesianGrid stroke="#e5e9f0" strokeDasharray="3 3" />
              <XAxis dataKey="month" tick={{ fill: "#8a94a6", fontSize: 11 }} />
              <YAxis tick={{ fill: "#8a94a6", fontSize: 12 }} domain={["auto", "auto"]} />
              <Tooltip contentStyle={{ background: "#fff", border: "1px solid #e5e9f0", borderRadius: 8 }} />
              <Line type="monotone" dataKey="avg" stroke="#4f46e5" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="max" stroke="#94a3b8" strokeWidth={1} dot={false} strokeDasharray="4 4" />
              <Line type="monotone" dataKey="min" stroke="#94a3b8" strokeWidth={1} dot={false} strokeDasharray="4 4" />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      </div>
    </div>
  );
}
