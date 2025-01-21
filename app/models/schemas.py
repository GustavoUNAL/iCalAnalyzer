from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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
    total_events: int = 0
    total_hours: float = 0.0
    events_by_calendar: List[CalendarStats] = []
    most_common_duration: float = 0.0
    busiest_day: str = "N/A"
    busiest_hour: int = 0

class CalendarResponse(BaseModel):
    status: str
    calendars: List[str]

class EventAnalysis(BaseModel):
    events_by_day: dict
    most_common_events: dict
    total_events: int
    total_hours: float