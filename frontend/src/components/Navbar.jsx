import { NavLink } from "react-router-dom";

const groups = [
  { label: "Ops", items: [
    { path: "/today", label: "Today" },
    { path: "/actions", label: "Actions" },
  ]},
  { label: "Inventory Engine", items: [
    { path: "/inventory", label: "Overview" },
    { path: "/inventory/parts", label: "Parts" },
    { path: "/inventory/worst", label: "Worst Offenders" },
  ]},
  { label: "Hedging", items: [{ path: "/hedging", label: "Planner" }] },
  { label: "Risk", items: [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/skus", label: "SKU Risk" },
  ]},
  { label: "AI", items: [{ path: "/chat", label: "Analyst" }] },
];

export default function Navbar() {
  return (
    <nav className="bg-slate-800 border-b border-slate-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">SL</span>
            </div>
            <span className="text-slate-100 font-bold text-lg">SupplyLens</span>
            <span className="text-slate-400 text-xs ml-1 hidden md:inline">Supply Chain Intelligence</span>
          </div>
          <div className="flex items-center gap-4">
            {groups.map((g) => (
              <div key={g.label} className="flex items-center gap-1">
                <span className="text-slate-600 text-[10px] uppercase tracking-wider hidden lg:inline mr-1">{g.label}</span>
                {g.items.map(({ path, label }) => (
                  <NavLink key={path} to={path} end
                    className={({ isActive }) =>
                      `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive ? "bg-blue-600 text-white" : "text-slate-400 hover:text-slate-100 hover:bg-slate-700"
                      }`}>
                    {label}
                  </NavLink>
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}
