import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { explainDecision, executeAction } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import { PageHeader, Card, RiskChip } from "../components/ui";

export default function DecisionView() {
  const { sku, site } = useParams();
  const [d, setD] = useState(null);
  const [msg, setMsg] = useState("");
  const nav = useNavigate();
  useEffect(() => { explainDecision(sku, site).then(setD); }, [sku, site]);
  if (!d) return <LoadingSpinner message="Analyzing decision options..." />;

  const run = async (a) => {
    setMsg("Executing...");
    try {
      const r = await executeAction(a.type, { sku, site, label: a.label, cost: a.cost, benefit: a.benefit });
      setMsg(`${a.type} started — ETA ${r.eta_days}d (action #${r.action_id})`);
    } catch { setMsg("Execution failed"); }
  };

  return (
    <div className="space-y-6">
      <PageHeader title={`${sku} · ${site}`} subtitle={d.narrative}
        actions={<button onClick={() => nav("/today")} className="btn-outline">← Back to Today</button>} />

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

        <Card title="Recommended Actions" className="lg:row-span-1">
          <div className="space-y-2.5">
            {d.actions.map((a) => (
              <div key={a.type} className={`p-3 rounded-lg border ${a.recommended ? "border-brand-600 bg-brand-50" : "border-surface-border"}`}>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-ink">{a.label}</span>
                  {a.recommended && <span className="text-[10px] font-semibold text-brand-700 bg-white border border-brand-600 rounded px-1.5 py-0.5">BEST</span>}
                </div>
                <div className="text-xs text-ink-muted mt-1">cost ${a.cost.toLocaleString()} · benefit ${a.benefit.toLocaleString()} · {Math.round(a.confidence * 100)}% confidence</div>
                <button onClick={() => run(a)} className="btn-primary mt-2.5 text-xs px-3 py-1.5">Execute</button>
              </div>
            ))}
          </div>
          {msg && <p className="text-xs text-[#067647] mt-3">{msg}</p>}
        </Card>
      </div>
    </div>
  );
}

function Row({ k, v }) {
  return <div className="flex items-center justify-between"><dt className="text-ink-soft">{k}</dt><dd>{v}</dd></div>;
}
