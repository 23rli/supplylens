import { useEffect, useState } from "react";
import { fetchDashboardStats, fetchTopRisks, fetchSuppliers, fetchRiskBySite } from "../api/client";
import KPIBar from "../components/KPIBar";
import RiskTable from "../components/RiskTable";
import SupplierChart from "../components/SupplierChart";
import RiskHeatmap from "../components/RiskHeatmap";
import LoadingSpinner from "../components/LoadingSpinner";
import { PageHeader } from "../components/ui";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [risks, setRisks] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [siteData, setSiteData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([fetchDashboardStats(), fetchTopRisks(10), fetchSuppliers(), fetchRiskBySite()])
      .then(([s, r, sup, site]) => { setStats(s); setRisks(r); setSuppliers(sup); setSiteData(site); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Loading supply chain data..." />;
  if (error) return <div className="text-[#b42318] text-center py-16">Error: {error}</div>;

  return (
    <div className="space-y-6">
      <PageHeader title="Risk Overview" subtitle="Real-time risk intelligence · Boston · Chicago · Seattle" />
      <KPIBar stats={stats} />
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
        <div className="xl:col-span-2"><RiskTable risks={risks} title="Top 10 At-Risk SKUs" /></div>
        <RiskHeatmap siteData={siteData} />
      </div>
      <SupplierChart suppliers={suppliers} />
    </div>
  );
}
