"""좌표 → 타임존 변환"""
from timezonefinder import TimezoneFinder


# 싱글톤으로 재사용 (초기화 비용이 큼)
_tf = None


def get_timezone_finder():
    global _tf
    if _tf is None:
        _tf = TimezoneFinder()
    return _tf


def get_timezone(latitude: float, longitude: float) -> str:
    """
    좌표로부터 타임존 문자열 반환
    
    Args:
        latitude: 위도
        longitude: 경도
        
    Returns:
        "Asia/Seoul" 같은 IANA 타임존 문자열
        
    Raises:
        ValueError: 타임존을 찾을 수 없을 때
    """
    tf = get_timezone_finder()
    tz = tf.timezone_at(lat=latitude, lng=longitude)
    
    if tz is None:
        raise ValueError(f"Cannot find timezone for coordinates: ({latitude}, {longitude})")
    
    return tz
