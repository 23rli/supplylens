/** Props: { siteData: [{ site_id, critical_count, high_count, medium_count, low_count }] } */
export default function RiskHeatmap({ siteData = [] }) {
  const levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"];
  const key = { CRITICAL: "critical_count", HIGH: "high_count", MEDIUM: "medium_count", LOW: "low_count" };
  const cell = {
    CRITICAL: (n) => n > 0 ? "bg-[#fef3f2] border-[#fecdca] text-[#b42318]" : "bg-surface-sunken border-surface-border text-ink-muted",
    HIGH: (n) => n > 0 ? "bg-[#fffaeb] border-[#fedf89] text-[#b54708]" : "bg-surface-sunken border-surface-border text-ink-muted",
    MEDIUM: (n) => n > 0 ? "bg-[#fffbeb] border-[#fde68a] text-[#854a0e]" : "bg-surface-sunken border-surface-border text-ink-muted",
    LOW: (n) => n > 0 ? "bg-[#ecfdf3] border-[#abefc6] text-[#067647]" : "bg-surface-sunken border-surface-border text-ink-muted",
  };
  return (
    <div className="card p-5">
      <h2 className="section-title mb-4">Risk Distribution by Site</h2>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr><th className="pb-3 text-left text-xs text-ink-muted uppercase tracking-wide">Site</th>
              {levels.map((l) => <th key={l} className="pb-3 text-center text-xs text-ink-muted uppercase tracking-wide">{l}</th>)}
            </tr>
          </thead>
          <tbody>
            {siteData.map((site) => (
              <tr key={site.site_id}>
                <td className="py-2.5 pr-4 text-sm font-semibold text-ink font-mono">{site.site_id}</td>
                {levels.map((level) => {
                  const n = site[key[level]] || 0;
                  return (
                    <td key={level} className="py-2.5 text-center">
                      <span className={`inline-flex items-center justify-center w-10 h-10 rounded-lg border text-sm font-bold font-mono ${cell[level](n)}`}>{n}</span>
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
