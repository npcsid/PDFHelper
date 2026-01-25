import { MessageSquare } from 'lucide-react'
import ChatInput from './chat-input'

export default function ChatPanel() {
  return (
    <div className="flex flex-col h-full bg-white relative">
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mb-6 text-gray-400">
          <MessageSquare size={32} />
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          Chat messages will be displayed here.
        </h3>
        <p className="text-gray-500 max-w-sm">
          Ask a question about your document to get started.
        </p>
      </div>

      <ChatInput />
    </div>
  )
}
