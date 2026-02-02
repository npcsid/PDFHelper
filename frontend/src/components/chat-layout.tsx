import { ArrowRight, Upload, Loader2 } from 'lucide-react'
import { Button } from './ui/button'
import ChatPanel from './chat-panel'
import { Link, useSearch } from '@tanstack/react-router'
import { Route as ChatRoute } from '../routes/chat'
import { lazy, Suspense, useEffect, useState } from 'react'
import { get } from 'idb-keyval'

const PdfViewer = lazy(() => import('./pdf-viewer'))

export default function ChatLayout() {
  const { file, source, url } = useSearch({ from: ChatRoute.id })
  const [fileUrl, setFileUrl] = useState<string | null>(null)
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
    let currentBlobUrl: string | null = null

    async function loadFile() {
      if (!file) {
        setFileUrl(null)
        return
      }

      if (source === 'cloud' && url) {
        const proxyUrl = `http://localhost:8000/api/v1/proxy-pdf?url=${encodeURIComponent(url)}`
        setFileUrl(proxyUrl)
        return
      }

      // 2. Try to get from IndexedDB (fastest for local uploads)
      try {
        const blob = await get(file)
        if (blob) {
          currentBlobUrl = URL.createObjectURL(blob)
          setFileUrl(currentBlobUrl)
          return
        }
      } catch (err) {
        console.warn("Failed to load PDF from IndexedDB storage:", err)
      }

      const backendUrl = `http://localhost:8000/uploads/${encodeURIComponent(file)}`
      setFileUrl(backendUrl)
    }
    loadFile()
    return () => {
      if (currentBlobUrl) {
        URL.revokeObjectURL(currentBlobUrl)
      }
    }
  }, [file, source, url])

  return (
    <div className="flex flex-col h-screen bg-gray-50 overflow-hidden font-sans">
      <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shrink-0 z-20 relative">
        <div className="flex items-center gap-2 font-bold text-xl text-gray-900">
          <div className="relative inline-flex items-center justify-center">
            <svg
              width="24"
              height="24"
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
          <span>PDFHelper</span>
        </div>

        <div className="flex items-center gap-4">
          <Button variant="primary" icon={<Upload size={16} />}>
            Upload
          </Button>
          <Link to="/" className="text-gray-600 hover:text-gray-900 text-sm font-medium flex items-center gap-1 transition-colors">
            Go to homepage
            <ArrowRight size={16} />
          </Link>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <div className="w-1/2 min-w-[400px]">
          {isClient ? (
            <Suspense fallback={
              <div className="flex items-center justify-center h-full text-gray-400">
                <Loader2 className="animate-spin" size={32} />
                <span className="ml-2">Loading Viewer...</span>
              </div>
            }>
              <PdfViewer fileUrl={fileUrl} />
            </Suspense>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <span className="ml-2">Initializing...</span>
            </div>
          )}
        </div>

        <div className="w-1/2 min-w-[400px]">
          <ChatPanel />
        </div>
      </div>
    </div>
  )
}
