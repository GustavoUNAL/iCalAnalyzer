import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging
from dashboard.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class CalendarAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        """Método helper para hacer requests a la API."""
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error making request to {endpoint}: {str(e)}")
            return {}

    def get_calendars(self) -> Dict[str, list]:
        """Obtiene la lista de calendarios disponibles."""
        try:
            return self._make_request("calendars/")
        except Exception as e:
            logger.error(f"Error getting calendars: {str(e)}")
            return {"calendars": []}

    def get_analysis(self, start_date: Optional[str] = None, 
                    end_date: Optional[str] = None, 
                    period: str = "week") -> Dict:
        """Obtiene el análisis general del calendario."""
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "period": period
        }
        return self._make_request("analysis/", params=params)

    def get_calendar_stats(self, calendar_name: str,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> Dict:
        """Obtiene estadísticas de un calendario específico."""
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        return self._make_request(f"calendar/{calendar_name}/stats", params=params)

    def get_productive_hours(self, start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> Dict:
        """Obtiene análisis de horas productivas."""
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        return self._make_request("productive-hours/", params=params)

    def get_calendar_events(self, calendar_name: str,
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> Dict:
        """Obtiene eventos de un calendario específico."""
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        return self._make_request(f"calendar/{calendar_name}/events", params=params)

    def format_date(self, date: datetime) -> str:
        """Formatea una fecha para la API."""
        return date.isoformat() if date else None

    def get_date_range(self, period: str = "week") -> tuple:
        """Obtiene un rango de fechas basado en el período."""
        start_date = datetime.now()
        if period == "day":
            end_date = start_date + timedelta(days=1)
        elif period == "week":
            end_date = start_date + timedelta(days=7)
        elif period == "month":
            end_date = start_date + timedelta(days=30)
        else:
            end_date = start_date + timedelta(days=7)
        
        return self.format_date(start_date), self.format_date(end_date)