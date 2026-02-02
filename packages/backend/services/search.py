"""
Search service for finding similar chunks.
Uses cosine similarity for vector matching.
"""
from backend.data.storage import get_all_chunks
from backend.services.embedding import cosine_similarity


async def search_similar_chunks(query_vector: list, limit: int = 3):
    """
    Finds the top 'limit' chunks most similar to the query vector.
    Searches both D1 and in-memory chunks.
    """
    all_chunks = await get_all_chunks()
    
    if not all_chunks:
        return []
    
    results = []
    for chunk in all_chunks:
        score = cosine_similarity(query_vector, chunk['vector'])
        results.append({
            "score": score,
            "chunk": chunk
        })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    top_matches = [item['chunk'] for item in results[:limit]]
    
    return top_matches