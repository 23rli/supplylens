const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export async function fetchDashboardStats() {
  const res = await fetch(`${BASE_URL}/dashboard-stats`);
  if (!res.ok) throw new Error("Failed to fetch dashboard stats");
  return res.json();
}

export async function fetchTopRisks(limit = 10) {
  const res = await fetch(`${BASE_URL}/top-risks?limit=${limit}`);
  if (!res.ok) throw new Error("Failed to fetch top risks");
  return res.json();
}

export async function fetchRiskSummary({ site, risk_level, category } = {}) {
  const params = new URLSearchParams();
  if (site) params.append("site", site);
  if (risk_level) params.append("risk_level", risk_level);
  if (category) params.append("category", category);
  const res = await fetch(`${BASE_URL}/risk-summary?${params}`);
  if (!res.ok) throw new Error("Failed to fetch risk summary");
  return res.json();
}

export async function fetchRiskBySite() {
  const res = await fetch(`${BASE_URL}/risk-by-site`);
  if (!res.ok) throw new Error("Failed to fetch site risk data");
  return res.json();
}

export async function fetchSuppliers() {
  const res = await fetch(`${BASE_URL}/suppliers`);
  if (!res.ok) throw new Error("Failed to fetch suppliers");
  return res.json();
}

export async function sendChatMessage(message, conversationHistory) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      conversation_history: conversationHistory,
    }),
  });
  if (!res.ok) throw new Error("Failed to get AI response");
  return res.json();
}

// ── Inventory Engine ──────────────────────────────────────────────
export async function fetchInventoryStats() {
  const res = await fetch(`${BASE_URL}/inventory/stats`);
  if (!res.ok) throw new Error("Failed to fetch inventory stats");
  return res.json();
}

export async function fetchParts({ abc, vendor, status } = {}) {
  const params = new URLSearchParams();
  if (abc) params.append("abc", abc);
  if (vendor) params.append("vendor", vendor);
  if (status) params.append("status", status);
  const res = await fetch(`${BASE_URL}/inventory/parts?${params}`);
  if (!res.ok) throw new Error("Failed to fetch parts");
  return res.json();
}

export async function fetchPartDetail(partNumber) {
  const res = await fetch(`${BASE_URL}/inventory/part/${partNumber}`);
  if (!res.ok) throw new Error("Failed to fetch part");
  return res.json();
}

export async function fetchWorstOffenders(kind = "over", limit = 15) {
  const res = await fetch(`${BASE_URL}/inventory/worst?kind=${kind}&limit=${limit}`);
  if (!res.ok) throw new Error("Failed to fetch worst offenders");
  return res.json();
}

export async function fetchWarehouseLoad() {
  const res = await fetch(`${BASE_URL}/inventory/warehouse-load`);
  if (!res.ok) throw new Error("Failed to fetch warehouse load");
  return res.json();
}

// ── Hedging Planner ───────────────────────────────────────────────
export async function fetchHedgingScenario({ s1 = 0.75, s2 = 0.25, inv_cost = 0.01, start_inv = 0 } = {}) {
  const params = new URLSearchParams({ s1, s2, inv_cost, start_inv });
  const res = await fetch(`${BASE_URL}/hedging/scenario?${params}`);
  if (!res.ok) throw new Error("Failed to fetch hedging scenario");
  return res.json();
}

export async function fetchPriceForecast(oil = "OIL_1") {
  const res = await fetch(`${BASE_URL}/hedging/forecast?oil=${oil}`);
  if (!res.ok) throw new Error("Failed to fetch forecast");
  return res.json();
}

export async function importParts(file) {
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(`${BASE_URL}/inventory/import`, { method: "POST", body: fd });
  if (!res.ok) throw new Error("Import failed");
  return res.json();
}

// ── Decision engine + AI copilot ──────────────────────────────────
export async function fetchToday() {
  const res = await fetch(`${BASE_URL}/today`);
  if (!res.ok) throw new Error("Failed to fetch today");
  return res.json();
}

export async function fetchBriefing() {
  const res = await fetch(`${BASE_URL}/ai/briefing`);
  if (!res.ok) throw new Error("Failed to fetch briefing");
  return res.json();
}

export async function explainDecision(sku, site) {
  const res = await fetch(`${BASE_URL}/ai/explain?sku=${sku}&site=${site}`);
  if (!res.ok) throw new Error("Failed to explain");
  return res.json();
}

export async function executeAction(kind, payload) {
  const ep = kind === "REBALANCE" ? "transfer" : "create-po";
  const res = await fetch(`${BASE_URL}/actions/${ep}`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Action failed");
  return res.json();
}

export async function fetchActions() {
  const res = await fetch(`${BASE_URL}/actions/status`);
  if (!res.ok) throw new Error("Failed to fetch actions");
  return res.json();
}
