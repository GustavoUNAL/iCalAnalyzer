# app/services/calendar_service.py
from typing import List
from datetime import datetime
import caldav
from app.core.config import get_settings
from app.models.schemas import Event

settings = get_settings()

class CalendarService:
    def __init__(self):
        self.client = caldav.DAVClient(
            url=settings.CALDAV_URL,
            username=settings.ICLOUD_USERNAME,
            password=settings.ICLOUD_APP_PASSWORD
        )

    def get_events(self, start_date: datetime, end_date: datetime) -> List[Event]:
        events = []
        principal = self.client.principal()
        calendars = principal.calendars()

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
                print(f"Error processing calendar {calendar.name}: {str(e)}")
                
        return events

    def get_calendars(self):
        principal = self.client.principal()
        return principal.calendars()