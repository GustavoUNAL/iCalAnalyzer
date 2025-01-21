import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_analysis_figures(data):
    if not data or 'total_events' not in data:
        return html.Div("No hay datos disponibles", className="text-center p-4")

    # Eventos por calendario
    calendar_events = go.Figure(data=[
        go.Bar(
            x=[cal['calendar_name'] for cal in data['events_by_calendar']],
            y=[cal['total_events'] for cal in data['events_by_calendar']],
            marker_color='rgb(26, 118, 255)'
        )
    ])
    calendar_events.update_layout(
        title="Distribución de eventos por calendario",
        xaxis_title="Calendario",
        yaxis_title="Número de eventos",
        template='plotly_white'
    )

    # Horas por calendario
    calendar_hours = go.Figure(data=[
        go.Pie(
            labels=[cal['calendar_name'] for cal in data['events_by_calendar']],
            values=[cal['total_hours'] for cal in data['events_by_calendar']],
            hole=.3
        )
    ])
    calendar_hours.update_layout(
        title="Distribución de horas por calendario",
        template='plotly_white'
    )

    # Tarjetas de resumen general
    summary_cards = dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Eventos", className="card-title text-center"),
                    html.H2(f"{data['total_events']}", className="text-center")
                ])
            ])
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Horas", className="card-title text-center"),
                    html.H2(f"{data['total_hours']:.1f}", className="text-center")
                ])
            ])
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Día más ocupado", className="card-title text-center"),
                    html.H2(f"{data['busiest_day']}", className="text-center")
                ])
            ])
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Hora más activa", className="card-title text-center"),
                    html.H2(f"{data['busiest_hour']:02d}:00", className="text-center")
                ])
            ])
        )
    ])

    return html.Div([
        html.H3("Análisis General", className="text-center mb-4"),
        summary_cards,
        html.Div(className="mb-4"),  # Espaciador
        dbc.Row([
            dbc.Col(dcc.Graph(figure=calendar_events), md=6),
            dbc.Col(dcc.Graph(figure=calendar_hours), md=6)
        ])
    ])