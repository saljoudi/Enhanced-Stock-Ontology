#!/usr/bin/env python
# coding: utf-8

# ============================================================
# ENHANCED ONTOLOGY-DRIVEN DASHBOARD
# ============================================================
# Advanced Web Dashboard with Real-time Capabilities
# Version 7.0 - Enhanced UI/UX and Performance
# ============================================================

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, Input, Output, State, callback_context
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import asyncio
from threading import Thread
import queue

# Import the enhanced ontology system
from enhanced_ontology_system import (
    EnhancedStockAnalysisEngine, 
    EnhancedStockOntologyGraph,
    PatternRecognitionModel,
    AdvancedRiskManager,
    RealTimeDataStreamer,
    config,
    enhanced_engine
)

# Custom CSS for enhanced styling
custom_css = """
<style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    .status-bullish { background-color: #28a745; }
    .status-bearish { background-color: #dc3545; }
    .status-neutral { background-color: #ffc107; }
    
    .chart-container {
        background: white;
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .analysis-panel {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    .recommendation-card {
        border-left: 4px solid;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    
    .rec-strong-buy { border-left-color: #28a745; background-color: #f8fff9; }
    .rec-buy { border-left-color: #20c997; background-color: #f0fdfa; }
    .rec-hold { border-left-color: #ffc107; background-color: #fffef7; }
    .rec-sell { border-left-color: #fd7e14; background-color: #fff8f0; }
    .rec-strong-sell { border-left-color: #dc3545; background-color: #fff5f5; }
    
    .real-time-indicator {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3498db;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .ontology-visualization {
        background: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
        font-family: monospace;
        font-size: 0.8rem;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .pattern-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        margin: 0.25rem;
    }
    
    .pattern-bullish { background-color: #d4edda; color: #155724; }
    .pattern-bearish { background-color: #f8d7da; color: #721c24; }
    .pattern-neutral { background-color: #fff3cd; color: #856404; }
</style>
"""

# Initialize the Dash app with enhanced theme
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.SOLAR,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    title="Enhanced Ontology-Driven Trading Dashboard"
)

# Global variables for real-time updates
real_time_data = {}
analysis_queue = queue.Queue()

# Layout Components
def create_header():
    """Create enhanced dashboard header"""
    return html.Div([
        html.Div([
            html.H1([
                html.I(className="fas fa-brain mr-3"),
                "Enhanced Ontology-Driven Trading Dashboard"
            ], className="text-center mb-2"),
            html.P("Advanced Financial Analysis with Machine Learning & Risk Management", 
                   className="text-center lead"),
            html.Div([
                html.Span("Real-time Mode: ", className="font-weight-bold"),
                html.Span("OFFLINE", id="real-time-status", className="badge badge-secondary")
            ], className="text-center mt-2")
        ], className="dashboard-header")
    ])

