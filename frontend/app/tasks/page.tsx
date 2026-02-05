'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Task, TaskStatus, TaskSort, CreateTaskInput } from '@/types'
import { api } from '@/lib/api'
import { TaskList } from '@/components/tasks/task-list'
import { TaskForm } from '@/components/tasks/task-form'
import { Header } from '@/components/layout/header'
import { Modal } from '@/components/ui/modal'

export default function TasksPage() {
  const router = useRouter()
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [userId, setUserId] = useState<string | null>(null)
  const [filter, setFilter] = useState<TaskStatus>('all')
  const [sort, setSort] = useState<TaskSort>('created')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  // Check authentication
  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    const uid = localStorage.getItem('user_id')

    if (!token || !uid) {
      router.push('/signin')
      return
    }

    setUserId(uid)
    api.setToken(token)
  }, [router])

  // Fetch tasks
  useEffect(() => {
    if (!userId) return

    async function fetchTasks() {
      try {
        setLoading(true)
        const data = await api.getTasks(userId!, filter, sort)
        setTasks(data)
        setError('')
      } catch (err: any) {
        console.error('Error fetching tasks:', err)
        setError('Failed to load tasks')
        
        // If unauthorized, redirect to signin
        if (err.status === 401) {
          localStorage.clear()
          router.push('/signin')
        }
      } finally {
        setLoading(false)
      }
    }

    fetchTasks()
  }, [userId, filter, sort, router])

  async function handleCreateTask(data: CreateTaskInput) {
    if (!userId) return

    try {
      const newTask = await api.createTask(userId, data)
      setTasks([newTask, ...tasks])
      setShowCreateModal(false)
    } catch (err: any) {
      console.error('Error creating task:', err)
      throw err
    }
  }

  async function handleUpdateTask(taskId: number, data: CreateTaskInput) {
    if (!userId) return

    try {
      const updatedTask = await api.updateTask(userId, taskId, data)
      setTasks(tasks.map((t) => (t.id === taskId ? updatedTask : t)))
      setEditingTask(null)
    } catch (err: any) {
      console.error('Error updating task:', err)
      throw err
    }
  }

  async function handleToggleComplete(taskId: number, completed: boolean) {
    if (!userId) return

    try {
      const updatedTask = await api.toggleTaskCompletion(userId, taskId, completed)
      setTasks(tasks.map((t) => (t.id === taskId ? updatedTask : t)))
    } catch (err: any) {
      console.error('Error toggling task:', err)
      alert('Failed to update task')
    }
  }

  async function handleDeleteTask(taskId: number) {
    if (!userId) return
    if (!confirm('Are you sure you want to delete this task?')) return

    try {
      await api.deleteTask(userId, taskId)
      setTasks(tasks.filter((t) => t.id !== taskId))
    } catch (err: any) {
      console.error('Error deleting task:', err)
      alert('Failed to delete task')
    }
  }

  if (!userId) {
    return null // Will redirect in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Page Header */}
        <div className="px-4 sm:px-0 flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            + New Task
          </button>
        </div>

        {/* Filters */}
        <div className="px-4 sm:px-0 mb-6">
          <div className="flex gap-2">
            {(['all', 'pending', 'completed'] as TaskStatus[]).map((status) => (
              <button
                key={status}
                onClick={() => setFilter(status)}
                className={`px-4 py-2 text-sm font-medium rounded-md ${
                  filter === status
                    ? 'bg-primary-100 text-primary-700'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Task List */}
        <div className="px-4 sm:px-0">
          {error && (
            <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
              {error}
            </div>
          )}

          <TaskList
            tasks={tasks}
            loading={loading}
            onToggle={handleToggleComplete}
            onEdit={setEditingTask}
            onDelete={handleDeleteTask}
          />
        </div>
      </main>

      {/* Create Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Task"
      >
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowCreateModal(false)}
        />
      </Modal>

      {/* Edit Modal */}
      {editingTask && (
        <Modal
          isOpen={true}
          onClose={() => setEditingTask(null)}
          title="Edit Task"
        >
          <TaskForm
            task={editingTask}
            onSubmit={(data) => handleUpdateTask(editingTask.id, data)}
            onCancel={() => setEditingTask(null)}
          />
        </Modal>
      )}
    </div>
  )
}
