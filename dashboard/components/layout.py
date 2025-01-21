import dash_bootstrap_components as dbc
from dash import html, dcc
from datetime import datetime, timedelta

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Calendar Analytics Dashboard", className="text-center my-4"),
                html.Hr()
            ])
        ]),

        # Filtros
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Filtros", className="mb-3"),
                        html.Label("Rango de fechas:"),
                        dcc.DatePickerRange(
                            id='date-range',
                            min_date_allowed=datetime.now() - timedelta(days=365),
                            max_date_allowed=datetime.now() + timedelta(days=365),
                            start_date=datetime.now().date(),
                            end_date=(datetime.now() + timedelta(days=7)).date(),
                            display_format='YYYY-MM-DD'
                        ),
                        html.Label("Calendario:", className="mt-3"),
                        dcc.Dropdown(
                            id='calendar-select',
                            options=[
                                {'label': 'VLESIM', 'value': 'VLESIM'},
                                {'label': 'Personal', 'value': 'Personal'},
                                {'label': 'Health', 'value': 'Health'}
                            ],
                            value='VLESIM',
                            className="mt-1"
                        )
                    ])
                ], className="mb-4")
            ])
        ]),

        # Loading spinner
        dbc.Spinner(
            children=[
                # Contenido principal
                dbc.Row([
                    dbc.Col([
                        html.Div(id='analysis-content', className="mb-4"),
                        dbc.Row([
                            dbc.Col(html.Div(id='calendar-stats-content'), md=6),
                            dbc.Col(html.Div(id='productive-hours-content'), md=6)
                        ])
                    ])
                ])
            ],
            color="primary",
            type="border",
            fullscreen=False
        )
    ], fluid=True)