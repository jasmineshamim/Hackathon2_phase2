// Define types
export type Task = {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
};

export type TaskCreate = {
  title: string;
  description?: string;
  completed?: boolean;
};

export type TaskUpdate = {
  title?: string;
  description?: string;
  completed?: boolean;
};

export type LoginResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

export type RegisterRequest = {
  email: string;
  password: string;
  name: string;
};

export type TaskStatistics = {
  total_count: number;
  pending_count: number;
  completed_count: number;
};

// API client for task operations
class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    // Get token from localStorage only on client-side
    let token: string | null = null;
    if (typeof window !== 'undefined') {
      token = localStorage.getItem('accessToken');
    }

    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    };

    // Log the request for debugging
    console.log(`API Request: ${options.method || 'GET'} ${this.baseUrl}${endpoint}`, { hasToken: !!token });

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    // Check if it's an authentication error
    if (response.status === 401 || response.status === 403) {
      const errorData = await response.json().catch(() => ({}));
      const errorDetail = typeof errorData.detail === 'string'
        ? errorData.detail
        : JSON.stringify(errorData.detail || 'Unauthorized');

      console.error(`Auth Error: ${errorDetail}`, { endpoint, status: response.status });

      // Clear invalid tokens
      if (typeof window !== 'undefined') {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
      }

      // Redirect to login
      window.location.href = '/auth/signin';
      throw new Error(errorDetail);
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorDetail = typeof errorData.detail === 'string'
        ? errorData.detail
        : (errorData.detail ? JSON.stringify(errorData.detail) : `API request failed: ${response.status} - ${response.statusText}`);

      console.error(`API Error: ${errorDetail}`, { endpoint, status: response.status });
      throw new Error(errorDetail);
    }

    // Handle responses that don't have JSON bodies (like DELETE)
    if (response.status === 204) {
      return undefined as T;
    }

    const data = await response.json();
    console.log(`API Response: ${endpoint}`, data);
    return data;
  }

  // Task operations
  async getTasks(): Promise<Task[]> {
    return this.request<Task[]>('/tasks/');
  }

  async createTask(task: TaskCreate): Promise<Task> {
    return this.request<Task>('/tasks/', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async getTaskById(id: number): Promise<Task> {
    return this.request<Task>(`/tasks/${id}`);
  }

  async updateTask(id: number, task: TaskUpdate): Promise<Task> {
    return this.request<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(task),
    });
  }

  async deleteTask(id: number): Promise<void> {
    return this.request<void>(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(id: number, completed: boolean): Promise<Task> {
    return this.request<Task>(`/tasks/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }

  async getTaskStatistics(): Promise<TaskStatistics> {
    return this.request<TaskStatistics>('/tasks/statistics');
  }

  // Auth operations
  async register(userData: RegisterRequest): Promise<LoginResponse> {
    return this.request<LoginResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: { email: string; password: string }): Promise<LoginResponse> {
    return this.request<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async logout() {
    // Clear tokens from localStorage if available (client-side only)
    if (typeof window !== 'undefined') {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  }

  isAuthenticated(): boolean {
    // Check if running on client-side before accessing localStorage
    if (typeof window !== 'undefined') {
      return !!localStorage.getItem('accessToken');
    }
    return false; // Server-side always returns false
  }
}

export const apiClient = new ApiClient();