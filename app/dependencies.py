from fastapi import Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.chart import calculate_chart
from app.utils.geocoding import get_coordinates
from app.utils.timezone import get_timezone
from typing import Optional

# 템플릿 설정 공유
templates = Jinja2Templates(directory="app/templates")
templates.env.add_extension("jinja2.ext.do")

# Config Constants (For Context)
CONFIG_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
signSymbols = ['♈︎', '♉︎', '♊︎', '♋︎', '♌︎', '♍︎', '♎︎', '♏︎', '♐︎', '♑︎', '♒︎', '♓︎']

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChartInputData:
    def __init__(self, 
                 name: str, 
                 birth_date: str, 
                 birth_time: str, 
                 place_name: str, 
                 gender: str = "unknown"):
        self.name = name
        
        # Parse 8-digit date (YYYYMMDD -> YYYY-MM-DD)
        if len(birth_date) == 8 and birth_date.isdigit():
            self.birth_date = f"{birth_date[:4]}-{birth_date[4:6]}-{birth_date[6:]}"
        else:
            self.birth_date = birth_date
            
        # Parse 4-digit time (HHMM -> HH:MM)
        if len(birth_time) == 4 and birth_time.isdigit():
            self.birth_time = f"{birth_time[:2]}:{birth_time[2:]}"
        else:
            self.birth_time = birth_time
            
        self.place_name = place_name
        self.gender = gender
        self.lat = None
        self.lon = None
        self.tz = None

    async def resolve_location(self):
        """위경도 및 타임존 계산"""
        lat, lon = get_coordinates(self.place_name)
        if lat is None:
            raise HTTPException(status_code=400, detail="Invalid location")
        self.lat = lat
        self.lon = lon
        self.tz = get_timezone(lat, lon)

    def calculate(self):
        """차트 데이터 계산"""
        chart_data = calculate_chart(
            self.birth_date, 
            self.birth_time, 
            self.lat, 
            self.lon, 
            self.tz
        )
        chart_data['name'] = self.name
        chart_data['birth_date'] = self.birth_date
        chart_data['birth_time'] = self.birth_time
        
        return chart_data
