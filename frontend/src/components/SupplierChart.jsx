import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

/**
 * Props: { suppliers: array of supplier rows }
 * Renders a horizontal bar chart of supplier on-time delivery rates.
 */
export default function SupplierChart({ suppliers = [] }) {
  const data = suppliers.map((s) => ({
    name: s.supplier_name.replace(" Co", "").replace(" GmbH", "").replace(" Solutions", ""),
    rate: Math.round(s.on_time_delivery_rate * 100),
    incidents: s.incident_count_12m,
    tier: s.contract_tier,
  }));

  const getBarColor = (rate) => {
    if (rate >= 93) return "#22C55E";
    if (rate >= 87) return "#EAB308";
    return "#EF4444";
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (!active || !payload?.length) return null;
    const d = payload[0].payload;
    return (
      <div className="bg-slate-700 border border-slate-600 rounded-lg p-3 text-sm">
        <p className="text-slate-100 font-semibold mb-1">{label}</p>
        <p className="text-slate-300">On-time rate: <span className="text-white font-mono">{d.rate}%</span></p>
        <p className="text-slate-300">Incidents (12m): <span className={d.incidents > 0 ? "text-orange-400" : "text-green-400"}>{d.incidents}</span></p>
        <p className="text-slate-400">Contract tier: {d.tier}</p>
      </div>
    );
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
      <h2 className="text-lg font-semibold text-slate-100 mb-4">Supplier On-Time Delivery Rate</h2>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} layout="vertical" margin={{ left: 20, right: 30 }}>
          <XAxis type="number" domain={[70, 100]} tickFormatter={(v) => `${v}%`}
            tick={{ fill: "#94A3B8", fontSize: 12 }} />
          <YAxis type="category" dataKey="name" width={120}
            tick={{ fill: "#CBD5E1", fontSize: 12 }} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="rate" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => (
              <Cell key={index} fill={getBarColor(entry.rate)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p className="text-xs text-slate-500 mt-2">Green ≥93% · Yellow 87–92% · Red &lt;87%</p>
    </div>
  );
}
