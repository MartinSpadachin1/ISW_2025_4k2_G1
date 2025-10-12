import React, { createContext, useEffect, useState } from 'react';
import api, { saveToken, clearToken } from '../services/api';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('access_token'));
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Si ya hay token en localStorage, intentamos recuperar información mínima del usuario.
    // Este proyecto no tiene un endpoint de 'me', así que guardamos sólo el token y asumimos autenticación válida.
    if (token) {
      setUser({ email: null }); // placeholder: si hay endpoint /user/me, reemplazar por fetch real
    } else {
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
        // opcional: parsear JWT para obtener email/nombre si necesario
        try {
          const payload = JSON.parse(atob(res.access_token.split('.')[1]));
          setUser({ email: payload.sub || payload.email || null, raw: payload });
        } catch (e) {
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
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
