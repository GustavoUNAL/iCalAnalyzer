# 1. Ruta Base (Health Check)

GET http://localhost:8000/
GET http://localhost:8000/health

# 2. Análisis General

GET http://localhost:8000/api/v1/analysis/

# Ejemplos:
# Sin parámetros (usa período por defecto de una semana)
http://localhost:8000/api/v1/analysis/

# Con período específico
http://localhost:8000/api/v1/analysis/?period=week
http://localhost:8000/api/v1/analysis/?period=day
http://localhost:8000/api/v1/analysis/?period=month

# Con fechas específicas
http://localhost:8000/api/v1/analysis/?start_date=2024-01-01&end_date=2024-01-31

# Combinando parámetros
http://localhost:8000/api/v1/analysis/?start_date=2024-01-01&end_date=2024-01-31&period=week

3. Estadísticas por Calendario

GET http://localhost:8000/api/v1/calendar/{calendar_name}/stats

# Ejemplos:
http://localhost:8000/api/v1/calendar/VLESIM/stats
http://localhost:8000/api/v1/calendar/Personal/stats
http://localhost:8000/api/v1/calendar/Health/stats

# Con fechas específicas
http://localhost:8000/api/v1/calendar/VLESIM/stats?start_date=2024-01-01&end_date=2024-01-31

4. Horas Productivas

GET http://localhost:8000/api/v1/productive-hours/

# Ejemplos:
# Sin parámetros (usa período por defecto)
http://localhost:8000/api/v1/productive-hours/

# Con fechas específicas
http://localhost:8000/api/v1/productive-hours/?start_date=2024-01-01&end_date=2024-01-31