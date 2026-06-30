import { useEffect, useState } from "react";
import { fetchParts, importParts } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import { PageHeader } from "../components/ui";
import { useNavigate } from "react-router-dom";

const ABC = ["", "A", "B", "C"];
const STATUS = ["", "over", "under"];

export default function PartsTable() {
  const [parts, setParts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ abc: "", status: "" });
  const [msg, setMsg] = useState("");
  const nav = useNavigate();

  useEffect(() => {
    setLoading(true);
    fetchParts(filters).then(setParts).finally(() => setLoading(false));
  }, [filters]);

  const onImport = async (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setMsg("Importing...");
    try { const r = await importParts(f); setMsg(`Imported ${r.imported} parts`); setFilters((x) => ({ ...x })); }
    catch { setMsg("Import failed — check columns"); }
  };

  return (
    <div className="space-y-6">
      <PageHeader title="Parts" subtitle={`${parts.length} parts · select a row for the 52-week projection`}
        actions={
          <label className="btn-primary cursor-pointer">
            Import CSV/XLSX
            <input type="file" accept=".csv,.xlsx,.xlsm" className="hidden" onChange={onImport} />
          </label>
        } />
      {msg && <p className="text-sm text-ink-soft">{msg}</p>}
      <div className="flex gap-3">
        <select className="input" value={filters.abc} onChange={(e) => setFilters((f) => ({ ...f, abc: e.target.value }))}>
          {ABC.map((a) => <option key={a} value={a}>{a ? `Group ${a}` : "All ABC"}</option>)}
        </select>
        <select className="input" value={filters.status} onChange={(e) => setFilters((f) => ({ ...f, status: e.target.value }))}>
          {STATUS.map((s) => <option key={s} value={s}>{s ? `${s}stocked` : "All Status"}</option>)}
        </select>
      </div>
      {loading ? <LoadingSpinner /> : (
        <div className="card overflow-hidden overflow-x-auto">
          <table className="w-full">
            <thead className="bg-surface-sunken">
              <tr className="border-b border-surface-border">
                {["Part", "Vendor", "ABC", "On Hand", "Weeks Supply", "Wks Over", "Wks Under", "Annual Spend"].map((h) => <th key={h} className="th">{h}</th>)}
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {parts.map((p) => (
                <tr key={p.part_number} onClick={() => nav(`/inventory/parts/${p.part_number}`)} className="hover:bg-surface-sunken/60 cursor-pointer">
                  <td className="td"><div className="font-medium text-ink">{p.part_number}</div><div className="text-xs text-ink-muted">{p.description}</div></td>
                  <td className="td">{p.vendor_name}</td>
                  <td className="td">{p.abc_group}</td>
                  <td className="td font-mono">{p.on_hand}</td>
                  <td className="td font-mono">{p.weeks_on_hand}</td>
                  <td className={`td font-mono ${p.weeks_overstocked > 0 ? "text-[#b54708]" : "text-ink-muted"}`}>{p.weeks_overstocked}</td>
                  <td className={`td font-mono ${p.weeks_understocked > 0 ? "text-[#b42318]" : "text-ink-muted"}`}>{p.weeks_understocked}</td>
                  <td className="td font-mono">${p.annual_spend.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
