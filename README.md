# PDFHelper

This repository contains a basic working PDF Helper/ PDF Chatbox clone

Frontend - React/Tanstack Start
Backend - Python/FastAPI

## System Architecture

The following flowchart describes the data flow from PDF upload to AI-powered chat response.

```mermaid
graph TD
    User([User])
    
    subgraph Frontend [Frontend - React / TanStack]
        UI[Chat Interface / Upload Button]
    end
    
    subgraph Backend [Backend - FastAPI]
        Router[API Router]
        PDFProc[PDF Processor]
        EmbedSvc[Embedding Service]
        LLMSvc[LLM Service]
        SearchSvc[Search Service]
    end
    
    subgraph Storage
        R2[(Cloudflare R2)]
        D1[(Cloudflare D1)]
        Memory[(In-Memory DB)]
    end
    
    User <--> UI
    UI -- "/upload (Local)" --> Router
    Router --> PDFProc
    PDFProc --> EmbedSvc
    EmbedSvc -- "Store Vectors" --> Memory
    
    UI -- "/upload/cloud" --> Router
    Router -- "PDF File" --> R2
    Router -- "Metadata" --> D1
    PDFProc -- "Chunks & Vectors" --> D1
    
    UI -- "/chat" --> Router
    Router --> EmbedSvc
    EmbedSvc -- "Query Vector" --> SearchSvc
    SearchSvc -- "Retrieve Context: Memory + D1" --> SearchSvc
    SearchSvc --> LLMSvc
    LLMSvc -- "Answer" --> Router
    Router -- "Response" --> UI
```

## Features
- **Local Upload**: Quick processing with in-memory storage.
- **Cloud Upload**: Persistent storage using Cloudflare R2 and D1.
- **RAG (Retrieval Augmented Generation)**: Intelligent context retrieval for accurate answers based on your documents.
