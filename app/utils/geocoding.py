from geopy.geocoders import Nominatim
from typing import Optional, List, Tuple, Dict

# 초기화 (User-Agent 필수)
geolocator = Nominatim(user_agent="natal_chart_service")

def get_coordinates(place_name: str) -> Tuple[Optional[float], Optional[float]]:
    """
    장소 이름으로 위도, 경도 조회 (동기)
    """
    try:
        location = geolocator.geocode(place_name)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Geocoding Error: {e}")
        return None, None

def search_places(query: str) -> List[Dict[str, str]]:
    """
    장소 검색 및 자동완성 결과 반환
    """
    try:
        locations = geolocator.geocode(query, exactly_one=False, limit=5)
        if not locations:
            return []
        
        results = []
        for loc in locations:
            results.append({
                "display_name": loc.address,
                "lat": loc.latitude,
                "lon": loc.longitude
            })
        return results
    except Exception as e:
        print(f"Search Error: {e}")
        return []
