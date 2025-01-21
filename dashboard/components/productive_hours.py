import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_productive_hours_figures(data):
    if not data or 'most_productive_hours' not in data:
        return html.Div("No hay datos disponibles", className="text-center p-4")

    # Horas más productivas
    productive_hours = go.Figure(data=[
        go.Bar(
            x=list(data['most_productive_hours'].keys()),
            y=list(data['most_productive_hours'].values()),
            marker_color='rgb(26, 118, 255)'
        )
    ])
    productive_hours.update_layout(
        title="Distribución de actividades por hora",
        xaxis_title="Hora del día",
        yaxis_title="Número de eventos",
        template='plotly_white'
    )

    # Distribución diaria
    daily_dist = go.Figure(data=[
        go.Bar(
            x=list(data['daily_distribution'].keys()),
            y=list(data['daily_distribution'].values()),
            marker_color='rgb(158, 202, 225)'
        )
    ])
    daily_dist.update_layout(
        title="Distribución diaria de actividades",
        xaxis_title="Día de la semana",
        yaxis_title="Horas totales",
        template='plotly_white'
    )

    # Tarjetas de métricas clave
    metrics_cards = dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Hora más productiva", className="card-title text-center"),
                    html.H2(data['peak_productivity_time'], className="text-center")
                ])
            ])
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Horas activas", className="card-title text-center"),
                    html.H2(str(data['total_active_hours']), className="text-center")
                ])
            ])
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Promedio diario", className="card-title text-center"),
                    html.H2(f"{data['total_hours_tracked']/7:.1f}h", className="text-center")
                ])
            ])
        )
    ])

    return html.Div([
        html.H3("Análisis de productividad", className="text-center mb-4"),
        metrics_cards,
        html.Div(className="mb-4"),  # Espaciador
        dbc.Row([
            dbc.Col(dcc.Graph(figure=productive_hours), md=6),
            dbc.Col(dcc.Graph(figure=daily_dist), md=6)
        ])
    ])