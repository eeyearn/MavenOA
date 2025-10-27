"""
Search Tool - Document search implementation

This tool handles the core search functionality:
- Query embedding generation
- Vector database search
- Metadata filtering
- Result formatting
"""

from typing import List, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from ..types import SearchRequest, SearchResult, DriveFile

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize ChromaDB client (persistent)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Get or create collection
try:
    collection = chroma_client.get_collection(name="drive_documents")
except:
    collection = chroma_client.create_collection(
        name="drive_documents",
        metadata={"hnsw:space": "cosine"}
    )


def generate_query_embedding(query: str) -> List[float]:
    """Generate embedding for a search query using OpenAI."""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    return response.data[0].embedding


async def search_documents(
    query: str,
    folder_id: Optional[str] = None,
    file_id: Optional[str] = None,
    limit: int = 10
) -> List[SearchResult]:
    """
    Search for documents using semantic search.

    Args:
        query: Search query text
        folder_id: Optional folder to restrict search
        file_id: Optional specific file to search within
        limit: Maximum number of results to return

    Returns:
        List of SearchResult with relevance scores and snippets
    """
    try:
        # Step 1: Generate embedding for the query
        query_embedding = generate_query_embedding(query)
        
        # Step 2: Build metadata filter if needed. Prioritize file_id if both are present.
        where_filter = {}
        if file_id:
            where_filter["file_id"] = file_id
        elif folder_id:
            where_filter["folder_id"] = folder_id
        
        # Step 3: Query the vector database
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=50,  # Increase n_results to get a larger pool for filtering
            where=where_filter if where_filter else None
        )
        
        # Step 4: Format results
        search_results = []
        
        if results and results['ids'] and len(results['ids'][0]) > 0:
            ids = results['ids'][0]
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]

            for i in range(len(ids)):
                # Highlights are now optional but good to have
                highlights = extract_highlights(documents[i], query)
                
                search_results.append(SearchResult(
                    id=ids[i],
                    score=1 - distances[i],  # Convert distance to similarity score
                    text=documents[i],
                    metadata=metadatas[i],
                    highlights=highlights
                ))
        
        print(f"Found {len(search_results)} relevant sources")
        # Sort results by score in descending order and take the top 'limit'
        return sorted(search_results, key=lambda r: r.score, reverse=True)[:limit]
    
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return []


def extract_highlights(text: str, query: str, max_highlights: int = 3) -> List[str]:
    """
    Extract relevant highlights from text based on query.
    
    Args:
        text: The full text to extract highlights from
        query: The search query
        max_highlights: Maximum number of highlights to return
        
    Returns:
        List of highlight strings
    """
    # Split text into sentences
    sentences = text.replace('\n', ' ').split('. ')
    
    # Find sentences that contain query terms (case-insensitive)
    query_terms = query.lower().split()
    highlights = []
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        # Check if any query term is in the sentence
        if any(term in sentence_lower for term in query_terms):
            # Clean up and add
            highlight = sentence.strip()
            if highlight and len(highlight) > 10:  # Avoid very short fragments
                highlights.append(highlight)
                if len(highlights) >= max_highlights:
                    break
    
    return highlights[:max_highlights]
