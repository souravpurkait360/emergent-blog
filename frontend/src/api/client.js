/**
 * Axios client configured for cookie-based JWT authentication.
 *
 * withCredentials: true ensures httpOnly cookies are sent on every request.
 * No token is stored in JavaScript – the browser handles cookie transmission.
 */
import axios from 'axios';

const API_URL = `${process.env.REACT_APP_BACKEND_URL}/api`;

const client = axios.create({
  baseURL: API_URL,
  withCredentials: true, // required for httpOnly cookie auth
});

/** Attempt silent token refresh on 401, then retry once. */
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        await client.post('/auth/token/refresh/');
        return client(originalRequest);
      } catch {
        // Refresh failed – redirect to login
        if (typeof window !== 'undefined') {
          window.location.href = '/auth';
        }
      }
    }
    return Promise.reject(error);
  },
);

export default client;
export const API_BASE = API_URL;
