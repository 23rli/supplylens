import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Login from "./pages/Login";
import { isAuthed } from "./auth";
import Today from "./pages/Today";
import DecisionView from "./pages/DecisionView";
import Actions from "./pages/Actions";
import Dashboard from "./pages/Dashboard";
import SKUTable from "./pages/SKUTable";
import InventoryOverview from "./pages/InventoryOverview";
import PartsTable from "./pages/PartsTable";
import PartDetail from "./pages/PartDetail";
import WorstOffenders from "./pages/WorstOffenders";
import Hedging from "./pages/Hedging";
import Chat from "./pages/Chat";

function Shell() {
  if (!isAuthed()) return <Navigate to="/login" replace />;
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 min-w-0">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Navigate to="/today" replace />} />
            <Route path="/today" element={<Today />} />
            <Route path="/decision/:sku/:site" element={<DecisionView />} />
            <Route path="/actions" element={<Actions />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/skus" element={<SKUTable />} />
            <Route path="/inventory" element={<InventoryOverview />} />
            <Route path="/inventory/parts" element={<PartsTable />} />
            <Route path="/inventory/parts/:partNumber" element={<PartDetail />} />
            <Route path="/inventory/worst" element={<WorstOffenders />} />
            <Route path="/hedging" element={<Hedging />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/*" element={<Shell />} />
      </Routes>
    </BrowserRouter>
  );
}
