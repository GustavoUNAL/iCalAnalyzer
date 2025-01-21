import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import logging

from dashboard.config import get_settings, setup_logging
from dashboard.utils.api_client import CalendarAPIClient
from dashboard.components.calendar_stats import create_calendar_stats_figures
from dashboard.components.productive_hours import create_productive_hours_figures
from dashboard.components.analysis import create_analysis_figures
from dashboard.components.layout import create_layout

# Configuración
settings = get_settings()
setup_logging(settings)
logger = logging.getLogger(__name__)

# Inicializar cliente API
api_client = CalendarAPIClient(base_url=settings.API_BASE_URL)

# Inicializar la aplicación Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Calendar Analytics Dashboard"
)

# Establecer el layout inicial
app.layout = create_layout()

# Callbacks para actualizar los datos
@app.callback(
    Output('calendar-select', 'options'),
    [Input('date-range', 'start_date')]
)
def update_calendar_options(start_date):
    try:
        response = api_client.get_calendars()
        calendars = response.get('calendars', [])
        return [{'label': cal, 'value': cal} for cal in calendars]
    except Exception as e:
        logger.error(f"Error updating calendar options: {str(e)}")
        return []

@app.callback(
    [Output('analysis-content', 'children'),
     Output('calendar-stats-content', 'children'),
     Output('productive-hours-content', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('calendar-select', 'value')]
)
def update_dashboard(start_date, end_date, selected_calendar):
    try:
        if not start_date or not end_date:
            raise ValueError("Please select valid dates")

        analysis_data = api_client.get_analysis(start_date, end_date)
        calendar_data = api_client.get_calendar_stats(selected_calendar, start_date, end_date)
        productive_data = api_client.get_productive_hours(start_date, end_date)

        analysis_content = create_analysis_figures(analysis_data)
        calendar_content = create_calendar_stats_figures(calendar_data)
        productive_content = create_productive_hours_figures(productive_data)

        return analysis_content, calendar_content, productive_content

    except Exception as e:
        logger.error(f"Error updating dashboard: {str(e)}")
        error_message = html.Div([
            html.H4("Error loading data", className="text-danger"),
            html.P(str(e))
        ])
        return error_message, error_message, error_message

def run_server():
    try:
        app.run_server(
            host=settings.DASH_HOST,
            port=settings.DASH_PORT,
            debug=settings.DASH_DEBUG
        )
    except Exception as e:
        logger.error(f"Error starting dashboard server: {str(e)}")
        raise

if __name__ == '__main__':
    run_server()