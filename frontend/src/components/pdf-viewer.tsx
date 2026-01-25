import {
  ChevronDown,
  Minus,
  Plus,
  Printer,
  RotateCw,
  Search,
} from 'lucide-react'

export default function PdfViewer() {
  return (
    <div className="flex flex-col h-full bg-gray-100 border-r border-gray-200">
      <div className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-4 shadow-sm z-10">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <button className="p-1 hover:bg-gray-100 rounded text-gray-500">
              <Minus size={18} />
            </button>
            <div className="flex items-center gap-1">
              <span className="text-sm font-medium text-gray-700">120%</span>
              <ChevronDown size={14} className="text-gray-500" />
            </div>
            <button className="p-1 hover:bg-gray-100 rounded text-gray-500">
              <Plus size={18} />
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button className="p-2 hover:bg-gray-100 rounded text-gray-500">
            <RotateCw size={18} />
          </button>
          <button className="p-2 hover:bg-gray-100 rounded text-gray-500">
            <Printer size={18} />
          </button>
          <button className="p-2 hover:bg-gray-100 rounded text-gray-500">
            <Search size={18} />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-8 flex justify-center">
        <div className="w-full max-w-3xl bg-white shadow-lg min-h-[800px] p-12 text-gray-800">
          <div className="flex flex-col items-center justify-center h-full min-h-[600px] text-gray-400">
            <div className="mb-4">
              <svg
                width="64"
                height="64"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
            </div>
            <p className="text-lg font-medium">No PDF loaded</p>
            <p className="text-sm">Upload a document to view it here.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
