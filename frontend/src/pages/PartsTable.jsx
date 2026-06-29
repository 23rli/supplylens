import { useEffect, useState } from "react";
import { fetchParts } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import { useNavigate } from "react-router-dom";

const ABC = ["", "A", "B", "C"];
const STATUS = ["", "over", "under"];

export default function PartsTable() {
  const [parts, setParts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ abc: "", status: "" });
  const nav = useNavigate();

  useEffect(() => {
    setLoading(true);
    fetchParts(filters).then(setParts).finally(() => setLoading(false));
  }, [filters]);

  const sel = "bg-slate-700 border border-slate-600 text-slate-200 text-sm rounded-lg px-3 py-2";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Parts</h1>
        <p className="text-slate-400 text-sm mt-1">{parts.length} parts · click a row for the 52-week projection</p>
      </div>
      <div className="flex gap-3">
        <select className={sel} value={filters.abc} onChange={(e) => setFilters((f) => ({ ...f, abc: e.target.value }))}>
          {ABC.map((a) => <option key={a} value={a}>{a ? `Group ${a}` : "All ABC"}</option>)}
        </select>
        <select className={sel} value={filters.status} onChange={(e) => setFilters((f) => ({ ...f, status: e.target.value }))}>
          {STATUS.map((s) => <option key={s} value={s}>{s ? s + "stocked" : "All Status"}</option>)}
        </select>
      </div>
      {loading ? <LoadingSpinner /> : (
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden overflow-x-auto">
          <table className="w-full">
            <thead><tr className="border-b border-slate-700">
              {["Part", "Vendor", "ABC", "On Hand", "Weeks Supply", "Wks Over", "Wks Under", "Annual Spend"].map((h) =>
                <th key={h} className="px-5 py-3 text-left text-xs font-medium text-slate-400 uppercase">{h}</th>)}
            </tr></thead>
            <tbody className="divide-y divide-slate-700/50">
              {parts.map((p) => (
                <tr key={p.part_number} onClick={() => nav(`/inventory/parts/${p.part_number}`)}
                    className="hover:bg-slate-700/30 cursor-pointer">
                  <td className="px-5 py-3"><div className="text-sm text-slate-100">{p.part_number}</div><div className="text-xs text-slate-500">{p.description}</div></td>
                  <td className="px-5 py-3 text-sm text-slate-400">{p.vendor_name}</td>
                  <td className="px-5 py-3 text-sm text-slate-300">{p.abc_group}</td>
                  <td className="px-5 py-3 text-sm font-mono text-slate-300">{p.on_hand}</td>
                  <td className="px-5 py-3 text-sm font-mono text-slate-300">{p.weeks_on_hand}</td>
                  <td className={`px-5 py-3 text-sm font-mono ${p.weeks_overstocked > 0 ? "text-yellow-400" : "text-slate-500"}`}>{p.weeks_overstocked}</td>
                  <td className={`px-5 py-3 text-sm font-mono ${p.weeks_understocked > 0 ? "text-red-400" : "text-slate-500"}`}>{p.weeks_understocked}</td>
                  <td className="px-5 py-3 text-sm font-mono text-slate-300">${p.annual_spend.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