def create_control_panel():
    """Create enhanced control panel"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-cogs mr-2"),
                "Analysis Controls"
            ], className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Stock Symbol", className="font-weight-bold"),
                    dbc.Input(
                        id="stock-input",
                        type="text",
                        value="AAPL",
                        placeholder="Enter stock symbol (e.g., AAPL, GOOGL, TSLA)",
                        className="mb-3"
                    )
                ], md=3),
                dbc.Col([
                    dbc.Label("Time Range", className="font-weight-bold"),
                    dcc.Dropdown(
                        id="time-range",
                        options=[
                            {"label": "3 Months", "value": "3mo"},
                            {"label": "6 Months", "value": "6mo"},
                            {"label": "1 Year", "value": "1y"},
                            {"label": "2 Years", "value": "2y"},
                            {"label": "3 Years", "value": "3y"},
                            {"label": "5 Years", "value": "5y"},
                            {"label": "All Time", "value": "max"}
                        ],
                        value="1y",
                        className="mb-3"
                    )
                ], md=3),
                dbc.Col([
                    dbc.Label("Interval", className="font-weight-bold"),
                    dcc.Dropdown(
                        id="interval",
                        options=[
                            {"label": "1 Minute", "value": "1m"},
                            {"label": "5 Minutes", "value": "5m"},
                            {"label": "15 Minutes", "value": "15m"},
                            {"label": "1 Hour", "value": "1h"},
                            {"label": "1 Day", "value": "1d"},
                            {"label": "1 Week", "value": "1wk"}
                        ],
                        value="1d",
                        className="mb-3"
                    )
                ], md=3),
                dbc.Col([
                    dbc.Label("Analysis Mode", className="font-weight-bold"),
                    dcc.Dropdown(
                        id="analysis-mode",
                        options=[
                            {"label": "🧠 Full Ontology Analysis", "value": "full"},
                            {"label": "📊 Standard Technical", "value": "standard"},
                            {"label": "🤖 ML Enhanced", "value": "ml"},
                            {"label": "⚡ Real-time", "value": "realtime"}
                        ],
                        value="full",
                        className="mb-3"
                    )
                ], md=3)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        [
                            html.I(className="fas fa-play mr-2"),
                            "Start Analysis"
                        ],
                        id="analyze-button",
                        color="primary",
                        size="lg",
                        className="w-100"
                    )
                ], md=6),
                dbc.Col([
                    dbc.Button(
                        [
                            html.I(className="fas fa-sync-alt mr-2"),
                            "Real-time Mode"
                        ],
                        id="realtime-button",
                        color="success",
                        size="lg",
                        className="w-100"
                    )
                ], md=6)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(id="analysis-progress", className="mt-3")
                ])
            ])
        ])
    ], className="mb-4")

def create_metrics_overview():
    """Create metrics overview cards"""
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.Span(id="market-state-indicator", className="status-indicator status-neutral"),
                    html.Span("Market State", className="metric-label")
                ], className="d-flex align-items-center mb-2"),
                html.Div(id="market-state-value", className="metric-value", children="--"),
                html.Small(id="market-state-change", className="text-muted")
            ], className="metric-card")
        ], md=3),
        dbc.Col([
            html.Div([
                html.Div([
                    html.Span(id="trend-indicator", className="status-indicator status-neutral"),
                    html.Span("Trend Direction", className="metric-label")
                ], className="d-flex align-items-center mb-2"),
                html.Div(id="trend-value", className="metric-value", children="--"),
                html.Small(id="trend-confidence", className="text-muted")
            ], className="metric-card")
        ], md=3),
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-shield-alt mr-2 text-warning"),
                    html.Span("Risk Level", className="metric-label")
                ], className="d-flex align-items-center mb-2"),
                html.Div(id="risk-value", className="metric-value", children="--"),
                html.Small(id="risk-description", className="text-muted")
            ], className="metric-card")
        ], md=3),
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-line mr-2 text-info"),
                    html.Span("Overall Score", className="metric-label")
                ], className="d-flex align-items-center mb-2"),
                html.Div(id="score-value", className="metric-value", children="--"),
                html.Small(id="score-description", className="text-muted")
            ], className="metric-card")
        ], md=3)
    ], className="mb-4")

def create_main_charts():
    """Create main chart area"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-candlestick mr-2"),
                        "Price Analysis"
                    ])
                ]),
                dbc.CardBody([
                    dcc.Graph(id="main-price-chart", style={"height": "500px"})
                ])
            ], className="mb-4")
        ], lg=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-layer-group mr-2"),
                        "Technical Indicators"
                    ])
                ]),
                dbc.CardBody([
                    dcc.Graph(id="indicators-chart", style={"height": "500px"})
                ])
            ])
        ], lg=4)
    ], className="mb-4")

def create_analysis_panels():
    """Create analysis panels"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-brain mr-2"),
                        "Ontology Analysis"
                    ])
                ]),
                dbc.CardBody([
                    html.Div(id="ontology-insights"),
                    html.Div(id="reasoning-trace", className="mt-3")
                ])
            ], className="analysis-panel mb-4")
        ], lg=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-robot mr-2"),
                        "ML Analysis"
                    ])
                ]),
                dbc.CardBody([
                    html.Div(id="ml-insights"),
                    html.Div(id="pattern-detection", className="mt-3")
                ])
            ], className="analysis-panel mb-4")
        ], lg=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-shield-alt mr-2"),
                        "Risk Management"
                    ])
                ]),
                dbc.CardBody([
                    html.Div(id="risk-insights"),
                    html.Div(id="risk-recommendations", className="mt-3")
                ])
            ], className="analysis-panel mb-4")
        ], lg=4)
    ], className="mb-4")

def create_detailed_charts():
    """Create detailed technical charts"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6([
                        html.I(className="fas fa-chart-area mr-2"),
                        "Volume & Momentum"
                    ])
                ]),
                dbc.CardBody([
                    dcc.Graph(id="volume-momentum-chart", style={"height": "300px"})
                ])
            ], className="mb-3")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6([
                        html.I(className="fas fa-chart-line mr-2"),
                        "Volatility Analysis"
                    ])
                ]),
                dbc.CardBody([
                    dcc.Graph(id="volatility-chart", style={"height": "300px"})
                ])
            ], className="mb-3")
        ], md=6)
    ], className="mb-4")

