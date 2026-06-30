import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { explainDecision, executeAction } from "../api/client";
import { PageHeader, Card, RiskChip, Skeleton, StatsRowSkeleton } from "../components/ui";
import { useToast } from "../components/Toast";

export default function DecisionView() {
  const { sku, site } = useParams();
  const [d, setD] = useState(null);
  const [running, setRunning] = useState(null);
  const nav = useNavigate();
  const toast = useToast();
  useEffect(() => { explainDecision(sku, site).then(setD); }, [sku, site]);

  const run = async (a) => {
    setRunning(a.type);
    try {
      const r = await executeAction(a.type, { sku, site, label: a.label, cost: a.cost, benefit: a.benefit });
      toast(`${a.type} started for ${sku} - ETA ${r.eta_days}d (action #${r.action_id})`, "success");
    } catch { toast("Execution failed. Please try again.", "error"); }
    finally { setRunning(null); }
  };

  if (!d) return (
    <div className="space-y-6">
      <PageHeader title={`${sku} \u00b7 ${site}`} subtitle="Analyzing decision options..." />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {[0, 1, 2].map((i) => <div key={i} className="card p-5 space-y-3"><Skeleton className="h-4 w-24" /><Skeleton className="h-4 w-full" /><Skeleton className="h-4 w-2/3" /></div>)}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <PageHeader title={`${sku} \u00b7 ${site}`} subtitle={d.narrative}
        actions={<button onClick={() => nav("/today")} className="btn-outline">&larr; Back to Today</button>} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <Card title="Context">
          <dl className="space-y-2.5 text-sm">
            <Row k="Risk level" v={<RiskChip level={d.risk} />} />
            <Row k="Buffer" v={<span className="font-mono text-[#b42318]">{d.buffer_days}d</span>} />
            <Row k="Exposure at risk" v={<span className="font-mono text-ink">${d.dollars_at_risk.toLocaleString()}</span>} />
          </dl>
        </Card>

        <Card title="Scenarios">
          <div className="space-y-2.5">
            {d.simulations.map((s) => (
              <div key={s.mode} className="flex items-center justify-between text-sm">
                <span className="text-ink-soft capitalize">{s.mode.replace("_", " ")}</span>
                <span className="font-mono font-semibold text-ink">${s.cost.toLocaleString()}</span>
              </div>
            ))}
          </div>
          {d.confidence && <p className="text-xs text-[#067647] mt-4 pt-3 border-t border-surface-border">{d.confidence}</p>}
        </Card>

        <Card title="Recommended Actions">
          <div className="space-y-2.5">
            {d.actions.map((a) => (
              <div key={a.type} className={`p-3 rounded-lg border ${a.recommended ? "border-brand-600 bg-brand-50" : "border-surface-border"}`}>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-ink">{a.label}</span>
                  {a.recommended && <span className="text-[10px] font-semibold text-brand-700 bg-white border border-brand-600 rounded px-1.5 py-0.5">BEST</span>}
                </div>
                <div className="text-xs text-ink-muted mt-1">cost ${a.cost.toLocaleString()} &middot; benefit ${a.benefit.toLocaleString()} &middot; {Math.round(a.confidence * 100)}% confidence</div>
                <button onClick={() => run(a)} disabled={running} className="btn-primary mt-2.5 text-xs px-3 py-1.5 disabled:opacity-50">
                  {running === a.type ? "Executing..." : "Execute"}
                </button>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

function Row({ k, v }) {
  return <div className="flex items-center justify-between"><dt className="text-ink-soft">{k}</dt><dd>{v}</dd></div>;
}
