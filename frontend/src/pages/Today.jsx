import { useEffect, useState } from "react";
import { fetchToday, fetchBriefing } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
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
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Today</h1>
        <p className="text-slate-400 text-sm mt-1">{brief?.headline || "Risk briefing"}</p>
      </div>
      <div className="grid grid-cols-3 gap-4">
        <Card label="Critical" value={data.critical} c="text-red-400" />
        <Card label="High" value={data.high} c="text-orange-400" />
        <Card label="$ at Risk" value={`$${(data.dollars_at_risk/1000).toFixed(1)}k`} c="text-green-400" />
      </div>
      <div>
        <h2 className="text-lg font-semibold text-slate-200 mb-3">Action needed in &lt; 48 hrs</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {data.cards.map((c) => (
            <div key={`${c.sku_id}-${c.site_id}`} className="bg-slate-800 border border-red-500/30 rounded-xl p-5">
              <div className="text-xs text-red-400 font-semibold uppercase">CRITICAL · {c.site_id}</div>
              <div className="text-slate-100 font-semibold mt-1">{c.sku_name}</div>
              <div className="text-slate-400 text-sm mt-1">Buffer {c.buffer_days}d · ${c.dollars_at_risk.toLocaleString()} at risk</div>
              <button onClick={() => nav(`/decision/${c.sku_id}/${c.site_id}`)}
                className="mt-4 w-full bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium py-2 rounded-lg">
                Fix it →
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function Card({ label, value, c }) {
  return <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
    <p className="text-slate-400 text-xs uppercase tracking-wide mb-1">{label}</p>
    <p className={`text-3xl font-bold font-mono ${c}`}>{value}</p></div>;
}
