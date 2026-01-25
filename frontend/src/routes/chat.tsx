import { createFileRoute } from '@tanstack/react-router'
import ChatLayout from '../components/chat-layout'

export const Route = createFileRoute('/chat')({
  component: ChatLayout,
})
