import { useEffect, useState } from "react";
import { fetchActions } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import { PageHeader } from "../components/ui";

export default function Actions() {
  const [rows, setRows] = useState(null);
  useEffect(() => { fetchActions().then(setRows); }, []);
  if (!rows) return <LoadingSpinner />;
  return (
    <div className="space-y-6">
      <PageHeader title="Actions" subtitle="Pending and executed fixes across the network" />
      <div className="card overflow-hidden">
        <table className="w-full">
          <thead className="bg-surface-sunken">
            <tr className="border-b border-surface-border">
              {["SKU", "Site", "Type", "Label", "Cost", "Status"].map((h) => <th key={h} className="th">{h}</th>)}
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-border">
            {rows.map((a) => (
              <tr key={a.id} className="hover:bg-surface-sunken/60">
                <td className="td font-mono text-ink">{a.sku_id}</td>
                <td className="td">{a.site_id}</td>
                <td className="td">{a.action_type}</td>
                <td className="td">{a.label}</td>
                <td className="td font-mono">${a.cost}</td>
                <td className="td"><span className="chip chip-low"><span className="chip-dot" />{a.status}</span></td>
              </tr>
            ))}
            {rows.length === 0 && <tr><td colSpan="6" className="text-center py-12 text-ink-muted text-sm">No actions yet — resolve a risk from Today to see it here.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
