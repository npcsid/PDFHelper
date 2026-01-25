import { createFileRoute } from '@tanstack/react-router'
import StartConversation from '../components/conversation'

export const Route = createFileRoute('/')({ component: App })

function App() {
  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      <StartConversation />
    </div>
  )
}