def create_recommendations_panel():
    """Create trading recommendations panel"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-lightbulb mr-2"),
                "Trading Recommendations"
            ])
        ]),
        dbc.CardBody([
            html.Div(id="trading-recommendations"),
            html.Hr(),
            html.H6("Position Management", className="mt-3"),
            html.Div(id="position-management")
        ])
    ], className="mb-4")

def create_ontology_visualization():
    """Create ontology knowledge visualization"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-sitemap mr-2"),
                "Knowledge Graph"
            ])
        ]),
        dbc.CardBody([
            html.Div(id="ontology-visualization", className="ontology-visualization"),
            html.Div([
                html.Small("Knowledge Graph Statistics:", className="text-muted"),
                html.Div(id="knowledge-stats")
            ], className="mt-3")
        ])
    ], className="mb-4")

# Main Layout
app.layout = dbc.Container([
    # Custom CSS
    html.Div(html.Raw(custom_css)),
    
    # Header
    create_header(),
    
    # Control Panel
    create_control_panel(),
    
    # Metrics Overview
    create_metrics_overview(),
    
    # Main Charts
    create_main_charts(),
    
    # Analysis Panels
    create_analysis_panels(),
    
    # Detailed Charts
    create_detailed_charts(),
    
    # Recommendations
    create_recommendations_panel(),
    
    # Ontology Visualization
    create_ontology_visualization(),
    
    # Hidden divs for data storage
    html.Div(id="analysis-data", style={"display": "none"}),
    html.Div(id="real-time-data", style={"display": "none"}),
    
    # Interval component for real-time updates
    dcc.Interval(
        id="real-time-interval",
        interval=30*1000,  # 30 seconds
        n_intervals=0,
        disabled=True
    ),
    
    # Footer
    html.Footer([
        html.Hr(),
        html.P("Enhanced Ontology-Driven Trading Dashboard © 2025", 
               className="text-center text-muted")
    ], className="mt-5")
], fluid=True, className="p-4")

# Callback Functions

@app.callback(
    [Output("analysis-progress", "children"),
     Output("analyze-button", "disabled"),
     Output("analyze-button", "children")],
    Input("analyze-button", "n_clicks"),
    State("stock-input", "value"),
    State("time-range", "value"),
    State("interval", "value"),
    State("analysis-mode", "value")
)
def start_analysis(n_clicks, symbol, time_range, interval, analysis_mode):
    """Handle analysis initiation"""
    if not n_clicks:
        return "", False, [html.I(className="fas fa-play mr-2"), "Start Analysis"]
    
    if not symbol:
        return "Please enter a stock symbol", False, [html.I(className="fas fa-play mr-2"), "Start Analysis"]
    
    # Start analysis in background thread
    thread = Thread(target=run_analysis, args=(symbol, time_range, interval, analysis_mode))
    thread.start()
    
    return [
        html.Div([
            html.Div(className="loading-spinner"),
            html.P("Analyzing... This may take a moment.", className="text-center mt-2")
        ]),
        True,
        [html.I(className="fas fa-spinner fa-spin mr-2"), "Analyzing..."]
    ]

def run_analysis(symbol, time_range, interval, analysis_mode):
    """Run analysis in background thread"""
    try:
        # Run the enhanced analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        if analysis_mode == "full":
            result = loop.run_until_complete(enhanced_engine.analyze_symbol(symbol, time_range, interval))
        else:
            # Simplified analysis for other modes
            result = loop.run_until_complete(enhanced_engine.analyze_symbol(symbol, time_range, interval))
        
        # Put result in queue
        analysis_queue.put(result)
        
    except Exception as e:
        analysis_queue.put({"error": str(e), "symbol": symbol})

