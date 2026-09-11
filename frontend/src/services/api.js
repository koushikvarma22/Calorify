import axios from 'axios';

const rawBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const baseURL = rawBaseUrl.replace(/\/+$/, '');

const api = axios.create({
  baseURL,
  timeout: 60000,
  headers: { Accept: 'application/json' },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const message = error.response?.data?.error ||
      (status === 0 ? 'Could not reach the Calorify server.' : error.message) ||
      'Request failed';
    console.error(`[Calorify API ${status || ''}] ${message}`);
    return Promise.reject(error);
  }
);

export default api;
