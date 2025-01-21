from fastapi import APIRouter, Depends
from typing import Optional
from datetime import datetime, timedelta
from app.services.calendar_service import CalendarService
from collections import Counter
import pandas as pd

router = APIRouter()

@router.get("/productive-hours/")
async def get_productive_hours(
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
    
    if not events:
        return {
            "most_productive_hours": {},
            "total_active_hours": 0,
            "peak_productivity_time": None,
            "daily_distribution": {}
        }

    # Crear DataFrame para análisis
    df = pd.DataFrame([{
        'start_hour': e.start.hour,
        'end_hour': e.end.hour,
        'duration': e.duration,
        'day': e.start.strftime('%A'),
        'date': e.start.strftime('%Y-%m-%d')
    } for e in events])

    # Analizar horas productivas
    hours_data = []
    for _, row in df.iterrows():
        hours_data.extend(range(row['start_hour'], row['end_hour'] + 1))
    
    hour_counts = Counter(hours_data)
    
    # Encontrar la hora más productiva
    peak_hour = max(hour_counts.items(), key=lambda x: x[1])[0]
    
    # Distribución diaria
    daily_distribution = df.groupby('day')['duration'].sum().to_dict()

    return {
        "most_productive_hours": dict(sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)),
        "total_active_hours": len(set(hours_data)),
        "peak_productivity_time": f"{peak_hour:02d}:00",
        "daily_distribution": daily_distribution,
        "total_events": len(df),
        "average_duration": df['duration'].mean(),
        "total_hours_tracked": df['duration'].sum()
    }