"""
Charts Component Module
Reusable chart visualization components
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from core.logger import get_logger

logger = get_logger(__name__)


class ChartComponents:
    """Reusable chart components for dashboard"""
    
    @staticmethod
    def create_line_chart(df, x_col, y_col, title="Line Chart"):
        """
        Create interactive line chart
        
        Args:
            df (pd.DataFrame): Data
            x_col (str): X-axis column
            y_col (str): Y-axis column
            title (str): Chart title
        
        Returns:
            plotly.graph_objects.Figure: Chart figure
        """
        try:
            fig = px.line(df, x=x_col, y=y_col, title=title,
                         markers=True, template='plotly_white')
            fig.update_layout(hovermode='x unified')
            return fig
        except Exception as e:
            logger.error(f"Error creating line chart: {str(e)}")
            return None
    
    @staticmethod
    def create_bar_chart(df, x_col, y_col, title="Bar Chart"):
        """Create interactive bar chart"""
        try:
            fig = px.bar(df, x=x_col, y=y_col, title=title,
                        template='plotly_white', color=y_col)
            return fig
        except Exception as e:
            logger.error(f"Error creating bar chart: {str(e)}")
            return None
    
    @staticmethod
    def create_pie_chart(df, values_col, names_col, title="Pie Chart"):
        """Create interactive pie chart"""
        try:
            fig = px.pie(df, values=values_col, names=names_col, title=title)
            return fig
        except Exception as e:
            logger.error(f"Error creating pie chart: {str(e)}")
            return None
    
    @staticmethod
    def create_scatter_chart(df, x_col, y_col, color_col=None, title="Scatter Chart"):
        """Create interactive scatter chart"""
        try:
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=title,
                           template='plotly_white', hover_data=df.columns)
            return fig
        except Exception as e:
            logger.error(f"Error creating scatter chart: {str(e)}")
            return None
    
    @staticmethod
    def create_heatmap(df, title="Heatmap"):
        """Create heatmap for correlations"""
        try:
            fig = go.Figure(data=go.Heatmap(z=df.values, x=df.columns, y=df.index))
            fig.update_layout(title=title, template='plotly_white')
            return fig
        except Exception as e:
            logger.error(f"Error creating heatmap: {str(e)}")
            return None
    
    @staticmethod
    def create_histogram(df, col, title="Histogram", nbins=30):
        """Create histogram"""
        try:
            fig = px.histogram(df, x=col, title=title, nbins=nbins,
                             template='plotly_white')
            return fig
        except Exception as e:
            logger.error(f"Error creating histogram: {str(e)}")
            return None
    
    @staticmethod
    def create_box_chart(df, y_col, x_col=None, title="Box Chart"):
        """Create box chart for distribution"""
        try:
            fig = px.box(df, y=y_col, x=x_col, title=title,
                        template='plotly_white')
            return fig
        except Exception as e:
            logger.error(f"Error creating box chart: {str(e)}")
            return None
