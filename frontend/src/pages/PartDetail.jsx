import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchPartDetail } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from "recharts";

export default function PartDetail() {
  const { partNumber } = useParams();
  const [p, setP] = useState(null);
  useEffect(() => { fetchPartDetail(partNumber).then(setP); }, [partNumber]);
  if (!p) return <LoadingSpinner message="Simulating..." />;

  const data = p.products.map((v, w) => ({ week: w, products: v }));
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">{p.part_number} — {p.description}</h1>
        <p className="text-slate-400 text-sm mt-1">{p.vendor_name} · lead {p.lead_time_weeks}w · EOQ {p.eoq} · safety {p.safety_stock}</p>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Stat label="Weeks Understocked" value={p.weeks_understocked} c="text-red-400" />
        <Stat label="Weeks Overstocked" value={p.weeks_overstocked} c="text-yellow-400" />
        <Stat label="Restock Point" value={p.restock_point} c="text-blue-400" />
        <Stat label="Overstock Point" value={p.overstock_point} c="text-slate-200" />
      </div>
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-4">Projected On-Hand — 52 Weeks</h2>
        <ResponsiveContainer width="100%" height={340}>
          <LineChart data={data}>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
            <XAxis dataKey="week" tick={{ fill: "#94A3B8", fontSize: 12 }} />
            <YAxis tick={{ fill: "#94A3B8", fontSize: 12 }} />
            <Tooltip contentStyle={{ background: "#1E293B", border: "1px solid #334155", borderRadius: 8 }} />
            <ReferenceLine y={p.overstock_point} stroke="#EAB308" strokeDasharray="4 4" />
            <ReferenceLine y={p.safety_stock} stroke="#EF4444" strokeDasharray="4 4" />
            <Line type="monotone" dataKey="products" stroke="#3B82F6" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
        <p className="text-xs text-slate-500 mt-2">Yellow = overstock point · Red = safety stock</p>
      </div>
    </div>
  );
}

function Stat({ label, value, c }) {
  return <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
    <p className="text-slate-400 text-xs uppercase tracking-wide mb-1">{label}</p>
    <p className={`text-3xl font-bold font-mono ${c}`}>{value}</p></div>;
}
