import { useEffect, useState } from "react";
import { fetchActions } from "../api/client";
import { PageHeader, TableSkeleton, EmptyState } from "../components/ui";

export default function Actions() {
  const [rows, setRows] = useState(null);
  useEffect(() => { fetchActions().then(setRows).catch(() => setRows([])); }, []);

  return (
    <div className="space-y-6">
      <PageHeader title="Actions" subtitle="Pending and executed fixes across the network" />
      {!rows ? <TableSkeleton rows={5} cols={6} /> : rows.length === 0 ? (
        <EmptyState icon="check" title="No actions yet" message="When you resolve a risk from the Today page, the executed PO or transfer shows up here for tracking." />
      ) : (
        <div className="card overflow-hidden fade-in">
          <table className="w-full">
            <thead className="bg-surface-sunken">
              <tr className="border-b border-surface-border">
                {["SKU", "Site", "Type", "Label", "Cost", "Status"].map((h) => <th key={h} className="th">{h}</th>)}
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {rows.map((a) => (
                <tr key={a.id} className="hover:bg-surface-sunken/60 transition-colors">
                  <td className="td font-mono text-ink">{a.sku_id}</td>
                  <td className="td">{a.site_id}</td>
                  <td className="td">{a.action_type}</td>
                  <td className="td">{a.label}</td>
                  <td className="td font-mono">${a.cost}</td>
                  <td className="td"><span className="chip chip-low"><span className="chip-dot" />{a.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
