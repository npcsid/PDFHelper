import httpx
from backend.config import CF_ACCOUNT_ID, CF_API_TOKEN, D1_DATABASE_ID
from typing import Optional
import uuid
from datetime import datetime

D1_API_BASE = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{D1_DATABASE_ID}"

def _get_headers():
    """Get headers for D1 API requests."""
    return {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

async def execute_sql(sql: str, params: list = None) -> dict:
    """
    Execute a SQL query on D1.
    
    Args:
        sql: SQL query string
        params: Optional list of parameters for prepared statements
        
    Returns:
        API response dict
    """
    async with httpx.AsyncClient() as client:
        payload = {"sql": sql}
        if params:
            payload["params"] = params
            
        response = await client.post(
            f"{D1_API_BASE}/query",
            headers=_get_headers(),
            json=payload,
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()

async def init_schema():
    """
    Initialize the D1 database schema.
    Creates tables if they don't exist.
    """
    schema_sql = """
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        original_name TEXT NOT NULL,
        r2_key TEXT NOT NULL,
        r2_url TEXT NOT NULL,
        file_size INTEGER,
        mime_type TEXT DEFAULT 'application/pdf',
        user_id TEXT,
        chunks_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """
    await execute_sql(schema_sql)
    
    chunks_sql = """
    CREATE TABLE IF NOT EXISTS chunks (
        id TEXT PRIMARY KEY,
        document_id TEXT,
        text TEXT NOT NULL,
        embedding TEXT NOT NULL,
        chunk_index INTEGER,
        source_doc TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
    );
    """
    await execute_sql(chunks_sql)
    
    await execute_sql("CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);")
    await execute_sql("CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);")
    await execute_sql("CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);")
    
    print("D1 schema initialized")

async def save_document(
    filename: str,
    original_name: str,
    r2_key: str,
    r2_url: str,
    file_size: int,
    user_id: Optional[str] = None,
    mime_type: str = "application/pdf"
) -> dict:
    """
    Save document metadata to D1.
    
    Returns:
        Document record with ID
    """
    doc_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    sql = """
    INSERT INTO documents (id, filename, original_name, r2_key, r2_url, file_size, mime_type, user_id, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = [doc_id, filename, original_name, r2_key, r2_url, file_size, mime_type, user_id, now, now]
    
    await execute_sql(sql, params)
    
    return {
        "id": doc_id,
        "filename": filename,
        "original_name": original_name,
        "r2_key": r2_key,
        "r2_url": r2_url,
        "file_size": file_size,
        "mime_type": mime_type,
        "user_id": user_id,
        "status": "pending",
        "created_at": now
    }

async def update_document_status(doc_id: str, status: str, chunks_count: int = None) -> bool:
    """
    Update document processing status.
    
    Args:
        doc_id: Document ID
        status: New status ('pending', 'processed', 'error')
        chunks_count: Optional number of chunks processed
    """
    now = datetime.utcnow().isoformat()
    
    if chunks_count is not None:
        sql = "UPDATE documents SET status = ?, chunks_count = ?, updated_at = ? WHERE id = ?;"
        params = [status, chunks_count, now, doc_id]
    else:
        sql = "UPDATE documents SET status = ?, updated_at = ? WHERE id = ?;"
        params = [status, now, doc_id]
    
    await execute_sql(sql, params)
    return True

async def get_document(doc_id: str) -> Optional[dict]:
    """
    Get document by ID.
    """
    sql = "SELECT * FROM documents WHERE id = ?;"
    result = await execute_sql(sql, [doc_id])
    
    if result.get("result") and result["result"][0].get("results"):
        rows = result["result"][0]["results"]
        if rows:
            return rows[0]
    return None

async def get_user_documents(user_id: str) -> list:
    """
    Get all documents for a user.
    """
    sql = "SELECT * FROM documents WHERE user_id = ? ORDER BY created_at DESC;"
    result = await execute_sql(sql, [user_id])
    
    if result.get("result") and result["result"][0].get("results"):
        return result["result"][0]["results"]
    return []

async def delete_document(doc_id: str) -> bool:
    """
    Delete document record.
    """
    sql = "DELETE FROM documents WHERE id = ?;"
    await execute_sql(sql, [doc_id])
    return True

async def save_chunk(
    text: str,
    embedding: list,
    source_doc: str,
    document_id: Optional[str] = None,
    chunk_index: int = 0
) -> dict:
    """
    Save a chunk with its embedding to D1.
    
    Args:
        text: The chunk text
        embedding: Vector embedding as a list
        source_doc: Source document filename
        document_id: Optional document ID for association
        chunk_index: Position of chunk in document
        
    Returns:
        Chunk record with ID
    """
    import json
    
    chunk_id = str(uuid.uuid4())
    embedding_json = json.dumps(embedding)
    now = datetime.utcnow().isoformat()
    
    sql = """
    INSERT INTO chunks (id, document_id, text, embedding, chunk_index, source_doc, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = [chunk_id, document_id, text, embedding_json, chunk_index, source_doc, now]
    
    await execute_sql(sql, params)
    
    return {
        "id": chunk_id,
        "document_id": document_id,
        "text": text,
        "chunk_index": chunk_index,
        "source_doc": source_doc
    }


async def get_chunks_by_document(document_id: str) -> list:
    """
    Get all chunks for a specific document.
    """
    import json
    
    sql = "SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_index;"
    result = await execute_sql(sql, [document_id])
    
    if result.get("result") and result["result"][0].get("results"):
        chunks = result["result"][0]["results"]
        for chunk in chunks:
            if chunk.get("embedding"):
                chunk["embedding"] = json.loads(chunk["embedding"])
        return chunks
    return []


async def get_all_chunks() -> list:
    """
    Get all chunks from D1 for search.
    Returns chunks with parsed embeddings.
    """
    import json
    
    sql = "SELECT id, document_id, text, embedding, source_doc FROM chunks;"
    result = await execute_sql(sql)
    
    if result.get("result") and result["result"][0].get("results"):
        chunks = result["result"][0]["results"]
        parsed_chunks = []
        for chunk in chunks:
            if chunk.get("embedding"):
                parsed_chunks.append({
                    "text": chunk["text"],
                    "vector": json.loads(chunk["embedding"]),
                    "source": chunk["source_doc"]
                })
        return parsed_chunks
    return []


async def delete_chunks_by_document(document_id: str) -> bool:
    """
    Delete all chunks for a document.
    """
    sql = "DELETE FROM chunks WHERE document_id = ?;"
    await execute_sql(sql, [document_id])
    return True
