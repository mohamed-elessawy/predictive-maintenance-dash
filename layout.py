"""
Dash Application Layout - Simple & Clean
"""

from dash import dcc, html

def create_layout():
    """Simple dashboard layout with two tabs"""
    
    return html.Div([
        # Header
        html.Div([
            html.H1("🏭 Predictive Maintenance Dashboard", style={'margin': 0, 'color': '#2c3e50'}),
            html.P("AI4I 2020 - Machine Failure Prediction", style={'margin': '5px 0 0 0', 'color': '#7f8c8d'}),
        ], style={
            'backgroundColor': 'white',
            'padding': '30px',
            'marginBottom': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        }),

        # Tabs
        dcc.Tabs(value='tab-1', children=[
            # TAB 1: Data Exploration
            dcc.Tab(label='📊 Data Exploration', value='tab-1', children=[
                html.Div([
                    html.Div([
                        html.H3("Filters", style={'marginTop': 0}),
                        html.Div([
                            html.Div([
                                html.Label("Failure Status:"),
                                dcc.Dropdown(
                                    id='failure-filter',
                                    options=[
                                        {'label': 'All Data', 'value': 'all'},
                                        {'label': 'No Failures', 'value': 0},
                                        {'label': 'Failures', 'value': 1},
                                    ],
                                    value='all',
                                ),
                            ], style={'width': '48%', 'display': 'inline-block'}),
                            html.Div([
                                html.Label("Feature:"),
                                dcc.Dropdown(
                                    id='feature-selector',
                                    options=[
                                        {'label': 'Process Temperature', 'value': 'Process temperature [K]'},
                                        {'label': 'Air Temperature', 'value': 'Air temperature [K]'},
                                        {'label': 'Rotational Speed', 'value': 'Rotational speed [rpm]'},
                                        {'label': 'Torque', 'value': 'Torque [Nm]'},
                                        {'label': 'Tool Wear', 'value': 'Tool wear [min]'},
                                    ],
                                    value='Process temperature [K]',
                                ),
                            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
                        ]),
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'marginBottom': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                    }),

                    html.Div([
                        html.H3("Feature Distribution", style={'marginTop': 0}),
                        dcc.Graph(id='feature-distribution-graph'),
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'marginBottom': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                    }),

                    html.Div([
                        html.H3("Relationship Analysis", style={'marginTop': 0}),
                        dcc.Graph(id='scatter-plot-graph'),
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'marginBottom': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                    }),

                    html.Div([
                        html.H3("Failure Distribution", style={'marginTop': 0}),
                        dcc.Graph(id='class-distribution-graph'),
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                    }),
                ], style={'padding': '20px'}),
            ]),

            # TAB 2: Model Inference
            dcc.Tab(label='🤖 Model Inference', value='tab-2', children=[
                html.Div([
                    html.Div([
                        html.H3("Sensor Inputs", style={'marginTop': 0}),
                        html.Div([
                            html.Div([
                                html.Label("Process Temperature [°C]:"),
                                dcc.Slider(id='temp-slider', min=25, max=37, step=0.5, value=32, marks={25: '25°C', 31: '31°C', 37: '37°C'}, tooltip={"placement": "bottom", "always_visible": True}),
                                html.Div(id='temp-output', style={'fontSize': '13px', 'marginTop': '8px', 'color': '#4a90e2'}),
                            ], style={'marginBottom': '20px'}),
                            html.Div([
                                html.Label("Rotational Speed [RPM]:"),
                                dcc.Slider(id='speed-slider', min=1500, max=2500, step=50, value=2000, marks={1500: '1500', 2000: '2000', 2500: '2500'}, tooltip={"placement": "bottom", "always_visible": True}),
                                html.Div(id='speed-output', style={'fontSize': '13px', 'marginTop': '8px', 'color': '#4a90e2'}),
                            ], style={'marginBottom': '20px'}),
                            html.Div([
                                html.Label("Torque [Nm]:"),
                                dcc.Slider(id='torque-slider', min=3, max=76, step=1, value=40, marks={3: '3', 40: '40', 76: '76'}, tooltip={"placement": "bottom", "always_visible": True}),
                                html.Div(id='torque-output', style={'fontSize': '13px', 'marginTop': '8px', 'color': '#4a90e2'}),
                            ], style={'marginBottom': '20px'}),
                            html.Div([
                                html.Label("Tool Wear [minutes]:"),
                                dcc.Slider(id='toolwear-slider', min=0, max=250, step=5, value=100, marks={0: '0', 125: '125', 250: '250'}, tooltip={"placement": "bottom", "always_visible": True}),
                                html.Div(id='toolwear-output', style={'fontSize': '13px', 'marginTop': '8px', 'color': '#4a90e2'}),
                            ], style={'marginBottom': '20px'}),
                            html.Div([
                                html.Label("Air Temperature [°C]:"),
                                dcc.Slider(id='air-temp-slider', min=20, max=40, step=0.5, value=25, marks={20: '20°C', 30: '30°C', 40: '40°C'}, tooltip={"placement": "bottom", "always_visible": True}),
                                html.Div(id='air-temp-output', style={'fontSize': '13px', 'marginTop': '8px', 'color': '#4a90e2'}),
                            ], style={'marginBottom': 0}),
                        ]),
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'marginBottom': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                    }),

                    html.Div([
                        html.H3("Prediction", style={'marginTop': 0}),
                        html.Div(id='prediction-output'),
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                    }),
                ], style={'padding': '20px'}),
            ]),
        ]),
    ], style={
        'fontFamily': 'Segoe UI, sans-serif',
        'backgroundColor': '#ecf0f1',
        'minHeight': '100vh',
        'padding': '20px',
    })
