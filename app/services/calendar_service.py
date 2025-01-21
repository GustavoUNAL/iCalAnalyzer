from typing import List
from datetime import datetime
import caldav
import logging
from app.core.config import get_settings
from app.models.schemas import Event

logger = logging.getLogger(__name__)
settings = get_settings()

class CalendarService:
    def __init__(self):
        self.settings = settings
        self.client = None
        self.principal = None

    def _ensure_connection(self):
        """Asegura que la conexión está establecida"""
        if not self.client:
            try:
                self.client = caldav.DAVClient(
                    url=self.settings.CALDAV_URL,
                    username=self.settings.ICLOUD_USERNAME,
                    password=self.settings.ICLOUD_APP_PASSWORD
                )
                self.principal = self.client.principal()
            except Exception as e:
                logger.error(f"Error connecting to CalDAV: {str(e)}")
                raise

    def get_events(self, start_date: datetime, end_date: datetime) -> List[Event]:
        try:
            self._ensure_connection()
            events = []
            calendars = self.principal.calendars()
            
            for calendar in calendars:
                try:
                    calendar_events = calendar.date_search(
                        start=start_date,
                        end=end_date
                    )
                    
                    for event in calendar_events:
                        event_data = event.instance.vevent
                        if hasattr(event_data, 'summary') and hasattr(event_data, 'dtstart') and hasattr(event_data, 'dtend'):
                            duration = (event_data.dtend.value - event_data.dtstart.value).total_seconds() / 3600
                            events.append(Event(
                                title=event_data.summary.value,
                                start=event_data.dtstart.value,
                                end=event_data.dtend.value,
                                duration=duration,
                                calendar_name=calendar.name
                            ))
                except Exception as e:
                    logger.error(f"Error processing calendar {calendar.name}: {str(e)}")
                    continue
                    
            return events
        except Exception as e:
            logger.error(f"Error getting events: {str(e)}")
            return []

    def get_calendars(self) -> List[str]:
        """Retorna la lista de nombres de calendarios disponibles"""
        try:
            self._ensure_connection()
            calendars = self.principal.calendars()
            return [cal.name for cal in calendars]
        except Exception as e:
            logger.error(f"Error getting calendars: {str(e)}")
            return []