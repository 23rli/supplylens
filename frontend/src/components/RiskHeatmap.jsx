/**
 * Props: { siteData: array of { site_id, critical_count, high_count, medium_count, low_count } }
 * Renders a site × risk level grid.
 */
export default function RiskHeatmap({ siteData = [] }) {
  const levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"];
  const countKey = { CRITICAL: "critical_count", HIGH: "high_count", MEDIUM: "medium_count", LOW: "low_count" };
  const cellColor = {
    CRITICAL: (n) => n > 0 ? "bg-red-500/30 border-red-500/40 text-red-300" : "bg-slate-700/30 border-slate-700 text-slate-600",
    HIGH: (n) => n > 2 ? "bg-orange-500/30 border-orange-500/40 text-orange-300" : n > 0 ? "bg-orange-500/15 border-orange-500/25 text-orange-400" : "bg-slate-700/30 border-slate-700 text-slate-600",
    MEDIUM: (n) => n > 0 ? "bg-yellow-500/20 border-yellow-500/30 text-yellow-300" : "bg-slate-700/30 border-slate-700 text-slate-600",
    LOW: (n) => n > 0 ? "bg-green-500/15 border-green-500/25 text-green-400" : "bg-slate-700/30 border-slate-700 text-slate-600",
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
      <h2 className="text-lg font-semibold text-slate-100 mb-4">Risk Distribution by Site</h2>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              <th className="pb-3 text-left text-xs text-slate-400 uppercase tracking-wide">Site</th>
              {levels.map((l) => (
                <th key={l} className="pb-3 text-center text-xs text-slate-400 uppercase tracking-wide">{l}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/30">
            {siteData.map((site) => (
              <tr key={site.site_id}>
                <td className="py-3 pr-4 text-sm font-semibold text-slate-200 font-mono">{site.site_id}</td>
                {levels.map((level) => {
                  const count = site[countKey[level]] || 0;
                  return (
                    <td key={level} className="py-3 text-center">
                      <span className={`inline-flex items-center justify-center w-10 h-10 rounded-lg border text-sm font-bold font-mono ${cellColor[level](count)}`}>
                        {count}
                      </span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
