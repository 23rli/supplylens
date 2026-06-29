import { useEffect, useState } from "react";
import { fetchActions } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";

export default function Actions() {
  const [rows, setRows] = useState(null);
  useEffect(() => { fetchActions().then(setRows); }, []);
  if (!rows) return <LoadingSpinner />;
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-100">Actions</h1>
      <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
        <table className="w-full">
          <thead><tr className="border-b border-slate-700">
            {["SKU","Site","Type","Label","Cost","Status"].map((h)=><th key={h} className="px-5 py-3 text-left text-xs text-slate-400 uppercase">{h}</th>)}
          </tr></thead>
          <tbody className="divide-y divide-slate-700/50">
            {rows.map((a)=>(
              <tr key={a.id}><td className="px-5 py-3 text-sm text-slate-200">{a.sku_id}</td>
                <td className="px-5 py-3 text-sm text-slate-300">{a.site_id}</td>
                <td className="px-5 py-3 text-sm text-slate-300">{a.action_type}</td>
                <td className="px-5 py-3 text-sm text-slate-400">{a.label}</td>
                <td className="px-5 py-3 text-sm font-mono text-slate-300">${a.cost}</td>
                <td className="px-5 py-3 text-sm text-green-400">{a.status}</td></tr>
            ))}
            {rows.length===0 && <tr><td colSpan="6" className="text-center py-10 text-slate-500">No actions yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
