import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login as apiLogin } from "../api/client";
import { useAuth } from "../auth";

export default function Login() {
  const [email, setEmail] = useState("admin@supplylens.io");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const { signIn } = useAuth();
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true); setError("");
    try {
      const { token, user } = await apiLogin(email, password);
      signIn(token, user);
      nav("/today");
    } catch {
      setError("Invalid email or password");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-sunken px-4">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2.5 justify-center mb-6">
          <div className="w-9 h-9 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold">SL</div>
          <span className="text-lg font-semibold text-ink">SupplyLens</span>
        </div>
        <form onSubmit={submit} className="card p-6 space-y-4">
          <div>
            <h1 className="section-title">Sign in</h1>
            <p className="text-sm text-ink-muted mt-0.5">Access your supply-chain workspace</p>
          </div>
          <div>
            <label className="label">Email</label>
            <input className="input w-full mt-1" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <label className="label">Password</label>
            <input className="input w-full mt-1" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="demo1234" required />
          </div>
          {error && <p className="text-sm text-[#b42318] bg-[#fef3f2] border border-[#fecdca] rounded-lg px-3 py-2">{error}</p>}
          <button className="btn-primary w-full" disabled={busy}>{busy ? "Signing in..." : "Sign in"}</button>
          <p className="text-xs text-ink-muted text-center">Demo: admin@supplylens.io / demo1234</p>
        </form>
      </div>
    </div>
  );
}
