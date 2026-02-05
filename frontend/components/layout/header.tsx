'use client'

import { useRouter } from 'next/navigation'

export function Header() {
  const router = useRouter()
  
  const userEmail = typeof window !== 'undefined' 
    ? localStorage.getItem('user_email') 
    : null

  function handleSignOut() {
    localStorage.clear()
    router.push('/signin')
  }

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
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
