import { useEffect, useState } from "react";
import { fetchToday, fetchBriefing } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import { PageHeader, Stat } from "../components/ui";
import { useNavigate } from "react-router-dom";

export default function Today() {
  const [data, setData] = useState(null);
  const [brief, setBrief] = useState(null);
  const nav = useNavigate();

  useEffect(() => {
    fetchToday().then(setData).catch(() => {});
    fetchBriefing().then(setBrief).catch(() => {});
  }, []);

  if (!data) return <LoadingSpinner message="Building today's briefing..." />;

  return (
    <div className="space-y-6">
      <PageHeader title="Today" subtitle="Your daily supply-chain risk briefing" />

      {brief?.headline && (
        <div className="card p-5 border-l-4 border-l-brand-600">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-brand-50 text-brand-600 flex items-center justify-center text-sm font-semibold shrink-0">AI</div>
            <div>
              <p className="text-sm font-medium text-ink">{brief.headline}</p>
              <p className="text-xs text-ink-muted mt-0.5">Generated from live inventory & supplier data</p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-3 gap-4">
        <Stat label="Critical" value={data.critical} sub="action needed < 48 hrs" tone="critical" />
        <Stat label="High" value={data.high} sub="monitor this week" tone="high" />
        <Stat label="Exposure at Risk" value={`$${(data.dollars_at_risk / 1000).toFixed(1)}k`} sub="if unaddressed" tone="brand" />
      </div>

      <div>
        <h2 className="section-title mb-3">Action needed in &lt; 48 hours</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {data.cards.map((c) => (
            <div key={`${c.sku_id}-${c.site_id}`} className="card p-5 flex flex-col">
              <div className="flex items-center justify-between">
                <span className="chip chip-critical"><span className="chip-dot" />CRITICAL</span>
                <span className="text-xs text-ink-muted font-mono">{c.site_id}</span>
              </div>
              <div className="mt-3 font-semibold text-ink">{c.sku_name}</div>
              <div className="text-sm text-ink-soft mt-1">Buffer <span className="font-mono text-[#b42318]">{c.buffer_days}d</span> · <span className="font-mono">${c.dollars_at_risk.toLocaleString()}</span> at risk</div>
              <button onClick={() => nav(`/decision/${c.sku_id}/${c.site_id}`)} className="btn-primary mt-4 w-full">Resolve →</button>
            </div>
          ))}
          {data.cards.length === 0 && <p className="text-sm text-ink-muted">No critical risks right now. ✅</p>}
        </div>
      </div>
    </div>
  );
}
