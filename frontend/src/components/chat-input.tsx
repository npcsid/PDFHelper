import { Paperclip, Send, Loader2 } from 'lucide-react'
import { Button } from './ui/button'
import { useState, KeyboardEvent } from 'react'

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

export default function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [message, setMessage] = useState('')

  const handleSend = () => {
    if (message.trim() && !isLoading) {
      onSend(message.trim())
      setMessage('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="p-4 bg-white border-t border-gray-100">
      <div className="relative flex items-center bg-gray-50 rounded-lg border border-gray-200 focus-within:ring-2 focus-within:ring-gray-200 focus-within:border-transparent transition-all">
        <button
          className="p-3 text-gray-400 hover:text-gray-600 transition-colors"
          aria-label="Add attachment"
          disabled={isLoading}
        >
          <Paperclip size={20} />
        </button>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your document..."
          disabled={isLoading}
          className="flex-1 bg-transparent py-3 px-2 text-gray-900 placeholder:text-gray-400 focus:outline-none disabled:opacity-50"
        />
        <div className="p-2">
          <Button
            variant="primary"
            size="sm"
            className="h-8 w-8 !p-0 rounded-full"
            aria-label="Send message"
            onClick={handleSend}
            disabled={!message.trim() || isLoading}
          >
            {isLoading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
          </Button>
        </div>
      </div>
      <div className="flex items-center justify-end mt-2 px-1">
        <span className="text-xs text-gray-400">{message.length}/1000 characters</span>
      </div>
    </div>
  )
}
