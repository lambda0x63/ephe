"""도시명 → 좌표 변환 (Geocoding)"""
from geopy.geocoders import Nominatim


# 싱글톤으로 geolocator 재사용
_geolocator = None


def get_geolocator():
    global _geolocator
    if _geolocator is None:
        _geolocator = Nominatim(user_agent="natal-chart-api")
    return _geolocator


def geocode(place_name: str) -> tuple[float, float]:
    """
    도시명을 위도/경도로 변환
    
    Args:
        place_name: "Seoul, South Korea" 같은 도시명
        
    Returns:
        (latitude, longitude) 튜플
        
    Raises:
        ValueError: 위치를 찾을 수 없을 때
    """
    geolocator = get_geolocator()
    location = geolocator.geocode(place_name, timeout=10)
    
    if location is None:
        raise ValueError(f"Cannot find location: {place_name}")
    
    return (location.latitude, location.longitude)


def search_places(query: str) -> list[dict]:
    """
    도시명으로 장소 검색 (여러 결과 반환)
    
    Args:
        query: 검색어 (예: "daegu")
        
    Returns:
        [{"name": "...", "lat": ..., "lng": ...}, ...]
    """
    geolocator = get_geolocator()
    # exactly_one=False: 여러 결과 반환
    # limit=5: 최대 5개 결과
    locations = geolocator.geocode(query, exactly_one=False, limit=5, language="ko")
    
    if not locations:
        return []
        
    results = []
    for loc in locations:
        results.append({
            "name": loc.address,
            "display_name": loc.address.split(",")[0], # 간단한 이름
            "latitude": loc.latitude,
            "longitude": loc.longitude
        })
    return results
