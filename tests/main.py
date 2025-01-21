import caldav
from datetime import datetime, timedelta

# Conectar a iCloud
url = "https://caldav.icloud.com"
username = "gustavoarteaga0508@gmail.com"
password = "rbmh-lbha-cwci-lmaf"

client = caldav.DAVClient(url=url, username=username, password=password)
principal = client.principal()

# Obtener calendarios
calendars = principal.calendars()
# Imprimir información de cada calendario
print("\n=== INFORMACIÓN DE TODOS LOS CALENDARIOS ===")
for i, calendar in enumerate(calendars):
    print(f"\nCalendario {i+1}:")
    print(f"Nombre: {calendar.name}")
    print(f"URL: {calendar.url}")
    print(f"ID: {calendar.id}")
    
    # Obtener todos los eventos del calendario
    print("\nEventos:")
    try:
        # Obtener eventos desde hace un año hasta un año en el futuro
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now() + timedelta(days=7)
        
        events = calendar.date_search(
            start=start_date,
            end=end_date
        )
        
        if not events:
            print("No hay eventos en este calendario")
        
        for j, event in enumerate(events):
            print(f"\nEvento {j+1}:")
            try:
                # Intentar obtener propiedades específicas del evento
                event_data = event.instance.vevent
                print(f"Título: {event_data.summary.value if hasattr(event_data, 'summary') else 'Sin título'}")
                print(f"Inicio: {event_data.dtstart.value if hasattr(event_data, 'dtstart') else 'Sin fecha de inicio'}")
                print(f"Fin: {event_data.dtend.value if hasattr(event_data, 'dtend') else 'Sin fecha de fin'}")
                print(f"Ubicación: {event_data.location.value if hasattr(event_data, 'location') else 'Sin ubicación'}")
                print(f"Descripción: {event_data.description.value if hasattr(event_data, 'description') else 'Sin descripción'}")
            except Exception as e:
                print(f"Error al procesar evento: {str(e)}")
                print("Datos raw del evento:")
                print(event.data)
                
    except Exception as e:
        print(f"Error al obtener eventos: {str(e)}")

print("\n=== FIN DEL REPORTE ===")