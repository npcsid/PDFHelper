"""
Storage layer for chunk data.
Wraps D1 database operations for persistent embedding storage.
"""
from backend.services.d1 import save_chunk as d1_save_chunk, get_all_chunks as d1_get_all_chunks

# Keep in-memory fallback for backward compatibility with local uploads
DB_MEMORY = {
    "documents": {}, 
    "chunks": []
}

async def add_chunk(text: str, vector: list, source_doc: str, document_id: str = None):
    """
    Save a chunk of text and its vector embedding.
    If document_id is provided, saves to D1 (cloud).
    Otherwise, saves to in-memory storage (local).
    """
    if document_id:
        # Save to D1 for cloud uploads
        chunk_index = len(DB_MEMORY["chunks"])  # Use current count as index
        await d1_save_chunk(
            text=text,
            embedding=vector,
            source_doc=source_doc,
            document_id=document_id,
            chunk_index=chunk_index
        )
    else:
        # Save to memory for local uploads (backward compatibility)
        DB_MEMORY["chunks"].append({
            "text": text,
            "vector": vector,
            "source": source_doc
        })


async def get_all_chunks():
    """
    Retrieve all chunks for searching.
    Combines both D1 chunks and in-memory chunks.
    """
    d1_chunks = await d1_get_all_chunks()
    
    all_chunks = d1_chunks + DB_MEMORY["chunks"]
    
    return all_chunks


def get_all_chunks_sync():
    """
    Synchronous version - returns only in-memory chunks.
    Used for backward compatibility.
    """
    return DB_MEMORY["chunks"]