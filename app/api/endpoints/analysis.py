# app/api/endpoints/analysis.py
from fastapi import APIRouter, Depends
from typing import Optional
from datetime import datetime, timedelta
from app.services.calendar_service import CalendarService
from app.models.schemas import TimeAnalysis, CalendarStats
import pandas as pd

router = APIRouter()

@router.get("/analysis/", response_model=TimeAnalysis)
async def get_analysis(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = "week",
    calendar_service: CalendarService = Depends(CalendarService)
):
    # Convertir fechas
    if not start_date:
        start_date = datetime.now()
    else:
        start_date = datetime.fromisoformat(start_date)
    
    if not end_date:
        if period == "day":
            end_date = start_date + timedelta(days=1)
        elif period == "week":
            end_date = start_date + timedelta(days=7)
        else:  # month
            end_date = start_date + timedelta(days=30)
    else:
        end_date = datetime.fromisoformat(end_date)

    # Obtener eventos
    events = calendar_service.get_events(start_date, end_date)
    
    # Crear DataFrame para análisis
    if not events:
        return TimeAnalysis(
            total_events=0,
            total_hours=0,
            events_by_calendar=[],
            most_common_duration=0,
            busiest_day="N/A",
            busiest_hour=0
        )

    df = pd.DataFrame([{
        'title': e.title,
        'start': e.start,
        'duration': e.duration,
        'calendar_name': e.calendar_name,
        'day_of_week': e.start.strftime('%A'),
        'hour': e.start.hour
    } for e in events])

    # Análisis por calendario
    calendar_stats = []
    for calendar_name in df['calendar_name'].unique():
        calendar_df = df[df['calendar_name'] == calendar_name]
        calendar_stats.append(CalendarStats(
            calendar_name=calendar_name,
            total_events=len(calendar_df),
            total_hours=calendar_df['duration'].sum(),
            average_duration=calendar_df['duration'].mean()
        ))

    return TimeAnalysis(
        total_events=len(df),
        total_hours=df['duration'].sum(),
        events_by_calendar=calendar_stats,
        most_common_duration=df['duration'].mode().iloc[0],
        busiest_day=df['day_of_week'].mode().iloc[0],
        busiest_hour=df['hour'].mode().iloc[0]
    )