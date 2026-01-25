import { Paperclip, Send } from 'lucide-react'
import { Button } from './ui/button'

export default function ChatInput() {
  return (
    <div className="p-4 bg-white border-t border-gray-100">
      <div className="relative flex items-center bg-gray-50 rounded-lg border border-gray-200 focus-within:ring-2 focus-within:ring-gray-200 focus-within:border-transparent transition-all">
        <button
          className="p-3 text-gray-400 hover:text-gray-600 transition-colors"
          aria-label="Add attachment"
        >
          <Paperclip size={20} />
        </button>
        <input
          type="text"
          placeholder="Ask a question about your document..."
          className="flex-1 bg-transparent py-3 px-2 text-gray-900 placeholder:text-gray-400 focus:outline-none"
        />
        <div className="p-2">
          <Button
            variant="primary"
            size="sm"
            className="h-8 w-8 !p-0 rounded-full"
            aria-label="Send message"
          >
            <Send size={16} />
          </Button>
        </div>
      </div>
      <div className="flex items-center justify-end mt-2 px-1">
        <span className="text-xs text-gray-400">0/1000 characters</span>
      </div>
    </div>
  )
}
