import { useEffect, useState } from "react";
import { fetchInventoryStats, fetchWarehouseLoad } from "../api/client";
import KPIBar from "../components/KPIBar";
import LoadingSpinner from "../components/LoadingSpinner";
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

  if (loading) return <LoadingSpinner message="Running 52-week simulation..." />;
  if (error) return <div className="text-red-400 text-center py-16">Error: {error}</div>;

  const kpis = stats && {
    critical_skus: stats.understock_parts, high_risk_skus: stats.overstock_parts,
    avg_days_of_supply: stats.total_parts, supplier_reliability_pct: 0,
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Inventory Engine</h1>
        <p className="text-slate-400 text-sm mt-1">52-week over/understock simulation across {stats.total_parts} parts</p>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card label="Total Parts" value={stats.total_parts} color="text-blue-400" />
        <Card label="At Risk of Understock" value={stats.understock_parts} color="text-red-400" />
        <Card label="At Risk of Overstock" value={stats.overstock_parts} color="text-yellow-400" />
        <Card label="Annual Spend" value={`$${(stats.total_annual_spend / 1e6).toFixed(1)}M`} color="text-green-400" />
      </div>
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-4">Warehouse Pallet Load — Next 52 Weeks</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={load}>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
            <XAxis dataKey="week" tick={{ fill: "#94A3B8", fontSize: 12 }} />
            <YAxis tick={{ fill: "#94A3B8", fontSize: 12 }} />
            <Tooltip contentStyle={{ background: "#1E293B", border: "1px solid #334155", borderRadius: 8 }} />
            <Line type="monotone" dataKey="pallets" stroke="#3B82F6" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function Card({ label, value, color }) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
      <p className="text-slate-400 text-xs font-medium uppercase tracking-wide mb-1">{label}</p>
      <p className={`text-3xl font-bold font-mono ${color}`}>{value}</p>
    </div>
  );
}
