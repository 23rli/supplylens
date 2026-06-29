import { useEffect, useState } from "react";
import { fetchWorstOffenders } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import { useNavigate } from "react-router-dom";

export default function WorstOffenders() {
  const [kind, setKind] = useState("under");
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const nav = useNavigate();

  useEffect(() => {
    setLoading(true);
    fetchWorstOffenders(kind, 15).then(setRows).finally(() => setLoading(false));
  }, [kind]);

  const col = kind === "under" ? "weeks_understocked" : "weeks_overstocked";
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Worst Offenders</h1>
          <p className="text-slate-400 text-sm mt-1">Parts most exposed to {kind}stock — your action list</p>
        </div>
        <div className="flex gap-1 bg-slate-800 rounded-lg p-1">
          {["under", "over"].map((k) => (
            <button key={k} onClick={() => setKind(k)}
              className={`px-4 py-2 rounded-md text-sm font-medium ${kind === k ? "bg-blue-600 text-white" : "text-slate-400"}`}>
              {k === "under" ? "Understock" : "Overstock"}
            </button>
          ))}
        </div>
      </div>
      {loading ? <LoadingSpinner /> : (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
          <table className="w-full">
            <thead><tr className="border-b border-slate-700">
              {["Part", "Vendor", "Weeks", "Pallet Gap", "Annual Spend"].map((h) =>
                <th key={h} className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase">{h}</th>)}
            </tr></thead>
            <tbody className="divide-y divide-slate-700/50">
              {rows.map((p) => (
                <tr key={p.part_number} onClick={() => nav(`/inventory/parts/${p.part_number}`)} className="hover:bg-slate-700/30 cursor-pointer">
                  <td className="px-6 py-3"><div className="text-sm text-slate-100">{p.part_number}</div><div className="text-xs text-slate-500">{p.description}</div></td>
                  <td className="px-6 py-3 text-sm text-slate-400">{p.vendor_name}</td>
                  <td className={`px-6 py-3 font-mono font-semibold ${kind === "under" ? "text-red-400" : "text-yellow-400"}`}>{p[col]}</td>
                  <td className="px-6 py-3 font-mono text-slate-300">{kind === "under" ? p.max_pallets_under : p.max_pallets_over}</td>
                  <td className="px-6 py-3 font-mono text-slate-300">${p.annual_spend.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
