import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchPartDetail } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import { PageHeader, Stat, Card } from "../components/ui";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from "recharts";

export default function PartDetail() {
  const { partNumber } = useParams();
  const [p, setP] = useState(null);
  const nav = useNavigate();
  useEffect(() => { fetchPartDetail(partNumber).then(setP); }, [partNumber]);
  if (!p) return <LoadingSpinner message="Simulating..." />;

  const data = p.products.map((v, w) => ({ week: w, products: v }));
  return (
    <div className="space-y-6">
      <PageHeader title={`${p.part_number} · ${p.description}`}
        subtitle={`${p.vendor_name} · lead ${p.lead_time_weeks}w · EOQ ${p.eoq} · safety ${p.safety_stock}`}
        actions={<button onClick={() => nav("/inventory/parts")} className="btn-outline">← Back to Parts</button>} />
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Stat label="Weeks Understocked" value={p.weeks_understocked} tone="critical" />
        <Stat label="Weeks Overstocked" value={p.weeks_overstocked} tone="warn" />
        <Stat label="Restock Point" value={p.restock_point} tone="brand" />
        <Stat label="Overstock Point" value={p.overstock_point} />
      </div>
      <Card title="Projected On-Hand — 52 Weeks">
        <ResponsiveContainer width="100%" height={340}>
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
        <p className="text-xs text-ink-muted mt-2">Amber = overstock point · Red = safety stock</p>
      </Card>
    </div>
  );
}
