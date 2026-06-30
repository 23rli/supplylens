import { createContext, useCallback, useContext, useState } from "react";

const ToastCtx = createContext(null);
let _id = 0;

const ICON = {
  success: { c: "#067647", bg: "#ecfdf3", d: "M9 11l3 3L22 4M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" },
  error: { c: "#b42318", bg: "#fef3f2", d: "M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" },
  info: { c: "#4f46e5", bg: "#eef2ff", d: "M12 16v-4M12 8h.01M12 22a10 10 0 1 1 0-20 10 10 0 0 1 0 20z" },
};

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const dismiss = useCallback((id) => setToasts((t) => t.filter((x) => x.id !== id)), []);
  const toast = useCallback((message, type = "success", ttl = 4000) => {
    const id = ++_id;
    setToasts((t) => [...t, { id, message, type }]);
    setTimeout(() => dismiss(id), ttl);
  }, [dismiss]);

  return (
    <ToastCtx.Provider value={toast}>
      {children}
      <div className="toast-wrap">
        {toasts.map((t) => {
          const i = ICON[t.type] || ICON.info;
          return (
            <div key={t.id} className="toast" role="status">
              <span className="w-6 h-6 rounded-md flex items-center justify-center shrink-0" style={{ background: i.bg, color: i.c }}>
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d={i.d} /></svg>
              </span>
              <p className="text-sm text-ink flex-1">{t.message}</p>
              <button onClick={() => dismiss(t.id)} className="text-ink-muted hover:text-ink text-sm">&times;</button>
            </div>
          );
        })}
      </div>
    </ToastCtx.Provider>
  );
}

export const useToast = () => useContext(ToastCtx);
