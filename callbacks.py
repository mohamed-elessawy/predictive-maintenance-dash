"""
Dash Application Callbacks
Handles all interactive updates and predictions
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Input, Output, html

# Get the project root
PROJECT_ROOT = Path(__file__).parent.resolve()
DATA_DIR = PROJECT_ROOT / 'data'

# Load model artifacts
print("Loading model artifacts...")
model = joblib.load(DATA_DIR / 'model_weights.pkl')
scaler = joblib.load(DATA_DIR / 'scaler.pkl')
feature_names = joblib.load(DATA_DIR / 'feature_names.pkl')

# Load the original dataset for EDA
df = pd.read_csv(DATA_DIR / 'ai4i2020.csv')

print("✓ Model and data loaded successfully!")


def register_callbacks(app):
    """
    Register all callbacks for the dashboard
    """
    
    # ==================== DATA EXPLORATION CALLBACKS ====================
    
    @app.callback(
        Output('feature-distribution-graph', 'figure'),
        [Input('failure-filter', 'value'),
         Input('feature-selector', 'value')]
    )
    def update_distribution_graph(failure_filter, feature):
        """Update feature distribution histogram"""
        
        # Filter data based on failure status
        if failure_filter == 'all':
            data = df
            title_suffix = "All Data"
        else:
            data = df[df['Machine failure'] == failure_filter]
            title_suffix = "No Failures" if failure_filter == 0 else "Failures"
        
        # Create histogram
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=data[feature],
            nbinsx=40,
            name=feature,
            marker=dict(color='#4a90e2', line=dict(color='#2c3e50', width=1)),
            opacity=0.8,
        ))
        
        fig.update_layout(
            title=f"Distribution of {feature} ({title_suffix})",
            xaxis_title=feature,
            yaxis_title="Frequency",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Segoe UI, sans-serif",
                size=12,
                color='#2c3e50'
            ),
            hovermode='x unified',
            margin=dict(l=60, r=40, t=60, b=60),
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#ecf0f1',
            zeroline=False,
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#ecf0f1',
            zeroline=False,
        )
        
        return fig
    
    
    @app.callback(
        Output('scatter-plot-graph', 'figure'),
        [Input('failure-filter', 'value'),
         Input('feature-selector', 'value')]
    )
    def update_scatter_plot(failure_filter, x_feature):
        """Update scatter plot with feature relationships"""
        
        # Filter data
        if failure_filter == 'all':
            data = df
            title_suffix = "All Data"
        else:
            data = df[df['Machine failure'] == failure_filter]
            title_suffix = "No Failures" if failure_filter == 0 else "Failures"
        
        # Select a complementary feature for Y axis
        feature_mapping = {
            'Process temperature [K]': 'Tool wear [min]',
            'Air temperature [K]': 'Rotational speed [rpm]',
            'Rotational speed [rpm]': 'Torque [Nm]',
            'Torque [Nm]': 'Process temperature [K]',
            'Tool wear [min]': 'Air temperature [K]',
        }
        
        y_feature = feature_mapping.get(x_feature, 'Tool wear [min]')
        
        # Create scatter plot
        fig = go.Figure()
        
        # Plot by failure status if viewing all data
        if failure_filter == 'all':
            for fail_status, label, color in [(0, 'No Failure', '#27ae60'), (1, 'Failure', '#e74c3c')]:
                subset = df[df['Machine failure'] == fail_status]
                fig.add_trace(go.Scatter(
                    x=subset[x_feature],
                    y=subset[y_feature],
                    mode='markers',
                    name=label,
                    marker=dict(
                        size=6,
                        color=color,
                        opacity=0.7,
                        line=dict(color='white', width=0.5),
                    ),
                    hovertemplate=f'<b>{label}</b><br>{x_feature}: %{{x:.2f}}<br>{y_feature}: %{{y:.2f}}<extra></extra>',
                ))
        else:
            fig.add_trace(go.Scatter(
                x=data[x_feature],
                y=data[y_feature],
                mode='markers',
                name=title_suffix,
                marker=dict(
                    size=6,
                    color='#4a90e2',
                    opacity=0.7,
                    line=dict(color='white', width=0.5),
                ),
                hovertemplate=f'<b>{title_suffix}</b><br>{x_feature}: %{{x:.2f}}<br>{y_feature}: %{{y:.2f}}<extra></extra>',
            ))
        
        fig.update_layout(
            title=f"Feature Relationship: {x_feature} vs {y_feature} ({title_suffix})",
            xaxis_title=x_feature,
            yaxis_title=y_feature,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Segoe UI, sans-serif",
                size=12,
                color='#2c3e50'
            ),
            hovermode='closest',
            margin=dict(l=60, r=40, t=60, b=60),
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#ecf0f1',
            zeroline=False,
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#ecf0f1',
            zeroline=False,
        )
        
        return fig
    
    
    @app.callback(
        Output('class-distribution-graph', 'figure'),
        Input('failure-filter', 'value')
    )
    def update_class_distribution(failure_filter):
        """Update class distribution pie/bar chart"""
        
        counts = df['Machine failure'].value_counts()
        
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "pie"}, {"type": "bar"}]],
            subplot_titles=("Count Distribution", "Percentage Distribution")
        )
        
        # Pie chart
        fig.add_trace(
            go.Pie(
                labels=['No Failure', 'Failure'],
                values=[counts[0], counts[1]],
                marker=dict(colors=['#27ae60', '#e74c3c']),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                name='',
            ),
            row=1, col=1
        )
        
        # Bar chart
        percentages = (counts / counts.sum()) * 100
        fig.add_trace(
            go.Bar(
                x=['No Failure', 'Failure'],
                y=[percentages[0], percentages[1]],
                marker=dict(color=['#27ae60', '#e74c3c']),
                text=[f'{p:.1f}%' for p in [percentages[0], percentages[1]]],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Percentage: %{y:.1f}%<extra></extra>',
                name='',
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Machine Failure Status Distribution",
            font=dict(
                family="Segoe UI, sans-serif",
                size=12,
                color='#2c3e50'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
        )
        
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ecf0f1')
        
        return fig
    
    
    # ==================== MODEL INFERENCE CALLBACKS ====================
    
    @app.callback(
        [Output('temp-output', 'children'),
         Output('speed-output', 'children'),
         Output('torque-output', 'children'),
         Output('toolwear-output', 'children'),
         Output('air-temp-output', 'children'),
         Output('prediction-output', 'children')],
        [Input('temp-slider', 'value'),
         Input('speed-slider', 'value'),
         Input('torque-slider', 'value'),
         Input('toolwear-slider', 'value'),
         Input('air-temp-slider', 'value')]
    )
    def update_prediction(temp_celsius, speed, torque, toolwear, air_temp_celsius):
        """
        Update prediction based on sensor inputs
        Convert Celsius to Kelvin for model
        """
        
        # Convert Celsius to Kelvin
        temp = temp_celsius + 273.15
        air_temp = air_temp_celsius + 273.15
        
        # Display slider values in Celsius
        temp_text = f"Selected: {temp_celsius:.1f}°C"
        speed_text = f"Selected: {speed:.0f} RPM"
        torque_text = f"Selected: {torque:.1f} Nm"
        toolwear_text = f"Selected: {toolwear:.0f} min"
        air_temp_text = f"Selected: {air_temp_celsius:.1f}°C"
        
        try:
            # Build feature vector in exact order as training
            features_dict = {}
            
            # Original features
            features_dict['Process temperature [K]'] = temp
            features_dict['Air temperature [K]'] = air_temp
            features_dict['Rotational speed [rpm]'] = speed
            features_dict['Torque [Nm]'] = torque
            features_dict['Tool wear [min]'] = toolwear
            
            # Engineered features
            features_dict['Temp_Difference'] = temp - air_temp
            features_dict['Power'] = torque * speed / 9550
            features_dict['Tool_Wear_per_Product'] = toolwear
            features_dict['Thermal_Stress_Index'] = ((temp - 298) / 12 + (torque * speed / 9550) / 200) / 2
            features_dict['Equipment_Condition_Index'] = ((speed - 1500) / 1000) * ((torque - 3) / 73)
            
            # Categorical features (failure modes)
            for cat in ['HDF', 'OSF', 'PWF', 'RNF', 'TWF', 'UDI']:
                features_dict[cat] = 0
            
            # Create DataFrame in exact feature order
            input_df = pd.DataFrame([features_dict])
            input_df = input_df[feature_names]
            
            # Scale and predict
            input_scaled = scaler.transform(input_df)
            prediction = model.predict(input_scaled)[0]
            prediction_proba = model.predict_proba(input_scaled)[0]
            
            # Get confidence scores
            confidence_no_failure = prediction_proba[0] * 100
            confidence_failure = prediction_proba[1] * 100
            
            # DEBUG: Print feature values
            print(f"\n=== PREDICTION DEBUG ===")
            print(f"Process Temp (K): {temp:.2f}, Air Temp (K): {air_temp:.2f}")
            print(f"Speed: {speed:.0f}, Torque: {torque:.2f}, Tool Wear: {toolwear:.0f}")
            print(f"Temp Diff: {temp - air_temp:.2f}")
            print(f"Confidence - No Failure: {confidence_no_failure:.1f}%, Failure: {confidence_failure:.1f}%")
            print(f"Prediction: {prediction}")
            print("========================\n")
            
            # Failure information from training data
            failure_stats = df[df['Machine failure'] == 1]
            
            fail_reminder = html.Div(
                style={
                    'background': 'rgba(255, 255, 255, 0.2)',
                    'padding': '15px',
                    'borderRadius': '6px',
                    'marginTop': '15px',
                    'fontSize': '13px',
                    'opacity': 0.95,
                },
                children=[
                    html.P(
                        f"💡 Failures typically occur with: Tool Wear > 200 min (avg failure: {failure_stats['Tool wear [min]'].mean():.0f}), High Torque (avg: {failure_stats['Torque [Nm]'].mean():.1f} Nm), High Temp. Try extreme slider values!",
                        style={'margin': '0', 'lineHeight': '1.6'}
                    ),
                ]
            )
            
            # Create prediction output
            if prediction == 0:
                prediction_box = html.Div(
                    style={
                        'background': 'linear-gradient(135deg, #27ae60 0%, #1e8449 100%)',
                        'color': 'white',
                        'padding': '40px',
                        'borderRadius': '12px',
                        'textAlign': 'center',
                        'boxShadow': '0 4px 15px rgba(39, 174, 96, 0.3)',
                    },
                    children=[
                        html.H2("✅ NO FAILURE PREDICTED", style={'margin': '0 0 15px 0', 'fontSize': '28px'}),
                        html.Div(
                            f"Confidence: {confidence_no_failure:.1f}%",
                            style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '15px'}
                        ),
                        html.Div(
                            "Machine is operating under normal conditions.",
                            style={'fontSize': '14px', 'opacity': 0.9, 'marginBottom': '15px'}
                        ),
                        fail_reminder,
                    ]
                )
            else:
                # Failure
                prediction_box = html.Div(
                    style={
                        'background': 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
                        'color': 'white',
                        'padding': '40px',
                        'borderRadius': '12px',
                        'textAlign': 'center',
                        'boxShadow': '0 4px 15px rgba(231, 76, 60, 0.3)',
                    },
                    children=[
                        html.H2("⚠️ FAILURE PREDICTED", style={'margin': '0 0 15px 0', 'fontSize': '28px'}),
                        html.Div(
                            f"Confidence: {confidence_failure:.1f}%",
                            style={'fontSize': '18px', 'fontWeight': '600', 'marginBottom': '15px'}
                        ),
                        html.Div(
                            "Machine maintenance is recommended immediately.",
                            style={'fontSize': '14px', 'opacity': 0.9}
                        ),
                    ]
                )
            
            return (
                temp_text,
                speed_text,
                torque_text,
                toolwear_text,
                air_temp_text,
                prediction_box
            )
        
        except Exception as e:
            error_box = html.Div(
                style={
                    'background': '#fff3cd',
                    'color': '#856404',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'borderLeft': '4px solid #f39c12',
                },
                children=[
                    html.H4("⚠️ Prediction Error", style={'margin': '0 0 10px 0'}),
                    html.P(f"Error: {str(e)}", style={'margin': '0', 'fontSize': '13px'}),
                ]
            )
            
            return (temp_text, speed_text, torque_text, toolwear_text, air_temp_text, error_box)


print("✓ All callbacks registered successfully!")
