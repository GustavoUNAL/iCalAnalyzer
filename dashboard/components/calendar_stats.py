import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_calendar_stats_figures(data):
    if not data or 'events_by_day' not in data:
        return html.Div("No hay datos disponibles", className="text-center p-4")

    # Eventos por día
    events_by_day = go.Figure(data=[
        go.Bar(
            x=list(data['events_by_day'].keys()),
            y=list(data['events_by_day'].values()),
            marker_color='rgb(55, 83, 109)'
        )
    ])
    events_by_day.update_layout(
        title="Eventos por día",
        xaxis_title="Fecha",
        yaxis_title="Número de eventos",
        template='plotly_white',
        height=400
    )

    # Eventos más comunes
    common_events = go.Figure(data=[
        go.Pie(
            labels=list(data['most_common_events'].keys()),
            values=list(data['most_common_events'].values()),
            hole=.3
        )
    ])
    common_events.update_layout(
        title="Tipos de eventos más comunes",
        template='plotly_white',
        height=400
    )

    # Tarjetas de resumen
    summary_cards = dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Eventos", className="card-title text-center"),
                    html.H2(f"{data['total_events']}", className="text-center")
                ])
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Horas", className="card-title text-center"),
                    html.H2(f"{data['total_hours']:.1f}", className="text-center")
                ])
            ]),
            width=6
        )
    ], className="mb-4")

    return html.Div([
        html.H3(f"Estadísticas del calendario", className="text-center mb-4"),
        summary_cards,
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=events_by_day,
                    config={'displayModeBar': False}
                )
            ], width=12, className="mb-4"),
            dbc.Col([
                dcc.Graph(
                    figure=common_events,
                    config={'displayModeBar': False}
                )
            ], width=12)
        ])
    ])