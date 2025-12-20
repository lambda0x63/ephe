from datetime import datetime

def parse_birth_datetime(date_str: str, time_str: str) -> datetime:
    """
    날짜와 시간을 파싱하여 datetime 객체 반환.
    HH:MM 형식이면 초(:00)를 자동으로 추가하여 처리.
    """
    if len(time_str.split(':')) == 2:
        time_str += ":00"
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
