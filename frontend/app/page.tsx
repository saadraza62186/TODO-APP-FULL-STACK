import { redirect } from 'next/navigation'

export default function HomePage() {
  // Redirect to tasks page (or signin if not authenticated)
  redirect('/tasks')
}
