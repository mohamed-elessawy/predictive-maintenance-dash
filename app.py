"""
Predictive Maintenance Dashboard - Main Application
Phase 2: Dash Application
"""

import dash
from dash import dcc, html
import os
from pathlib import Path

# Import layout and callbacks
from layout import create_layout
from callbacks import register_callbacks

# Get the project root
PROJECT_ROOT = Path(__file__).parent.resolve()
DATA_DIR = PROJECT_ROOT / 'data'

# Initialize the Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[],
)

# Set app title
app.title = "Predictive Maintenance Dashboard"

# Create and set layout
app.layout = create_layout()

# Register all callbacks
register_callbacks(app)

# Server for deployment
server = app.server

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True, host='127.0.0.1', port=8050)
