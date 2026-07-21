import axios from 'axios';

function resolveApiUrl() {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  const { hostname, protocol, host } = window.location;
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:9000';
  }
  // Direct EC2 IP access: UI on :3001, API on :9000
  if (/^\d{1,3}(\.\d{1,3}){3}$/.test(hostname)) {
    return `http://${hostname}:9000`;
  }
  // Domain access (e.g. testneo-ecom.testneo.ai): same origin /api → nginx → backend
  return `${protocol}//${host}/api`;
}

const API_URL = resolveApiUrl();

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/refresh`, { refresh_token: refreshToken });
          localStorage.setItem('access_token', response.data.access_token);
          error.config.headers.Authorization = `Bearer ${response.data.access_token}`;
          return api.request(error.config);
        } catch (err) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// Authentication
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/users/me'),
};

// Products
export const productsAPI = {
  getAll: (params = {}) => api.get('/products', { params }),
  getById: (id) => api.get(`/products/${id}`),
};

// Cart
export const cartAPI = {
  getCart: () => api.get('/cart'),
  addToCart: (data) => api.post('/cart', data),
  updateCartItem: (itemId, data) => api.put(`/cart/${itemId}`, data),
  removeFromCart: (itemId) => api.delete(`/cart/${itemId}`),
  clearCart: () => api.delete('/cart'),
};

// Orders
export const ordersAPI = {
  createOrder: (data) => api.post('/orders', data),
  getOrders: (params = {}) => api.get('/orders', { params }),
  getOrderById: (id) => api.get(`/orders/${id}`),
  cancelOrder: (id) => api.delete(`/orders/${id}`),
};

// Reviews
export const reviewsAPI = {
  createReview: (data) => api.post('/reviews', data),
  getProductReviews: (productId, params = {}) => api.get(`/reviews/${productId}`, { params }),
};

// Admin - Stats
export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  getRevenue: (params = {}) => api.get('/admin/stats/revenue', { params }),
};

// Admin - Products
export const adminProductsAPI = {
  createProduct: (data) => api.post('/products', data),
  updateProduct: (id, data) => api.put(`/products/${id}`, data),
  deleteProduct: (id) => api.delete(`/products/${id}`),
};

// Admin - Coupons
export const adminCouponsAPI = {
  list: (params = {}) => api.get('/coupons', { params }),
  create: (data) => api.post('/coupons', data),
  update: (id, data) => api.put(`/coupons/${id}`, data),
};

// Admin - Orders
export const adminOrdersAPI = {
  getAllOrders: (params = {}) => api.get('/orders', { params }),
  getOrder: (id) => api.get(`/orders/${id}`),
  updateOrder: (id, data) => api.put(`/orders/${id}`, data),
  cancelOrder: (id) => api.delete(`/admin/orders/${id}`),
};

// Admin - Users
export const adminUsersAPI = {
  getAllUsers: (params = {}) => api.get('/users', { params }),
  getUser: (id) => api.get(`/users/${id}`),
  updateUser: (id, data) => api.put(`/users/${id}`, data),
  deleteUser: (id) => api.delete(`/users/${id}`),
  createUser: (data) => api.post('/auth/register', data),
};

// Admin - Reviews
export const adminReviewsAPI = {
  getAllReviews: (params = {}) => api.get('/admin/reviews', { params }),
  approveReview: (id) => api.put(`/admin/reviews/${id}/approve`),
  rejectReview: (id) => api.put(`/admin/reviews/${id}/reject`),
  deleteReview: (id) => api.delete(`/admin/reviews/${id}`),
};

// Utility function to extract error message from API responses
export const extractErrorMessage = (error) => {
  // Handle axios errors
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail;
    if (Array.isArray(detail)) {
      // Handle Pydantic validation errors
      return detail.map(d => {
        if (typeof d === 'object' && d.msg) {
          return d.msg;
        } else if (typeof d === 'string') {
          return d;
        }
        return JSON.stringify(d);
      }).filter(Boolean).join(', ');
    } else if (typeof detail === 'string') {
      return detail;
    } else if (typeof detail === 'object') {
      // If detail is an object, try to extract a message
      return detail.message || detail.msg || JSON.stringify(detail);
    }
  }
  
  // Handle error message
  if (error.message && typeof error.message === 'string') {
    return error.message;
  }
  
  // Fallback
  return 'An unexpected error occurred';
};

export default api;

