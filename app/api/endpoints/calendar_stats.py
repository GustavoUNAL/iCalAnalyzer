from fastapi import APIRouter, Depends
from typing import Optional
from datetime import datetime, timedelta
from app.services.calendar_service import CalendarService
import pandas as pd

router = APIRouter()

@router.get("/calendar/{calendar_name}/stats")
async def get_calendar_stats(
    calendar_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    calendar_service: CalendarService = Depends(CalendarService)
):
    # Convertir fechas
    if not start_date:
        start_date = datetime.now()
    else:
        start_date = datetime.fromisoformat(start_date)
    
    if not end_date:
        end_date = start_date + timedelta(days=7)
    else:
        end_date = datetime.fromisoformat(end_date)

    # Obtener eventos
    events = calendar_service.get_events(start_date, end_date)
    
    # Filtrar eventos del calendario específico
    calendar_events = [e for e in events if e.calendar_name == calendar_name]
    
    if not calendar_events:
        return {
            "calendar_name": calendar_name,
            "total_events": 0,
            "total_hours": 0,
            "events_by_day": {},
            "most_common_events": {}
        }

    # Crear DataFrame para análisis
    df = pd.DataFrame([{
        'title': e.title,
        'start': e.start,
        'duration': e.duration,
        'day': e.start.strftime('%Y-%m-%d')
    } for e in calendar_events])

    # Análisis
    events_by_day = df.groupby('day')['title'].count().to_dict()
    most_common_events = df['title'].value_counts().head(5).to_dict()

    return {
        "calendar_name": calendar_name,
        "total_events": len(df),
        "total_hours": df['duration'].sum(),
        "events_by_day": events_by_day,
        "most_common_events": most_common_events
    }