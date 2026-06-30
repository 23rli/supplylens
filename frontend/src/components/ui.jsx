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

// ---- Skeletons -----------------------------------------------------------
export function Skeleton({ className = "" }) {
  return <div className={`skeleton ${className}`} />;
}

export function StatSkeleton() {
  return (
    <div className="card p-4 space-y-2">
      <Skeleton className="h-3 w-20" />
      <Skeleton className="h-7 w-16" />
      <Skeleton className="h-3 w-24" />
    </div>
  );
}

export function StatsRowSkeleton({ count = 4 }) {
  return (
    <div className={`grid grid-cols-2 lg:grid-cols-${count} gap-4`}>
      {Array.from({ length: count }).map((_, i) => <StatSkeleton key={i} />)}
    </div>
  );
}

export function TableSkeleton({ rows = 6, cols = 5 }) {
  return (
    <div className="card overflow-hidden">
      <div className="px-5 py-3.5 border-b border-surface-border"><Skeleton className="h-4 w-40" /></div>
      <div className="divide-y divide-surface-border">
        {Array.from({ length: rows }).map((_, r) => (
          <div key={r} className="flex items-center gap-4 px-5 py-3.5">
            {Array.from({ length: cols }).map((_, c) => (
              <Skeleton key={c} className={`h-4 ${c === 0 ? "w-40" : "w-20"}`} />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export function ChartSkeleton({ height = 280 }) {
  return (
    <div className="card p-5 space-y-3">
      <Skeleton className="h-4 w-48" />
      <Skeleton className="w-full" style={{ height }} />
    </div>
  );
}

// ---- Empty & error states ------------------------------------------------
export function EmptyState({ title = "Nothing here yet", message, icon = "inbox", action }) {
  const paths = {
    inbox: "M22 12h-6l-2 3h-4l-2-3H2M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z",
    check: "M9 11l3 3L22 4M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11",
    search: "M21 21l-4.35-4.35M11 19a8 8 0 1 1 0-16 8 8 0 0 1 0 16z",
  };
  return (
    <div className="card p-12 flex flex-col items-center text-center gap-3">
      <div className="w-12 h-12 rounded-xl bg-surface-sunken flex items-center justify-center text-ink-muted">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d={paths[icon] || paths.inbox} /></svg>
      </div>
      <div>
        <p className="font-semibold text-ink">{title}</p>
        {message && <p className="text-sm text-ink-muted mt-0.5 max-w-sm">{message}</p>}
      </div>
      {action}
    </div>
  );
}

export function ErrorState({ message = "Something went wrong", onRetry }) {
  return (
    <div className="card p-10 flex flex-col items-center text-center gap-3">
      <div className="w-12 h-12 rounded-xl bg-[#fef3f2] text-[#b42318] flex items-center justify-center">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" /></svg>
      </div>
      <p className="text-sm text-ink-soft max-w-sm">{message}</p>
      {onRetry && <button onClick={onRetry} className="btn-outline">Try again</button>}
    </div>
  );
}