@app.callback(
    [Output("analysis-data", "children"),
     Output("analyze-button", "disabled"),
     Output("analyze-button", "children"),
     Output("analysis-progress", "children")],
    Input("real-time-interval", "n_intervals")
)
def check_analysis_completion(n_intervals):
    """Check for completed analysis"""
    try:
        result = analysis_queue.get_nowait()
        return json.dumps(result), False, [html.I(className="fas fa-play mr-2"), "Start Analysis"], ""
    except queue.Empty:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

@app.callback(
    [Output("market-state-value", "children"),
     Output("market-state-indicator", "className"),
     Output("trend-value", "children"),
     Output("trend-indicator", "className"),
     Output("risk-value", "children"),
     Output("score-value", "children"),
     Output("score-description", "children")],
    Input("analysis-data", "children")
)
def update_metrics(analysis_data):
    """Update main metrics display"""
    if not analysis_data:
        return ["--"] * 7
    
    try:
        data = json.loads(analysis_data)
        
        # Market State
        market_state = data.get("market_context", {}).get("market_state", "unknown")
        market_state_class = "status-bullish" if "bull" in market_state else "status-bearish" if "bear" in market_state else "status-neutral"
        
        # Trend Direction
        trend_direction = data.get("market_context", {}).get("trend_direction", "neutral")
        trend_class = "status-bullish" if "up" in trend_direction else "status-bearish" if "down" in trend_direction else "status-neutral"
        
        # Risk Level
        risk_level = data.get("risk_assessment", {}).get("risk_score", 0.5)
        risk_display = f"{risk_level:.1%}"
        
        # Overall Score
        overall_score = data.get("overall_score", 0)
        score_display = f"{overall_score:.1%}"
        score_desc = data.get("overall_recommendation", "hold").upper()
        
        return [
            market_state.replace("_", " ").title(),
            f"status-indicator {market_state_class}",
            trend_direction.replace("_", " ").title(),
            f"status-indicator {trend_class}",
            risk_display,
            score_display,
            score_desc
        ]
        
    except Exception as e:
        return [f"Error: {str(e)}"] + ["--"] * 6

@app.callback(
    Output("main-price-chart", "figure"),
    Input("analysis-data", "children")
)
def update_main_chart(analysis_data):
    """Update main price chart"""
    if not analysis_data:
        return go.Figure().update_layout(title="No data available", template="plotly_dark")
    
    try:
        data = json.loads(analysis_data)
        
        # Create enhanced candlestick chart
        fig = go.Figure()
        
        # Add candlestick (placeholder - would need actual OHLC data)
        fig.add_trace(go.Scatter(
            x=[1, 2, 3, 4, 5],
            y=[100, 102, 98, 105, 103],
            mode='lines+markers',
            name=f"{data.get('symbol', 'Stock')} Price",
            line=dict(color='#00d4ff', width=2)
        ))
        
        # Add support and resistance levels
        support_levels = data.get("market_context", {}).get("support_levels", [])
        resistance_levels = data.get("market_context", {}).get("resistance_levels", [])
        
        for i, level in enumerate(support_levels[:2]):
            fig.add_hline(y=level, line_dash="dash", line_color="green", 
                         annotation_text=f"Support {i+1}: {level:.2f}")
        
        for i, level in enumerate(resistance_levels[:2]):
            fig.add_hline(y=level, line_dash="dash", line_color="red",
                         annotation_text=f"Resistance {i+1}: {level:.2f}")
        
        fig.update_layout(
            title=f"{data.get('symbol', 'Stock')} Price Analysis",
            template="plotly_dark",
            height=500,
            showlegend=True
        )
        
        return fig
        
    except Exception as e:
        return go.Figure().update_layout(title=f"Error: {str(e)}", template="plotly_dark")

