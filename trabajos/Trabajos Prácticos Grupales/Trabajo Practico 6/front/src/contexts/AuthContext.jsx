import React, { createContext, useEffect, useRef, useState } from 'react';
import api, { saveToken, clearToken } from '../services/api';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('access_token'));
  const [loading, setLoading] = useState(false);
  const logoutTimeoutRef = useRef(null);

  // Decodifica el payload de un JWT (sin verificar firma). Retorna objeto o null.
  function decodeJwtPayload(jwt) {
    try {
      const parts = jwt.split('.');
      if (parts.length < 2) return null;
      const payload = parts[1];
      const b64 = payload.replace(/-/g, '+').replace(/_/g, '/');
      const json = decodeURIComponent(
        atob(b64)
          .split('')
          .map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
          })
          .join('')
      );
      return JSON.parse(json);
    } catch (e) {
      return null;
    }
  }

  // Retorna true si el payload indica que el token expiró.
  function isTokenExpired(payload) {
    if (!payload || typeof payload.exp !== 'number') return true;
    return Date.now() >= payload.exp * 1000;
  }

  // Programa un timeout para el auto-logout basado en exp (ms restantes).
  function scheduleAutoLogout(payload) {
    if (!payload || typeof payload.exp !== 'number') return;
    // limpiar timeout previo
    if (logoutTimeoutRef.current) {
      clearTimeout(logoutTimeoutRef.current);
      logoutTimeoutRef.current = null;
    }
    const expiresAt = payload.exp * 1000; // ms
    const msLeft = expiresAt - Date.now();
    if (msLeft <= 0) {
      // ya expirado
      logout();
      return;
    }
    const MAX_TIMEOUT = 2147483647; // límite de setTimeout en JS
    const timeout = Math.min(msLeft, MAX_TIMEOUT);
    logoutTimeoutRef.current = setTimeout(() => {
      logout();
    }, timeout);
  }

  // Función pública para validar el token actual (no expirado).
  function validateToken(jwt = token) {
    if (!jwt) return false;
    const payload = decodeJwtPayload(jwt);
    if (!payload) return false;
    return !isTokenExpired(payload);
  }

  useEffect(() => {
    // Si ya hay token en localStorage, intentamos recuperar información mínima del usuario
    // y validar si está expirado. También programamos auto-logout según exp.
    if (token) {
      const payload = decodeJwtPayload(token);
      if (!payload || isTokenExpired(payload)) {
        // token inválido o expirado -> desloguear
        clearToken();
        setToken(null);
        setUser(null);
        return;
      }
      setUser({ email: payload.sub || payload.email || null, raw: payload });
      scheduleAutoLogout(payload);
    } else {
      // no hay token: limpiar timeout si existe
      if (logoutTimeoutRef.current) {
        clearTimeout(logoutTimeoutRef.current);
        logoutTimeoutRef.current = null;
      }
      setUser(null);
    }
  }, [token]);

  async function login(email, password) {
    setLoading(true);
    try {
      const res = await api.login(email, password);
      if (res && res.access_token) {
        saveToken(res.access_token);
        setToken(res.access_token);
        // parsear JWT para obtener email y programar auto-logout
        const payload = decodeJwtPayload(res.access_token);
        if (payload && !isTokenExpired(payload)) {
          setUser({ email: payload.sub || payload.email || null, raw: payload });
          scheduleAutoLogout(payload);
        } else {
          setUser({ email });
        }
        return res;
      }
      throw new Error('Token no recibido');
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    clearToken();
    setToken(null);
    setUser(null);
    if (logoutTimeoutRef.current) {
      clearTimeout(logoutTimeoutRef.current);
      logoutTimeoutRef.current = null;
    }
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, validateToken }}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
