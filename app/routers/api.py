from fastapi import APIRouter, Query
from app.utils.geocoding import search_places

router = APIRouter(prefix="/api/v1", tags=["API"])

@router.get("/search-place")
def search_place_api(query: str = Query(..., min_length=2)):
    """장소 검색 API (Nominatim)"""
    results = search_places(query)
    return {"results": results}
