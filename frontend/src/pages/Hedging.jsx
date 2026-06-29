import { useEffect, useState } from "react";
import { fetchHedgingScenario, fetchPriceForecast } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
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

  useEffect(() => { fetchPriceForecast("OIL_1").then(setFc).catch(() => {}); }, []);

  if (loading && !data) return <LoadingSpinner message="Running procurement scenario..." />;

  const chart = data.oils.map((o) => ({ name: o.oil_id, Hedged: o.hedged_cost, "Spot Only": o.spot_only_cost }));
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Hedging Planner</h1>
        <p className="text-slate-400 text-sm mt-1">Hedged vs spot-only procurement · {data.total_mt.toLocaleString()} MT · coverage {data.all_coverage_ok ? "on plan" : "below minimum"}</p>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card label="Amount Saved" value={`$${(data.amount_saved / 1e6).toFixed(2)}M`} c="text-green-400" />
        <Card label="Saved / Ton" value={`$${data.saved_per_ton}`} c="text-green-400" />
        <Card label="Hedged Total" value={`$${(data.hedged_total / 1e6).toFixed(1)}M`} c="text-blue-400" />
        <Card label="Spot Only" value={`$${(data.spot_total / 1e6).toFixed(1)}M`} c="text-slate-200" />
      </div>
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-slate-100">Strategy Split</h2>
          <span className="text-sm text-slate-400">S1 (front-loaded) {Math.round(s1*100)}% · S2 (systematic) {Math.round(s2*100)}%</span>
        </div>
        <input type="range" min="0" max="1" step="0.05" value={s1} onChange={(e) => setS1(+e.target.value)} className="w-full accent-blue-500" />
      </div>
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-4">Cost: Hedged vs Spot-Only</h2>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={chart}>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
            <XAxis dataKey="name" tick={{ fill: "#94A3B8", fontSize: 12 }} />
            <YAxis tick={{ fill: "#94A3B8", fontSize: 12 }} tickFormatter={(v) => `$${(v/1e6).toFixed(0)}M`} />
            <Tooltip contentStyle={{ background: "#1E293B", border: "1px solid #334155", borderRadius: 8 }} />
            <Legend />
            <Bar dataKey="Hedged" fill="#3B82F6" radius={[4,4,0,0]} />
            <Bar dataKey="Spot Only" fill="#64748B" radius={[4,4,0,0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-1">OIL_1 Price Forecast</h2>
        <p className="text-xs text-slate-500 mb-4">Monthly avg/min/max — Prophet when available, numpy trend+seasonality otherwise</p>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={fc}>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
            <XAxis dataKey="month" tick={{ fill: "#94A3B8", fontSize: 11 }} />
            <YAxis tick={{ fill: "#94A3B8", fontSize: 12 }} domain={["auto","auto"]} />
            <Tooltip contentStyle={{ background: "#1E293B", border: "1px solid #334155", borderRadius: 8 }} />
            <Line type="monotone" dataKey="avg" stroke="#3B82F6" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="max" stroke="#64748B" strokeWidth={1} dot={false} strokeDasharray="4 4" />
            <Line type="monotone" dataKey="min" stroke="#64748B" strokeWidth={1} dot={false} strokeDasharray="4 4" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function Card({ label, value, c }) {
  return <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
    <p className="text-slate-400 text-xs uppercase tracking-wide mb-1">{label}</p>
    <p className={`text-3xl font-bold font-mono ${c}`}>{value}</p></div>;
}
