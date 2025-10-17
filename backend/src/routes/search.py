"""
Search Routes - Candidates implement the service logic
These routes are complete, but call RetrievalService methods that need implementation
"""

from fastapi import APIRouter, HTTPException
from typing import List
from ..services.retrieval_service import retrieval_service
from ..types import SearchRequest, SearchResult

router = APIRouter(tags=["search"])


@router.post("/search", response_model=List[SearchResult])
async def search_documents(request: SearchRequest):
    """
    Search for documents based on a query.

    This endpoint is COMPLETE. Candidates implement the
    retrieval_service.search() method.

    The service should:
    - Generate embeddings for the query
    - Search vector database for similar chunks
    - Apply filters (folder_id, file_id) if provided
    - Return top N results with source attribution
    """
    try:
        results = await retrieval_service.search(request)
        return results
    except NotImplementedError as e:
        raise HTTPException(
            status_code=501,
            detail="Search functionality not yet implemented. Please implement retrieval_service.search()"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
