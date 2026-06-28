/**
 * authStore – Zustand store for authentication state.
 *
 * Tokens live ONLY in httpOnly cookies (set by Django).
 * No sensitive data is ever stored in localStorage or sessionStorage.
 * On init we call /api/auth/me/ – if the cookie is valid the user is restored.
 */
import { create } from 'zustand';
import client from '@/api/client';

const useAuthStore = create((set) => ({
  /** null = not logged in, undefined = hydrating */
  user: undefined,

  /** Call on app mount to restore session from httpOnly cookie. */
  init: async () => {
    try {
      const { data } = await client.get('/auth/me/');
      set({ user: data });
    } catch {
      set({ user: null });
    }
  },

  login: async (email, password) => {
    const { data } = await client.post('/auth/token/', { email, password });
    set({ user: data.user });
    return data.user;
  },

  register: async (userData) => {
    const { data } = await client.post('/auth/register/', userData);
    set({ user: data.user });
    return data.user;
  },

  logout: async () => {
    await client.post('/auth/logout/').catch(() => {});
    set({ user: null });
  },

  setUser: (user) => set({ user }),
}));

export default useAuthStore;
