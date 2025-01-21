# test_icloud.py
import caldav
from datetime import datetime, timedelta

url = "https://caldav.icloud.com"
username = "gustavoarteaga0508@gmail.com"
password = "rbmh-lbha-cwci-lmaf"

try:
    client = caldav.DAVClient(url=url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()
    print(f"Conexión exitosa! Encontrados {len(calendars)} calendarios:")
    for cal in calendars:
        print(f"- {cal.name}")
except Exception as e:
    print(f"Error: {str(e)}")