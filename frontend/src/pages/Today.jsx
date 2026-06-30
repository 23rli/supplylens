import { useEffect, useState } from "react";
import { fetchToday, fetchBriefing, askAI } from "../api/client";
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
              <p className="text-xs text-ink-muted mt-0.5">Generated from live inventory &amp; supplier data</p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-3 gap-4">
        <Stat label="Critical" value={data.critical} sub="action needed < 48 hrs" tone="critical" />
        <Stat label="High" value={data.high} sub="monitor this week" tone="high" />
        <Stat label="Exposure at Risk" value={`$${(data.dollars_at_risk / 1000).toFixed(1)}k`} sub="if unaddressed" tone="brand" />
      </div>

      <AskAI />

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
              <div className="text-sm text-ink-soft mt-1">Buffer <span className="font-mono text-[#b42318]">{c.buffer_days}d</span> &middot; <span className="font-mono">${c.dollars_at_risk.toLocaleString()}</span> at risk</div>
              <button onClick={() => nav(`/decision/${c.sku_id}/${c.site_id}`)} className="btn-primary mt-4 w-full">Resolve &rarr;</button>
            </div>
          ))}
          {data.cards.length === 0 && <p className="text-sm text-ink-muted">No critical risks right now.</p>}
        </div>
      </div>
    </div>
  );
}

const SUGGESTED = [
  "What's our biggest stockout risk right now?",
  "Which supplier should I be most concerned about?",
  "What should I prioritize this week?",
];

function AskAI() {
  const [q, setQ] = useState("");
  const [ans, setAns] = useState(null);
  const [busy, setBusy] = useState(false);

  const run = async (question) => {
    const text = question || q.trim();
    if (!text || busy) return;
    setBusy(true); setAns(null); setQ(text);
    try { const r = await askAI(text); setAns(r.answer); }
    catch { setAns("Couldn't reach the AI service."); }
    finally { setBusy(false); }
  };

  return (
    <div className="card p-5">
      <h2 className="section-title mb-3">Ask SupplyLens AI</h2>
      <div className="flex gap-2">
        <input className="input flex-1" value={q} onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && run()} placeholder="Ask anything about risk, suppliers, or what to do next..." />
        <button className="btn-primary" onClick={() => run()} disabled={busy || !q.trim()}>{busy ? "Thinking..." : "Ask"}</button>
      </div>
      <div className="flex flex-wrap gap-2 mt-3">
        {SUGGESTED.map((s) => (
          <button key={s} onClick={() => run(s)} className="text-xs text-ink-soft bg-surface-sunken border border-surface-border rounded-full px-3 py-1 hover:border-brand-500 hover:text-ink">{s}</button>
        ))}
      </div>
      {busy && <p className="text-sm text-ink-muted mt-3">Analyzing live data...</p>}
      {ans && <div className="mt-4 text-sm text-ink leading-relaxed border-t border-surface-border pt-3 whitespace-pre-wrap">{ans}</div>}
    </div>
  );
}
