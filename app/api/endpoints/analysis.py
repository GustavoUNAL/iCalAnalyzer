from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from typing import Optional
from app.services.calendar_service import CalendarService
from app.models.schemas import TimeAnalysis, CalendarResponse
import pandas as pd

router = APIRouter()

@router.get("/analysis/", response_model=TimeAnalysis)
async def get_analysis(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = "week",
    calendar_service: CalendarService = Depends(CalendarService)
):
    try:
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
        
        if not events:
            return TimeAnalysis()

        # Crear DataFrame para análisis
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
            calendar_stats.append({
                "calendar_name": calendar_name,
                "total_events": len(calendar_df),
                "total_hours": float(calendar_df['duration'].sum()),
                "average_duration": float(calendar_df['duration'].mean())
            })

        return TimeAnalysis(
            total_events=len(df),
            total_hours=float(df['duration'].sum()),
            events_by_calendar=calendar_stats,
            most_common_duration=float(df['duration'].mode().iloc[0] if not df.empty else 0),
            busiest_day=df['day_of_week'].mode().iloc[0] if not df.empty else "N/A",
            busiest_hour=int(df['hour'].mode().iloc[0] if not df.empty else 0)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-connection/", response_model=CalendarResponse)
async def test_connection(calendar_service: CalendarService = Depends(CalendarService)):
    try:
        calendars = calendar_service.get_calendars()
        return CalendarResponse(status="success", calendars=calendars)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))