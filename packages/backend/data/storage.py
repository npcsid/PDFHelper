DB_MEMORY = {
    "documents": {}, 
    "chunks": []
}

def add_chunk(text: str, vector: list, source_doc: str):
    """
    Save a chunk of text and its vector embedding to memory.
    """
    DB_MEMORY["chunks"].append({
        "text": text,
        "vector": vector,
        "source": source_doc
    })

def get_all_chunks():
    """
    Retrieve all chunks (for searching).
    """
    return DB_MEMORY["chunks"]