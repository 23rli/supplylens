import { useEffect, useState } from "react";
import { fetchRiskSummary } from "../api/client";
import RiskTable from "../components/RiskTable";
import LoadingSpinner from "../components/LoadingSpinner";

const SITES = ["", "BOSTON", "CHICAGO", "SEATTLE"];
const RISK_LEVELS = ["", "CRITICAL", "HIGH", "MEDIUM", "LOW"];
const CATEGORIES = ["", "Critical", "Standard", "Consumable"];

export default function SKUTable() {
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ site: "", risk_level: "", category: "" });

  useEffect(() => {
    setLoading(true);
    fetchRiskSummary(filters)
      .then(setRisks)
      .finally(() => setLoading(false));
  }, [filters]);

  const setFilter = (key, value) => setFilters((prev) => ({ ...prev, [key]: value }));

  const selectClass = "bg-slate-700 border border-slate-600 text-slate-200 text-sm rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Full SKU Risk Table</h1>
        <p className="text-slate-400 text-sm mt-1">All {risks.length} SKU-site combinations · sorted by risk</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <select className={selectClass} value={filters.site} onChange={(e) => setFilter("site", e.target.value)}>
          {SITES.map((s) => <option key={s} value={s}>{s || "All Sites"}</option>)}
        </select>
        <select className={selectClass} value={filters.risk_level} onChange={(e) => setFilter("risk_level", e.target.value)}>
          {RISK_LEVELS.map((r) => <option key={r} value={r}>{r || "All Risk Levels"}</option>)}
        </select>
        <select className={selectClass} value={filters.category} onChange={(e) => setFilter("category", e.target.value)}>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c || "All Categories"}</option>)}
        </select>
        {(filters.site || filters.risk_level || filters.category) && (
          <button
            onClick={() => setFilters({ site: "", risk_level: "", category: "" })}
            className="text-sm text-blue-400 hover:text-blue-300 underline"
          >
            Clear filters
          </button>
        )}
      </div>

      {loading ? <LoadingSpinner /> : <RiskTable risks={risks} title={`${risks.length} SKUs`} />}
    </div>
  );
}
