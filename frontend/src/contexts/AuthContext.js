import React, { createContext, useContext, useState, useEffect } from 'react';
import client from '@/api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(undefined);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      client.get('/auth/me/')
        .then(r => setUser(r.data))
        .catch(() => { localStorage.clear(); setUser(null); });
    } else {
      setUser(null);
    }
  }, []);

  const login = async (email, password) => {
    const { data } = await client.post('/auth/token/', { email, password });
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    const me = await client.get('/auth/me/');
    setUser(me.data);
    return me.data;
  };

  const register = async (userData) => {
    const { data } = await client.post('/auth/register/', userData);
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    setUser(data.user);
    return data.user;
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
