import { createFileRoute } from '@tanstack/react-router'
import ChatLayout from '../components/chat-layout'

export const Route = createFileRoute('/chat')({
  component: ChatLayout,
  validateSearch: (search: Record<string, unknown>): { file?: string; source?: string; url?: string } => {
    return {
      file: (search.file as string) || undefined,
      source: (search.source as string) || undefined,
      url: (search.url as string) || undefined,
    }
  },
})
