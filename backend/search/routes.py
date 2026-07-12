from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Dict, Any

from database.connection import get_session
from search.service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def global_search(
    q: str = Query(..., min_length=1, description="Search query string"),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    service = SearchService(session)
    results = service.global_search(q, limit)
    return {"success": True, "message": "Search completed successfully", "data": results}
