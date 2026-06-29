import RiskBadge from "./RiskBadge";

/**
 * Props: { risks: array of risk summary rows, title: string, limit: number }
 * Renders a table of SKUs with risk scores and recommended actions.
 */
export default function RiskTable({ risks = [], title = "Top Risks", limit }) {
  const rows = limit ? risks.slice(0, limit) : risks;

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-700">
        <h2 className="text-lg font-semibold text-slate-100">{title}</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700">
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wide">SKU</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wide">Site</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wide">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wide">Stock</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wide">Days Supply</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wide">Buffer</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wide">Risk</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wide">Recommended Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {rows.map((row, idx) => (
              <tr key={`${row.sku_id}-${row.site_id}-${idx}`} className="hover:bg-slate-700/30 transition-colors">
                <td className="px-6 py-4">
                  <div className="text-sm font-medium text-slate-100">{row.sku_name}</div>
                  <div className="text-xs text-slate-500 font-mono">{row.sku_id}</div>
                </td>
                <td className="px-6 py-4 text-sm text-slate-300 font-mono">{row.site_id}</td>
                <td className="px-6 py-4 text-sm text-slate-400">{row.category}</td>
                <td className="px-6 py-4 text-sm text-slate-300 font-mono">{row.current_stock?.toLocaleString()}</td>
                <td className="px-6 py-4 text-sm font-mono font-semibold text-slate-100">{row.days_of_supply}d</td>
                <td className="px-6 py-4">
                  <span className={`text-sm font-mono font-semibold ${row.buffer_days < 0 ? "text-red-400" : "text-slate-300"}`}>
                    {row.buffer_days}d
                  </span>
                </td>
                <td className="px-6 py-4"><RiskBadge level={row.risk_level} /></td>
                <td className="px-6 py-4 text-xs text-slate-400 max-w-xs">{row.recommended_action}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length === 0 && (
          <div className="text-center py-12 text-slate-500">No SKUs match the current filters.</div>
        )}
      </div>
    </div>
  );
}
