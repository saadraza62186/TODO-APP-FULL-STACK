export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface CreateTaskInput {
  title: string
  description?: string
}

export interface UpdateTaskInput {
  title?: string
  description?: string
}

export interface ToggleCompleteInput {
  completed: boolean
}

export interface User {
  id: string
  email: string
  name?: string
}

export interface AuthSession {
  user: User
  token: string
}

export type TaskStatus = 'all' | 'pending' | 'completed'
export type TaskSort = 'created' | 'title' | 'updated'
