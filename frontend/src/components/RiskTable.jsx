import { RiskChip } from "./ui";

/**
 * Props: { risks: array of risk summary rows, title, limit }
 */
export default function RiskTable({ risks = [], title = "Top Risks", limit }) {
  const rows = limit ? risks.slice(0, limit) : risks;
  return (
    <div className="card overflow-hidden">
      <div className="px-5 py-3.5 border-b border-surface-border">
        <h2 className="section-title">{title}</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-surface-sunken">
            <tr className="border-b border-surface-border">
              <th className="th">SKU</th><th className="th">Site</th><th className="th">Category</th>
              <th className="th">Stock</th><th className="th">Days Supply</th><th className="th">Buffer</th>
              <th className="th">Risk</th><th className="th">Recommended Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-border">
            {rows.map((row, idx) => (
              <tr key={`${row.sku_id}-${row.site_id}-${idx}`} className="hover:bg-surface-sunken/60">
                <td className="td">
                  <div className="font-medium text-ink">{row.sku_name}</div>
                  <div className="text-xs text-ink-muted font-mono">{row.sku_id}</div>
                </td>
                <td className="td font-mono">{row.site_id}</td>
                <td className="td">{row.category}</td>
                <td className="td font-mono">{row.current_stock?.toLocaleString()}</td>
                <td className="td font-mono font-semibold text-ink">{row.days_of_supply}d</td>
                <td className="td">
                  <span className={`font-mono font-semibold ${row.buffer_days < 0 ? "text-[#b42318]" : "text-ink-soft"}`}>{row.buffer_days}d</span>
                </td>
                <td className="td"><RiskChip level={row.risk_level} /></td>
                <td className="td text-xs max-w-xs">{row.recommended_action}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length === 0 && <div className="text-center py-12 text-ink-muted text-sm">No SKUs match the current filters.</div>}
      </div>
    </div>
  );
}
