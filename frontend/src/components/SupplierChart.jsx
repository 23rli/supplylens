import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

/** Props: { suppliers: array of supplier rows } */
export default function SupplierChart({ suppliers = [] }) {
  const data = suppliers.map((s) => ({
    name: s.supplier_name.replace(" Co", "").replace(" GmbH", "").replace(" Solutions", ""),
    rate: Math.round(s.on_time_delivery_rate * 100),
    incidents: s.incident_count_12m,
    tier: s.contract_tier,
  }));

  const barColor = (r) => (r >= 93 ? "#16a34a" : r >= 87 ? "#ca8a04" : "#d92d20");

  const TT = ({ active, payload, label }) => {
    if (!active || !payload?.length) return null;
    const d = payload[0].payload;
    return (
      <div className="bg-white border border-surface-border rounded-lg shadow-pop p-3 text-sm">
        <p className="font-semibold text-ink mb-1">{label}</p>
        <p className="text-ink-soft">On-time: <span className="font-mono text-ink">{d.rate}%</span></p>
        <p className="text-ink-soft">Incidents (12m): <span className={d.incidents > 0 ? "text-[#b54708]" : "text-[#067647]"}>{d.incidents}</span></p>
        <p className="text-ink-muted">Tier: {d.tier}</p>
      </div>
    );
  };

  return (
    <div className="card p-5">
      <h2 className="section-title mb-4">Supplier On-Time Delivery Rate</h2>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} layout="vertical" margin={{ left: 20, right: 30 }}>
          <XAxis type="number" domain={[70, 100]} tickFormatter={(v) => `${v}%`} tick={{ fill: "#8a94a6", fontSize: 12 }} />
          <YAxis type="category" dataKey="name" width={120} tick={{ fill: "#5b6678", fontSize: 12 }} />
          <Tooltip content={<TT />} cursor={{ fill: "#f6f8fb" }} />
          <Bar dataKey="rate" radius={[0, 4, 4, 0]}>
            {data.map((e, i) => <Cell key={i} fill={barColor(e.rate)} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p className="text-xs text-ink-muted mt-2">Green ≥93% · Amber 87–92% · Red &lt;87%</p>
    </div>
  );
}
