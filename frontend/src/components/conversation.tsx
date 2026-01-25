import { FileText, Upload } from 'lucide-react'
import { Link } from '@tanstack/react-router'
import { Button } from './ui/button'

export default function StartConversation() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 animate-in fade-in zoom-in duration-500">
      <div className="mb-6">
        <div className="relative inline-flex items-center justify-center">
          <svg
            width="64"
            height="64"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="text-gray-900"
          >
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M8 10H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M8 14H12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </div>

      <h2 className="text-2xl font-bold text-gray-900 mb-2">
        Start New Conversation
      </h2>

      <p className="text-gray-500 mb-8 max-w-md mx-auto leading-relaxed">
        Start by uploading a new PDF or accessing your previous uploads.
      </p>

      <div className="flex flex-wrap items-center gap-4 justify-center">
        <Link to="/chat">
          <Button variant="primary" icon={<FileText size={18} />}>
            Documents
          </Button>
        </Link>
        <Link to="/chat">
          <Button variant="primary" icon={<Upload size={18} />}>
            Upload
          </Button>
        </Link>
      </div>
    </div >
  )
}