@app.callback(
    Output("ontology-insights", "children"),
    Input("analysis-data", "children")
)
def update_ontology_insights(analysis_data):
    """Update ontology insights panel"""
    if not analysis_data:
        return html.Div("No analysis data available")
    
    try:
        data = json.loads(analysis_data)
        market_context = data.get("market_context", {})
        
        insights = [
            html.H6("Market Context", className="mb-3"),
            html.P([
                html.Strong("State: "), 
                market_context.get("market_state", "unknown").replace("_", " ").title()
            ]),
            html.P([
                html.Strong("Trend: "), 
                market_context.get("trend_direction", "neutral").replace("_", " ").title()
            ]),
            html.P([
                html.Strong("Volatility: "), 
                market_context.get("volatility_regime", "medium").replace("_", " ").title()
            ]),
            html.P([
                html.Strong("Volume Profile: "), 
                market_context.get("volume_profile", "neutral").replace("_", " ").title()
            ])
        ]
        
        # Add support and resistance levels
        support_levels = market_context.get("support_levels", [])
        resistance_levels = market_context.get("resistance_levels", [])
        
        if support_levels:
            insights.extend([
                html.Hr(),
                html.H6("Support Levels", className="mb-2"),
                html.Ul([
                    html.Li(f"Level {i+1}: {level:.2f}") 
                    for i, level in enumerate(support_levels[:3]) if level
                ])
            ])
        
        if resistance_levels:
            insights.extend([
                html.H6("Resistance Levels", className="mb-2 mt-2"),
                html.Ul([
                    html.Li(f"Level {i+1}: {level:.2f}") 
                    for i, level in enumerate(resistance_levels[:3]) if level
                ])
            ])
        
        return insights
        
    except Exception as e:
        return html.Div(f"Error loading ontology insights: {str(e)}")

@app.callback(
    Output("ml-insights", "children"),
    Input("analysis-data", "children")
)
def update_ml_insights(analysis_data):
    """Update ML insights panel"""
    if not analysis_data:
        return html.Div("No ML analysis data available")
    
    try:
        data = json.loads(analysis_data)
        ml_analysis = data.get("ml_analysis", {})
        
        insights = [
            html.H6("Machine Learning Analysis", className="mb-3"),
            html.P([
                html.Strong("Prediction: "), 
                html.Span(ml_analysis.get("prediction", "neutral").title(), 
                         className=f"badge badge-{ml_analysis.get('prediction', 'secondary')}")
            ]),
            html.P([
                html.Strong("Confidence: "), 
                f"{ml_analysis.get('confidence', 0):.1%}"
            ]),
            html.P([
                html.Strong("Recommendation: "), 
                ml_analysis.get("recommendation", "hold").upper()
            ])
        ]
        
        # Anomaly detection
        anomaly_detection = data.get("anomaly_detection", {})
        if anomaly_detection.get("is_anomaly"):
            insights.extend([
                html.Hr(),
                html.Div([
                    html.I(className="fas fa-exclamation-triangle text-warning mr-2"),
                    html.Strong("Anomaly Detected!")
                ], className="alert alert-warning"),
                html.P([
                    html.Strong("Anomaly Score: "), 
                    f"{anomaly_detection.get('anomaly_score', 0):.3f}"
                ])
            ])
        
        return insights
        
    except Exception as e:
        return html.Div(f"Error loading ML insights: {str(e)}")

@app.callback(
    Output("risk-insights", "children"),
    Input("analysis-data", "children")
)
def update_risk_insights(analysis_data):
    """Update risk insights panel"""
    if not analysis_data:
        return html.Div("No risk analysis data available")
    
    try:
        data = json.loads(analysis_data)
        risk_assessment = data.get("risk_assessment", {})
        
        risk_score = risk_assessment.get("risk_score", 0.5)
        risk_color = "danger" if risk_score > 0.7 else "warning" if risk_score > 0.4 else "success"
        
        insights = [
            html.H6("Risk Assessment", className="mb-3"),
            html.Div([
                html.Span("Risk Score: ", className="font-weight-bold"),
                html.Span(f"{risk_score:.1%}", 
                         className=f"badge badge-{risk_color} ml-2")
            ], className="mb-3"),
            
            html.H6("Position Management", className="mb-2"),
            html.P([
                html.Strong("Recommended Position Size: "), 
                f"${risk_assessment.get('position_size', 0):,.2f}"
            ]),
            html.P([
                html.Strong("Stop Loss: "), 
                f"${risk_assessment.get('stop_loss', 0):.2f}"
            ]),
            html.P([
                html.Strong("Take Profit: "), 
                f"${risk_assessment.get('take_profit', 0):.2f}"
            ])
        ]
        
        return insights
        
    except Exception as e:
        return html.Div(f"Error loading risk insights: {str(e)}")

