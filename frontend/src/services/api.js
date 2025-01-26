import axios from 'axios';

const API_URL = 'http://localhost:8000/api';  // Change this to your backend URL

// Helper to get the JWT token from localStorage
const getToken = () => localStorage.getItem('token');

// Create Axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add Authorization header with token for authenticated routes
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers['Authorization'] = `Token ${token}`; // Add the token to the header if available
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Sign up a new user (does not need authentication token)
export const signup = async (userData) => {
  const response = await axios.post('http://127.0.0.1:8000/api/signup/', userData);
  return response.data;  // Returning the response message or data from the backend
};

// Set token only for requests that require authentication
export const setAuthHeader = (token) => {
  api.defaults.headers['Authorization'] = `Token ${token}`; // Set the Authorization header for this request
};

// Remove the token from the headers when logging out or when not needed
export const removeAuthHeader = () => {
  delete api.defaults.headers['Authorization'];  // Remove the token from the header
};

// Login an existing user (get token and set it for future authenticated requests)
export const login = async (userData) => {
  const response = await axios.post('http://127.0.0.1:8000/api/login/', userData);
  
  
  const token = response.data.token;
  const user_id = response.data.user_id;
  localStorage.setItem('token', token);
  localStorage.setItem('user_id', user_id);
  
  // Set the token for authenticated requests
  setAuthHeader(token);

  return response.data;  // Returning the response message or data from the backend
};

// Fetch user profile (including preferences) - protected route
export const getUserProfile = async () => {
  const response = await api.get('/user_profile/');
  return response.data;
};

// Fetch recommended products based on user preferences - protected route
export const getProductRecommendations = async (userId) => {
  const response = await api.get(`/product_recommendations/${userId}/`);
  return response.data;
};

export default api;
