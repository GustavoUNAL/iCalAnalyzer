from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from app.services.calendar_service import CalendarService
import pandas as pd

router = APIRouter()

@router.get("/calendars/", response_model=Dict[str, List[str]])
async def get_available_calendars(
    calendar_service: CalendarService = Depends(CalendarService)
):
    """Obtiene la lista de calendarios disponibles."""
    try:
        calendars = calendar_service.get_calendars()
        return {"calendars": calendars}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calendar/{calendar_name}/stats")
async def get_calendar_stats(
    calendar_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    calendar_service: CalendarService = Depends(CalendarService)
):
    """Obtiene estadísticas detalladas de un calendario específico."""
    try:
        # Convertir fechas
        if not start_date:
            start_date = datetime.now()
        else:
            start_date = datetime.fromisoformat(start_date)
        
        if not end_date:
            end_date = start_date + timedelta(days=7)
        else:
            end_date = datetime.fromisoformat(end_date)

        # Obtener eventos del calendario
        events = calendar_service.get_events(start_date, end_date)
        calendar_events = [e for e in events if e.calendar_name == calendar_name]
        
        if not calendar_events:
            return {
                "calendar_name": calendar_name,
                "total_events": 0,
                "total_hours": 0,
                "events_by_day": {},
                "most_common_events": {},
                "average_duration": 0
            }

        # Crear DataFrame para análisis
        df = pd.DataFrame([{
            'title': e.title,
            'start': e.start,
            'duration': e.duration,
            'day': e.start.strftime('%Y-%m-%d')
        } for e in calendar_events])

        # Análisis de datos
        events_by_day = df.groupby('day')['title'].count().to_dict()
        most_common_events = df['title'].value_counts().head(5).to_dict()
        
        return {
            "calendar_name": calendar_name,
            "total_events": len(df),
            "total_hours": float(df['duration'].sum()),
            "average_duration": float(df['duration'].mean()),
            "events_by_day": events_by_day,
            "most_common_events": most_common_events,
            "analysis": {
                "busiest_day": df.groupby('day')['title'].count().idxmax(),
                "average_events_per_day": len(df) / len(events_by_day),
                "total_days": len(events_by_day)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calendar/{calendar_name}/events")
async def get_calendar_events(
    calendar_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    calendar_service: CalendarService = Depends(CalendarService)
):
    """Obtiene todos los eventos de un calendario específico."""
    try:
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
        all_events = calendar_service.get_events(start_date, end_date)
        calendar_events = [e for e in all_events if e.calendar_name == calendar_name]
        
        return {
            "calendar_name": calendar_name,
            "events": [
                {
                    "title": e.title,
                    "start": e.start.isoformat(),
                    "end": e.end.isoformat(),
                    "duration": e.duration
                }
                for e in calendar_events
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))