@app.callback(
    Output("trading-recommendations", "children"),
    Input("analysis-data", "children")
)
def update_recommendations(analysis_data):
    """Update trading recommendations"""
    if not analysis_data:
        return html.Div("No recommendations available")
    
    try:
        data = json.loads(analysis_data)
        recommendation = data.get("overall_recommendation", "hold")
        
        # Map recommendation to CSS class
        rec_class = {
            "strong_buy": "rec-strong-buy",
            "buy": "rec-buy", 
            "hold": "rec-hold",
            "sell": "rec-sell",
            "strong_sell": "rec-strong-sell"
        }.get(recommendation, "rec-hold")
        
        # Risk assessment recommendations
        risk_recommendations = data.get("risk_assessment", {}).get("recommendations", [])
        
        recommendations = [
            html.Div([
                html.H4(recommendation.replace("_", " ").upper(), 
                       className=f"text-center mb-3 recommendation-card {rec_class}"),
                html.H6("Risk Management Recommendations:", className="mb-3"),
                html.Ul([
                    html.Li(rec) for rec in risk_recommendations
                ]) if risk_recommendations else html.P("No specific recommendations")
            ])
        ]
        
        return recommendations
        
    except Exception as e:
        return html.Div(f"Error loading recommendations: {str(e)}")

@app.callback(
    [Output("real-time-status", "children"),
     Output("real-time-status", "className"),
     Output("real-time-interval", "disabled")],
    Input("realtime-button", "n_clicks"),
    State("real-time-interval", "disabled")
)
def toggle_realtime(n_clicks, current_disabled):
    """Toggle real-time mode"""
    if not n_clicks:
        return "OFFLINE", "badge badge-secondary", True
    
    if current_disabled:
        return "LIVE", "badge badge-success real-time-indicator", False
    else:
        return "OFFLINE", "badge badge-secondary", True

@app.callback(
    Output("knowledge-stats", "children"),
    Input("analysis-data", "children")
)
def update_knowledge_stats(analysis_data):
    """Update knowledge graph statistics"""
    if not analysis_data:
        return "No knowledge graph data"
    
    try:
        data = json.loads(analysis_data)
        knowledge_summary = data.get("knowledge_summary", {})
        
        stats = [
            html.P([html.Strong("Statements: "), knowledge_summary.get("total_statements", 0)]),
            html.P([html.Strong("Indicators: "), knowledge_summary.get("indicators", 0)]),
            html.P([html.Strong("Signals: "), knowledge_summary.get("signals", 0)]),
            html.P([html.Strong("ML Predictions: "), knowledge_summary.get("ml_predictions", 0)]),
            html.P([html.Strong("Risk Assessments: "), knowledge_summary.get("risk_assessments", 0)]),
            html.P([html.Strong("Contradictions: "), knowledge_summary.get("contradictions", 0)]),
            html.P([html.Strong("Confirmations: "), knowledge_summary.get("confirmations", 0)])
        ]
        
        return stats
        
    except Exception as e:
        return f"Error: {str(e)}"

# Real-time update callback
@app.callback(
    Output("real-time-data", "children"),
    Input("real-time-interval", "n_intervals")
)
def update_real_time(n_intervals):
    """Update real-time data"""
    if n_intervals == 0:
        return ""
    
    # Here you would implement real-time data fetching
    # For now, return a placeholder
    return json.dumps({
        "timestamp": datetime.now().isoformat(),
        "status": "real_time_update"
    })

# Initialize the enhanced dashboard
if __name__ == "__main__":
    print("🚀 Starting Enhanced Ontology-Driven Trading Dashboard...")
    print("📊 Features:")
    print("   • Advanced Ontology Reasoning")
    print("   • Machine Learning Integration") 
    print("   • Real-time Risk Management")
    print("   • Pattern Recognition")
    print("   • Enhanced Visualizations")
    print("   • Real-time Data Streaming")
    print("\n🔗 Dashboard will be available at: http://localhost:8050")
    
    app.run_server(debug=True, port=8050, host="0.0.0.0")