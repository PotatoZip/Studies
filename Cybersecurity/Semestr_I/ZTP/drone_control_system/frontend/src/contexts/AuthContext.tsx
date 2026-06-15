import React, { createContext, useContext, useEffect, useState } from "react";
import { authApi, setToken, clearToken, getToken } from "@/services/api";
import type { Role } from "@/services/api";
import { wsService } from "@/services/websocket";

// ─────────────────────────────────────────────────────────────────────────────
//  Auth context – manages JWT, user info, WebSocket lifecycle
// ─────────────────────────────────────────────────────────────────────────────

interface AuthUser {
  username: string;
  role: Role;
}

interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>(null!);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setTokenState] = useState<string | null>(getToken());
  const [isLoading, setIsLoading] = useState(true);

  // On mount: restore session from localStorage
  useEffect(() => {
    const stored = getToken();
    if (!stored) {
      setIsLoading(false);
      return;
    }
    authApi
      .me()
      .then((me) => {
        setUser({ username: me.username, role: me.role });
        setTokenState(stored);
        // connect WebSocket using stored token
        wsService.connect(stored).catch(console.error);
      })
      .catch(() => {
        // token expired / invalid – clear it
        clearToken();
        setTokenState(null);
      })
      .finally(() => setIsLoading(false));
  }, []);

  const login = async (username: string, password: string) => {
    const res = await authApi.login(username, password);
    setToken(res.token);
    setTokenState(res.token);
    setUser({ username: res.username, role: res.role });
    wsService.connect(res.token).catch(console.error);
  };

  const register = async (
    username: string,
    email: string,
    password: string,
  ) => {
    const res = await authApi.register(username, email, password);
    setToken(res.token);
    setTokenState(res.token);
    setUser({ username: res.username, role: res.role });
    wsService.connect(res.token).catch(console.error);
  };

  const logout = () => {
    wsService.disconnect();
    clearToken();
    setTokenState(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
