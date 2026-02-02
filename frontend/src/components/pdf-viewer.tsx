import {
  Minus,
  Plus,
  RotateCw,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'
import { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';

// Core PDF viewer styles
// import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
// import 'react-pdf/dist/esm/Page/TextLayer.css';

// Set worker source
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

interface PdfViewerProps {
  fileUrl?: string | null;
}

export default function PdfViewer({ fileUrl }: PdfViewerProps) {
  const [numPages, setNumPages] = useState<number | null>(null);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [scale, setScale] = useState<number>(1.0);
  const [rotation, setRotation] = useState<number>(0);

  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages);
    setPageNumber(1);
  }
  console.log('fileUrl: ', fileUrl)

  return (
    <div className="flex flex-col h-full bg-gray-100 border-r border-gray-200">
      <div className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-4 shadow-sm z-10">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <button
              className="p-1 hover:bg-gray-100 rounded text-gray-500"
              onClick={() => setScale(prev => Math.max(0.5, prev - 0.1))}
            >
              <Minus size={18} />
            </button>
            <div className="flex items-center gap-1 min-w-[60px] justify-center">
              <span className="text-sm font-medium text-gray-700">{Math.round(scale * 100)}%</span>
            </div>
            <button
              className="p-1 hover:bg-gray-100 rounded text-gray-500"
              onClick={() => setScale(prev => Math.min(2.0, prev + 0.1))}
            >
              <Plus size={18} />
            </button>
          </div>

          {numPages && (
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <button
                disabled={pageNumber <= 1}
                onClick={() => setPageNumber(prev => prev - 1)}
                className="disabled:opacity-50 hover:bg-gray-100 p-1 rounded"
              >
                <ChevronLeft size={16} />
              </button>
              <span>{pageNumber} / {numPages}</span>
              <button
                disabled={pageNumber >= numPages}
                onClick={() => setPageNumber(prev => prev + 1)}
                className="disabled:opacity-50 hover:bg-gray-100 p-1 rounded"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          <button
            className="p-2 hover:bg-gray-100 rounded text-gray-500"
            onClick={() => setRotation(prev => (prev + 90) % 360)}
          >
            <RotateCw size={18} />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-8 flex justify-center bg-gray-100 relative">
        {fileUrl ? (
          <div className="shadow-lg">
            <Document
              file={fileUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              className="flex flex-col items-center"
              loading={
                <div className="flex items-center justify-center p-10 text-gray-500">
                  Loading PDF...
                </div>
              }
              error={
                <div className="flex flex-col items-center justify-center min-h-[400px] text-red-500 bg-white p-8 rounded shadow">
                  <p>Failed to load PDF.</p>
                  <p className="text-xs mt-2 text-gray-400">URL: {fileUrl}</p>
                </div>
              }
            >
              <Page
                pageNumber={pageNumber}
                scale={scale}
                rotate={rotation}
                renderAnnotationLayer={false}
                renderTextLayer={false}
                className="bg-white"
              />
            </Document>
          </div>
        ) : (
          <div className="w-full max-w-3xl bg-white shadow-lg min-h-[600px] p-12 text-gray-800 flex flex-col items-center justify-center h-full">
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <div className="mb-4">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
              </div>
              <p className="text-lg font-medium">No PDF loaded</p>
              <p className="text-sm">Upload a document to view it here.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
