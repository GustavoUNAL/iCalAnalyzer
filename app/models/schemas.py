# app/models/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Event(BaseModel):
    title: str
    start: datetime
    end: datetime
    duration: float
    calendar_name: str

class CalendarStats(BaseModel):
    calendar_name: str
    total_events: int
    total_hours: float
    average_duration: float

class TimeAnalysis(BaseModel):
    total_events: int
    total_hours: float
    events_by_calendar: List[CalendarStats]
    most_common_duration: float
    busiest_day: str
    busiest_hour: int