import { createContext, useContext, useState } from "react";
import { TOKEN_KEY } from "./api/client";

const AuthCtx = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("sl_user");
    return raw ? JSON.parse(raw) : null;
  });

  const signIn = (token, u) => {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem("sl_user", JSON.stringify(u));
    setUser(u);
  };
  const signOut = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem("sl_user");
    setUser(null);
    window.location.href = "/login";
  };

  return <AuthCtx.Provider value={{ user, signIn, signOut }}>{children}</AuthCtx.Provider>;
}

export const useAuth = () => useContext(AuthCtx);

export function isAuthed() {
  return !!localStorage.getItem(TOKEN_KEY);
}
