import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Visualizer:
    @staticmethod
    def create_attack_distribution_chart(data):
        """Create pie chart of attack distribution"""
        fig = px.pie(
            values=list(data.values()),
            names=list(data.keys()),
            title="Overview of Detected Attack Vectors",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            hole=0.45
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label', 
            textfont=dict(color='#0f172a', size=13),
            marker=dict(line=dict(color='#ffffff', width=2))
        )
        fig.update_layout(
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#0f172a'),
            margin=dict(t=50, b=10, l=10, r=10)
        )
        return fig
    
    @staticmethod
    def create_confidence_gauge(confidence, prediction):
        """Create a gauge chart for confidence score"""
        # More modern vibrant colors
        colors = ['#ef4444', '#f59e0b', '#10b981'] if prediction == 'normal' else ['#10b981', '#f59e0b', '#ef4444']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence * 100,
            title={'text': f"Confidence: {prediction.upper()}", 'font': {'size': 20, 'color': '#0f172a'}},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': "#3b82f6"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#e2e8f0",
                'steps': [
                    {'range': [0, 33], 'color': colors[0]},
                    {'range': [33, 66], 'color': colors[1]},
                    {'range': [66, 100], 'color': colors[2]}
                ],
                'threshold': {
                    'line': {'color': "#0f172a", 'width': 3},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#0f172a'),
            margin=dict(t=50, b=10, l=10, r=10)
        )
        return fig
    
    @staticmethod
    def create_feature_importance_chart(feature_importance, feature_names):
        """Create feature importance bar chart"""
        # Sort features by importance
        sorted_idx = np.argsort(feature_importance)[-15:]  # Top 15 features
        
        fig = go.Figure(go.Bar(
            x=feature_importance[sorted_idx],
            y=[feature_names[i] for i in sorted_idx],
            orientation='h',
            marker_color='#3b82f6'
        ))
        
        fig.update_layout(
            title="Top 15 Most Important Features",
            xaxis_title="Importance",
            yaxis_title="Features",
            height=400,
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_network_traffic_heatmap(data):
        """Create correlation heatmap of network features"""
        # Create sample correlation matrix
        corr_matrix = np.random.rand(10, 10)
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            colorscale='Blues',
            showscale=True
        ))
        
        fig.update_layout(
            title="Network Feature Correlations",
            height=400,
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig