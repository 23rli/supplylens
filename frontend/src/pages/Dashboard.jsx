import { useEffect, useState } from "react";
import { fetchDashboardStats, fetchTopRisks, fetchSuppliers, fetchRiskBySite } from "../api/client";
import KPIBar from "../components/KPIBar";
import RiskTable from "../components/RiskTable";
import SupplierChart from "../components/SupplierChart";
import RiskHeatmap from "../components/RiskHeatmap";
import LoadingSpinner from "../components/LoadingSpinner";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [risks, setRisks] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [siteData, setSiteData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      fetchDashboardStats(),
      fetchTopRisks(10),
      fetchSuppliers(),
      fetchRiskBySite(),
    ])
      .then(([statsData, risksData, suppliersData, siteRiskData]) => {
        setStats(statsData);
        setRisks(risksData);
        setSuppliers(suppliersData);
        setSiteData(siteRiskData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Loading supply chain data..." />;
  if (error) return <div className="text-red-400 text-center py-16">Error: {error}</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Supply Chain Overview</h1>
        <p className="text-slate-400 text-sm mt-1">
          Real-time risk intelligence · Boston · Chicago · Seattle
        </p>
      </div>

      <KPIBar stats={stats} />

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2">
          <RiskTable risks={risks} title="Top 10 At-Risk SKUs" />
        </div>
        <div>
          <RiskHeatmap siteData={siteData} />
        </div>
      </div>

      <SupplierChart suppliers={suppliers} />
    </div>
  );
}
