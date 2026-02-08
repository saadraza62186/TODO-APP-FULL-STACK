'use client'

import { useRouter, usePathname } from 'next/navigation'
import Link from 'next/link'

export function Header() {
  const router = useRouter()
  const pathname = usePathname()
  
  const userEmail = typeof window !== 'undefined' 
    ? localStorage.getItem('user_email') 
    : null

  function handleSignOut() {
    localStorage.clear()
    router.push('/signin')
  }

  const isActive = (path: string) => pathname === path

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-8">
            <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
            
            {/* Navigation Links */}
            {userEmail && (
              <nav className="flex items-center gap-4">
                <Link
                  href="/tasks"
                  className={`text-sm font-medium transition ${
                    isActive('/tasks')
                      ? 'text-blue-600'
                      : 'text-gray-700 hover:text-gray-900'
                  }`}
                >
                  📝 Tasks
                </Link>
                <Link
                  href="/chat"
                  className={`text-sm font-medium transition ${
                    isActive('/chat')
                      ? 'text-blue-600'
                      : 'text-gray-700 hover:text-gray-900'
                  }`}
                >
                  💬 AI Chat
                </Link>
              </nav>
            )}
          </div>
          
          <div className="flex items-center gap-4">
            {userEmail && (
              <span className="text-sm text-gray-600">{userEmail}</span>
            )}
            <button
              onClick={handleSignOut}
              className="text-sm font-medium text-gray-700 hover:text-gray-900"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
