import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  team_id?: number;
  role: string;
  timezone: string;
  last_checkin?: string;
  current_streak: number;
  total_checkins: number;
}

const authApi = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await axios.post<AuthResponse>(`${API_URL}/auth/login`, formData);
    return response.data;
  },

  async register(data: RegisterData): Promise<User> {
    const response = await axios.post<User>(`${API_URL}/auth/register`, data);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No token found');
    }

    const response = await axios.get<User>(`${API_URL}/users/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  },

  setToken(token: string) {
    localStorage.setItem('token', token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  },

  removeToken() {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  },
};

// Add axios interceptor for token refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      authApi.removeToken();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default authApi; 