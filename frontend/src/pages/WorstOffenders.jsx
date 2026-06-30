import { useEffect, useState } from "react";
import { fetchWorstOffenders } from "../api/client";
import { TableSkeleton } from "../components/ui";
import { PageHeader } from "../components/ui";
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
      <PageHeader title="Worst Offenders" subtitle={`Parts most exposed to ${kind}stock â€” your action list`}
        actions={
          <div className="flex gap-1 bg-surface-sunken border border-surface-border rounded-lg p-1">
            {["under", "over"].map((k) => (
              <button key={k} onClick={() => setKind(k)}
                className={`px-3.5 py-1.5 rounded-md text-sm font-medium transition-colors ${kind === k ? "bg-white text-ink shadow-card" : "text-ink-muted hover:text-ink"}`}>
                {k === "under" ? "Understock" : "Overstock"}
              </button>
            ))}
          </div>
        } />
      {loading ? <TableSkeleton rows={8} cols={5} /> : (
        <div className="card overflow-hidden">
          <table className="w-full">
            <thead className="bg-surface-sunken">
              <tr className="border-b border-surface-border">
                {["Part", "Vendor", "Weeks", "Pallet Gap", "Annual Spend"].map((h) => <th key={h} className="th">{h}</th>)}
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {rows.map((p) => (
                <tr key={p.part_number} onClick={() => nav(`/inventory/parts/${p.part_number}`)} className="hover:bg-surface-sunken/60 cursor-pointer">
                  <td className="td"><div className="font-medium text-ink">{p.part_number}</div><div className="text-xs text-ink-muted">{p.description}</div></td>
                  <td className="td">{p.vendor_name}</td>
                  <td className={`td font-mono font-semibold ${kind === "under" ? "text-[#b42318]" : "text-[#b54708]"}`}>{p[col]}</td>
                  <td className="td font-mono">{kind === "under" ? p.max_pallets_under : p.max_pallets_over}</td>
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
