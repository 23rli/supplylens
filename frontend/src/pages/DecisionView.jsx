import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { explainDecision, executeAction } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";

export default function DecisionView() {
  const { sku, site } = useParams();
  const [d, setD] = useState(null);
  const [msg, setMsg] = useState("");
  useEffect(() => { explainDecision(sku, site).then(setD); }, [sku, site]);
  if (!d) return <LoadingSpinner message="Analyzing..." />;

  const run = async (a) => {
    setMsg("Executing...");
    try { const r = await executeAction(a.type, { sku, site, label: a.label, cost: a.cost, benefit: a.benefit });
      setMsg(`${a.type} started — ETA ${r.eta_days}d (action #${r.action_id})`); }
    catch { setMsg("Execution failed"); }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">{sku} @ {site}</h1>
        <p className="text-slate-400 text-sm mt-1">{d.narrative}</p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
          <h2 className="text-sm uppercase text-slate-400 mb-3">Context</h2>
          <p className="text-slate-300 text-sm">Risk: <span className="text-red-400 font-semibold">{d.risk}</span></p>
          <p className="text-slate-300 text-sm">Buffer: {d.buffer_days}d</p>
          <p className="text-slate-300 text-sm">$ at risk: ${d.dollars_at_risk.toLocaleString()}</p>
        </div>
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
          <h2 className="text-sm uppercase text-slate-400 mb-3">Scenarios</h2>
          {d.simulations.map((s) => <p key={s.mode} className="text-slate-300 text-sm">{s.mode}: ${s.cost.toLocaleString()}</p>)}
          <p className="text-xs text-green-400 mt-3">{d.confidence}</p>
        </div>
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
          <h2 className="text-sm uppercase text-slate-400 mb-3">Ranked Actions</h2>
          {d.actions.map((a) => (
            <div key={a.type} className={`mb-2 p-3 rounded-lg border ${a.recommended ? "border-blue-500/50 bg-blue-500/10" : "border-slate-700"}`}>
              <div className="text-slate-100 text-sm font-medium">{a.label}</div>
              <div className="text-xs text-slate-400">cost ${a.cost.toLocaleString()} · benefit ${a.benefit.toLocaleString()} · {Math.round(a.confidence*100)}%</div>
              <button onClick={() => run(a)} className="mt-2 text-xs bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded">Execute</button>
            </div>
          ))}
          {msg && <p className="text-xs text-green-400 mt-2">{msg}</p>}
        </div>
      </div>
    </div>
  );
}
