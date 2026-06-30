import { useEffect, useState } from "react";
import { fetchInventoryStats, fetchWarehouseLoad } from "../api/client";
import { StatsRowSkeleton, ChartSkeleton } from "../components/ui";
import { PageHeader, Stat, Card } from "../components/ui";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function InventoryOverview() {
  const [stats, setStats] = useState(null);
  const [load, setLoad] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([fetchInventoryStats(), fetchWarehouseLoad()])
      .then(([s, l]) => { setStats(s); setLoad(l); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="space-y-6"><StatsRowSkeleton count={4} /><ChartSkeleton height={300} /></div>;
  if (error) return <div className="text-[#b42318] text-center py-16">Error: {error}</div>;

  return (
    <div className="space-y-6">
      <PageHeader title="Inventory Overview" subtitle={`52-week over/understock simulation across ${stats.total_parts} parts`} />
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Stat label="Total Parts" value={stats.total_parts} tone="brand" />
        <Stat label="Understock Risk" value={stats.understock_parts} tone="critical" />
        <Stat label="Overstock Risk" value={stats.overstock_parts} tone="warn" />
        <Stat label="Annual Spend" value={`$${(stats.total_annual_spend / 1e6).toFixed(1)}M`} tone="good" />
      </div>
      <Card title="Warehouse Pallet Load â€” Next 52 Weeks">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={load}>
            <CartesianGrid stroke="#e5e9f0" strokeDasharray="3 3" />
            <XAxis dataKey="week" tick={{ fill: "#8a94a6", fontSize: 12 }} />
            <YAxis tick={{ fill: "#8a94a6", fontSize: 12 }} />
            <Tooltip contentStyle={{ background: "#fff", border: "1px solid #e5e9f0", borderRadius: 8 }} />
            <Line type="monotone" dataKey="pallets" stroke="#4f46e5" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );
}
