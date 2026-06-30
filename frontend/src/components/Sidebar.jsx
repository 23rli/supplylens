import { NavLink } from "react-router-dom";

const sections = [
  { items: [{ to: "/today", label: "Today", icon: "home" }] },
  { title: "Risk Intelligence", items: [
    { to: "/dashboard", label: "Overview", icon: "grid" },
    { to: "/skus", label: "SKU Risk", icon: "list" },
  ]},
  { title: "Inventory", items: [
    { to: "/inventory", label: "Overview", icon: "box" },
    { to: "/inventory/parts", label: "Parts", icon: "list" },
    { to: "/inventory/worst", label: "Worst Offenders", icon: "alert" },
  ]},
  { title: "Procurement", items: [
    { to: "/hedging", label: "Hedging Planner", icon: "trend" },
  ]},
  { title: "Workflow", items: [
    { to: "/actions", label: "Actions", icon: "check" },
    { to: "/chat", label: "AI Analyst", icon: "spark" },
  ]},
];

const icons = {
  home: "M3 11l9-8 9 8M5 10v10h14V10",
  grid: "M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z",
  list: "M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01",
  box: "M21 8l-9-5-9 5 9 5 9-5zM3 8v8l9 5 9-5V8",
  alert: "M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z",
  trend: "M3 17l6-6 4 4 8-8M21 7v6h-6",
  check: "M9 11l3 3L22 4M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11",
  spark: "M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2 2M16 16l2 2M16 8l2-2M6 18l2-2",
};

function Icon({ name }) {
  return (
    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor"
      strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="shrink-0">
      <path d={icons[name]} />
    </svg>
  );
}

export default function Sidebar() {
  return (
    <aside className="w-60 shrink-0 bg-white border-r border-surface-border flex flex-col h-screen sticky top-0">
      <div className="h-16 flex items-center gap-2.5 px-5 border-b border-surface-border">
        <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold text-sm">SL</div>
        <div className="leading-tight">
          <div className="font-semibold text-ink text-[15px]">SupplyLens</div>
          <div className="text-[11px] text-ink-muted">Supply Chain Intelligence</div>
        </div>
      </div>
      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-5">
        {sections.map((s, i) => (
          <div key={i}>
            {s.title && <p className="px-3 mb-1.5 text-[10px] font-semibold text-ink-muted uppercase tracking-wider">{s.title}</p>}
            <div className="space-y-0.5">
              {s.items.map((it) => (
                <NavLink key={it.to} to={it.to} end={it.to === "/inventory"}
                  className={({ isActive }) =>
                    `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      isActive ? "bg-brand-50 text-brand-700" : "text-ink-soft hover:bg-surface-sunken hover:text-ink"
                    }`}>
                  <Icon name={it.icon} />{it.label}
                </NavLink>
              ))}
            </div>
          </div>
        ))}
      </nav>
      <div className="px-5 py-3 border-t border-surface-border text-[11px] text-ink-muted">v1.5 · Decision Engine</div>
    </aside>
  );
}
