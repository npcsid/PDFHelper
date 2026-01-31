import { FileText, Upload, Loader2, CheckCircle, AlertCircle, Cloud } from 'lucide-react'
import { Link } from '@tanstack/react-router'
import { Button } from './ui/button'
import { useState, useRef } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { set } from 'idb-keyval'

export default function StartConversation() {
  // Local upload states
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Cloud upload states
  const [isCloudUploading, setIsCloudUploading] = useState(false)
  const [cloudUploadStatus, setCloudUploadStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const cloudFileInputRef = useRef<HTMLInputElement>(null)

  const navigate = useNavigate()

  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  const handleCloudUploadClick = () => {
    cloudFileInputRef.current?.click()
  }

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    setUploadStatus('idle')

    const formData = new FormData()
    formData.append('file', file)

    try {
      // Store file locally first
      await set(file.name, file)

      const response = await fetch('http://localhost:8000/api/v1/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      setUploadStatus('success')
      // Optional: Navigate to chat after a brief delay
      setTimeout(() => {
        navigate({
          to: '/chat',
          search: { file: file.name }
        })
      }, 1500)

    } catch (error) {
      console.error('Upload error:', error)
      setUploadStatus('error')
    } finally {
      setIsUploading(false)
    }
  }

  const handleCloudFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setIsCloudUploading(true)
    setCloudUploadStatus('idle')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/api/v1/upload/cloud', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Cloud upload failed')
      }

      const result = await response.json() as { url: string }
      setCloudUploadStatus('success')

      setTimeout(() => {
        navigate({
          to: '/chat',
          search: { file: file.name, source: 'cloud', url: result.url }
        })
      }, 1500)

    } catch (error) {
      console.error('Cloud upload error:', error)
      setCloudUploadStatus('error')
    } finally {
      setIsCloudUploading(false)
    }
  }

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

        <input
          type="file"
          accept=".pdf"
          ref={fileInputRef}
          className="hidden"
          onChange={handleFileChange}
        />

        <Button
          variant="primary"
          icon={isUploading ? <Loader2 className="animate-spin" size={18} /> : <Upload size={18} />}
          onClick={handleUploadClick}
          disabled={isUploading}
        >
          {isUploading ? 'Uploading...' : 'Upload PDF'}
        </Button>

        <input
          type="file"
          accept=".pdf"
          ref={cloudFileInputRef}
          className="hidden"
          onChange={handleCloudFileChange}
        />

        <button
          className="inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed bg-sky-500 text-white hover:bg-sky-600 focus:ring-sky-500 h-10 px-4 text-sm"
          onClick={handleCloudUploadClick}
          disabled={isCloudUploading}
        >
          <span className="mr-2">
            {isCloudUploading ? <Loader2 className="animate-spin" size={18} /> : <Cloud size={18} />}
          </span>
          {isCloudUploading ? 'Uploading to Cloud...' : 'Upload to Cloud'}
        </button>
      </div>

      {uploadStatus === 'success' && (
        <div className="mt-4 text-green-600 flex items-center gap-2 animate-in fade-in slide-in-from-bottom-2">
          <CheckCircle size={18} />
          <span>Upload successful! Redirecting...</span>
        </div>
      )}

      {uploadStatus === 'error' && (
        <div className="mt-4 text-red-600 flex items-center gap-2 animate-in fade-in slide-in-from-bottom-2">
          <AlertCircle size={18} />
          <span>Upload failed. Please try again.</span>
        </div>
      )}

      {cloudUploadStatus === 'success' && (
        <div className="mt-4 text-sky-600 flex items-center gap-2 animate-in fade-in slide-in-from-bottom-2">
          <CheckCircle size={18} />
          <span>Uploaded to cloud! Ready for processing...</span>
        </div>
      )}

      {cloudUploadStatus === 'error' && (
        <div className="mt-4 text-red-600 flex items-center gap-2 animate-in fade-in slide-in-from-bottom-2">
          <AlertCircle size={18} />
          <span>Cloud upload failed. Please try again.</span>
        </div>
      )}
    </div>
  )
}
