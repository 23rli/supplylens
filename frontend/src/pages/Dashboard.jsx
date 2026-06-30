import { useEffect, useState } from "react";
import { fetchDashboardStats, fetchTopRisks, fetchSuppliers, fetchRiskBySite } from "../api/client";
import KPIBar from "../components/KPIBar";
import RiskTable from "../components/RiskTable";
import SupplierChart from "../components/SupplierChart";
import RiskHeatmap from "../components/RiskHeatmap";
import { PageHeader, StatsRowSkeleton, TableSkeleton, ChartSkeleton, ErrorState } from "../components/ui";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [risks, setRisks] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [siteData, setSiteData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = () => {
    setLoading(true); setError(null);
    Promise.all([fetchDashboardStats(), fetchTopRisks(10), fetchSuppliers(), fetchRiskBySite()])
      .then(([s, r, sup, site]) => { setStats(s); setRisks(r); setSuppliers(sup); setSiteData(site); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };
  useEffect(load, []);

  return (
    <div className="space-y-6">
      <PageHeader title="Risk Overview" subtitle="Real-time risk intelligence \u00b7 Boston \u00b7 Chicago \u00b7 Seattle" />
      {error ? <ErrorState message={error} onRetry={load} /> : loading ? (
        <div className="space-y-6">
          <StatsRowSkeleton count={4} />
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
            <div className="xl:col-span-2"><TableSkeleton rows={6} cols={6} /></div>
            <ChartSkeleton height={200} />
          </div>
          <ChartSkeleton height={240} />
        </div>
      ) : (
        <div className="space-y-6 fade-in">
          <KPIBar stats={stats} />
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
            <div className="xl:col-span-2"><RiskTable risks={risks} title="Top 10 At-Risk SKUs" /></div>
            <RiskHeatmap siteData={siteData} />
          </div>
          <SupplierChart suppliers={suppliers} />
        </div>
      )}
    </div>
  );
}
