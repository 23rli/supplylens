// Shared enterprise UI primitives.

export function PageHeader({ title, subtitle, actions }) {
  return (
    <div className="flex items-start justify-between gap-4">
      <div>
        <h1 className="page-title">{title}</h1>
        {subtitle && <p className="page-sub">{subtitle}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}

export function Card({ title, action, children, className = "", pad = true }) {
  return (
    <div className={`card ${className}`}>
      {(title || action) && (
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-surface-border">
          {title && <h2 className="section-title">{title}</h2>}
          {action}
        </div>
      )}
      <div className={pad ? "p-5" : ""}>{children}</div>
    </div>
  );
}

const TONE = {
  neutral: "text-ink", brand: "text-brand-600", critical: "text-[#b42318]",
  high: "text-[#b54708]", warn: "text-[#854a0e]", good: "text-[#067647]",
};

export function Stat({ label, value, sub, tone = "neutral" }) {
  return (
    <div className="card p-4">
      <p className="label mb-1.5">{label}</p>
      <p className={`stat ${TONE[tone] || TONE.neutral}`}>{value}</p>
      {sub && <p className="text-xs text-ink-muted mt-1">{sub}</p>}
    </div>
  );
}

export function RiskChip({ level }) {
  const l = (level || "LOW").toUpperCase();
  const cls = { CRITICAL: "chip-critical", HIGH: "chip-high", MEDIUM: "chip-medium", LOW: "chip-low" }[l] || "chip-low";
  return <span className={`chip ${cls}`}><span className="chip-dot" />{l}</span>;
}
