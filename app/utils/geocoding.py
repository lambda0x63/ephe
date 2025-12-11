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
    location = geolocator.geocode(place_name)
    
    if location is None:
        raise ValueError(f"Cannot find location: {place_name}")
    
    return (location.latitude, location.longitude)
