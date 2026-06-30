import { useEffect, useState } from "react";
import { fetchRiskSummary } from "../api/client";
import RiskTable from "../components/RiskTable";
import LoadingSpinner from "../components/LoadingSpinner";
import { PageHeader } from "../components/ui";

const SITES = ["", "BOSTON", "CHICAGO", "SEATTLE"];
const RISK_LEVELS = ["", "CRITICAL", "HIGH", "MEDIUM", "LOW"];
const CATEGORIES = ["", "Critical", "Standard", "Consumable"];

export default function SKUTable() {
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ site: "", risk_level: "", category: "" });

  useEffect(() => {
    setLoading(true);
    fetchRiskSummary(filters).then(setRisks).finally(() => setLoading(false));
  }, [filters]);

  const set = (k, v) => setFilters((p) => ({ ...p, [k]: v }));
  const active = filters.site || filters.risk_level || filters.category;

  return (
    <div className="space-y-6">
      <PageHeader title="SKU Risk" subtitle={`${risks.length} SKU-site combinations · sorted by risk`} />
      <div className="flex flex-wrap items-center gap-3">
        <select className="input" value={filters.site} onChange={(e) => set("site", e.target.value)}>
          {SITES.map((s) => <option key={s} value={s}>{s || "All Sites"}</option>)}
        </select>
        <select className="input" value={filters.risk_level} onChange={(e) => set("risk_level", e.target.value)}>
          {RISK_LEVELS.map((r) => <option key={r} value={r}>{r || "All Risk Levels"}</option>)}
        </select>
        <select className="input" value={filters.category} onChange={(e) => set("category", e.target.value)}>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c || "All Categories"}</option>)}
        </select>
        {active && <button onClick={() => setFilters({ site: "", risk_level: "", category: "" })} className="text-sm text-brand-600 hover:text-brand-700 font-medium">Clear filters</button>}
      </div>
      {loading ? <LoadingSpinner /> : <RiskTable risks={risks} title={`${risks.length} SKUs`} />}
    </div>
  );
}
