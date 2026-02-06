import type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  ToggleCompleteInput,
  TaskStatus,
  TaskSort,
} from '@/types'
import { getErrorMessage } from './utils'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://todo-app-full-stack-tgfk.vercel.app'

/**
 * API client for backend communication
 */
class ApiClient {
  private baseUrl: string
  private token: string | null = null

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  /**
   * Set JWT token for authenticated requests
   */
  setToken(token: string | null) {
    this.token = token
  }

  /**
   * Get authorization headers
   */
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    return headers
  }

  /**
   * Handle API response
   */
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      const error = new Error(errorData.detail || response.statusText)
      ;(error as any).status = response.status
      ;(error as any).response = { data: errorData }
      throw error
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return null as T
    }

    return response.json()
  }

  /**
   * GET request
   */
  private async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'GET',
      headers: this.getHeaders(),
    })
    return this.handleResponse<T>(response)
  }

  /**
   * POST request
   */
  private async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    })
    return this.handleResponse<T>(response)
  }

  /**
   * PUT request
   */
  private async put<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    })
    return this.handleResponse<T>(response)
  }

  /**
   * PATCH request
   */
  private async patch<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'PATCH',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    })
    return this.handleResponse<T>(response)
  }

  /**
   * DELETE request
   */
  private async delete<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    })
    return this.handleResponse<T>(response)
  }

  // Task API methods

  /**
   * Get all tasks for user
   */
  async getTasks(
    userId: string,
    status: TaskStatus = 'all',
    sort: TaskSort = 'created'
  ): Promise<Task[]> {
    const params = new URLSearchParams({ status, sort })
    return this.get<Task[]>(`/api/${userId}/tasks?${params}`)
  }

  /**
   * Get single task
   */
  async getTask(userId: string, taskId: number): Promise<Task> {
    return this.get<Task>(`/api/${userId}/tasks/${taskId}`)
  }

  /**
   * Create new task
   */
  async createTask(userId: string, data: CreateTaskInput): Promise<Task> {
    return this.post<Task>(`/api/${userId}/tasks`, data)
  }

  /**
   * Update task
   */
  async updateTask(
    userId: string,
    taskId: number,
    data: UpdateTaskInput
  ): Promise<Task> {
    return this.put<Task>(`/api/${userId}/tasks/${taskId}`, data)
  }

  /**
   * Delete task
   */
  async deleteTask(userId: string, taskId: number): Promise<void> {
    return this.delete<void>(`/api/${userId}/tasks/${taskId}`)
  }

  /**
   * Toggle task completion
   */
  async toggleTaskCompletion(
    userId: string,
    taskId: number,
    completed: boolean
  ): Promise<Task> {
    return this.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      completed,
    })
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<any> {
    return this.get<any>('/health')
  }

  // Authentication API methods

  /**
   * Sign up new user
   */
  async signUp(email: string, password: string, name?: string): Promise<{
    access_token: string
    token_type: string
    user_id: string
    email: string
    name?: string
  }> {
    return this.post<any>('/api/auth/signup', { email, password, name })
  }

  /**
   * Sign in existing user
   */
  async signIn(email: string, password: string): Promise<{
    access_token: string
    token_type: string
    user_id: string
    email: string
    name?: string
  }> {
    return this.post<any>('/api/auth/signin', { email, password })
  }
}

// Export singleton instance
export const api = new ApiClient(API_BASE_URL)

// Export for setting token
export { ApiClient }
