import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import SKUTable from "./pages/SKUTable";
import Chat from "./pages/Chat";
import InventoryOverview from "./pages/InventoryOverview";
import PartsTable from "./pages/PartsTable";
import PartDetail from "./pages/PartDetail";
import WorstOffenders from "./pages/WorstOffenders";
import Hedging from "./pages/Hedging";
import Today from "./pages/Today";
import DecisionView from "./pages/DecisionView";
import Actions from "./pages/Actions";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-900">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Navigate to="/today" replace />} />
            <Route path="/today" element={<Today />} />
            <Route path="/decision/:sku/:site" element={<DecisionView />} />
            <Route path="/actions" element={<Actions />} />
            <Route path="/inventory" element={<InventoryOverview />} />
            <Route path="/inventory/parts" element={<PartsTable />} />
            <Route path="/inventory/parts/:partNumber" element={<PartDetail />} />
            <Route path="/inventory/worst" element={<WorstOffenders />} />
            <Route path="/hedging" element={<Hedging />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/skus" element={<SKUTable />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
