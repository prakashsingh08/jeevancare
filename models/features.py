"""
Features Module
Feature engineering and feature calculation
"""

import pandas as pd
import numpy as np
from core.logger import get_logger

logger = get_logger(__name__)


class FeatureEngineering:
    """Feature engineering for forecasting and analysis"""
    
    @staticmethod
    def calculate_moving_average(data, window=7):
        """
        Calculate moving average
        
        Args:
            data (pd.Series or list): Time series data
            window (int): Window size for moving average
        
        Returns:
            pd.Series: Moving average values
        """
        try:
            if isinstance(data, list):
                data = pd.Series(data)
            
            ma = data.rolling(window=window, min_periods=1).mean()
            logger.debug(f"Calculated {window}-period moving average")
            return ma
        except Exception as e:
            logger.error(f"Error calculating moving average: {str(e)}")
            return None
    
    @staticmethod
    def calculate_exponential_moving_average(data, span=7):
        """
        Calculate exponential moving average
        
        Args:
            data (pd.Series or list): Time series data
            span (int): Span for EMA
        
        Returns:
            pd.Series: Exponential moving average values
        """
        try:
            if isinstance(data, list):
                data = pd.Series(data)
            
            ema = data.ewm(span=span, adjust=False).mean()
            logger.debug(f"Calculated EMA with span {span}")
            return ema
        except Exception as e:
            logger.error(f"Error calculating EMA: {str(e)}")
            return None
    
    @staticmethod
    def calculate_trend(data):
        """
        Calculate trend direction
        
        Args:
            data (pd.Series or list): Time series data
        
        Returns:
            str: 'increasing', 'decreasing', or 'stable'
        """
        try:
            if isinstance(data, list):
                data = pd.Series(data)
            
            if len(data) < 2:
                return 'stable'
            
            recent = data.iloc[-5:].mean() if len(data) >= 5 else data.iloc[-1]
            previous = data.iloc[-10:-5].mean() if len(data) >= 10 else data.iloc[0]
            
            if recent > previous * 1.1:
                return 'increasing'
            elif recent < previous * 0.9:
                return 'decreasing'
            else:
                return 'stable'
        except Exception as e:
            logger.error(f"Error calculating trend: {str(e)}")
            return 'unknown'
    
    @staticmethod
    def calculate_volatility(data, window=7):
        """
        Calculate data volatility (standard deviation)
        
        Args:
            data (pd.Series or list): Time series data
            window (int): Window size
        
        Returns:
            pd.Series: Volatility values
        """
        try:
            if isinstance(data, list):
                data = pd.Series(data)
            
            volatility = data.rolling(window=window, min_periods=1).std()
            logger.debug(f"Calculated volatility with window {window}")
            return volatility
        except Exception as e:
            logger.error(f"Error calculating volatility: {str(e)}")
            return None
    
    @staticmethod
    def calculate_seasonality(data, period=7):
        """
        Calculate seasonal component (weekly pattern)
        
        Args:
            data (pd.Series or list): Time series data
            period (int): Seasonal period (default 7 for weekly)
        
        Returns:
            pd.Series: Seasonal component
        """
        try:
            if isinstance(data, list):
                data = pd.Series(data)
            
            if len(data) < period:
                logger.warning("Insufficient data for seasonality calculation")
                return pd.Series([0] * len(data))
            
            seasonal = data.groupby(data.index % period).transform('mean')
            logger.debug(f"Calculated seasonality with period {period}")
            return seasonal
        except Exception as e:
            logger.error(f"Error calculating seasonality: {str(e)}")
            return None
    
    @staticmethod
    def normalize_features(df):
        """
        Normalize feature values to 0-1 range
        
        Args:
            df (pd.DataFrame): Data to normalize
        
        Returns:
            pd.DataFrame: Normalized data
        """
        try:
            normalized = df.copy()
            numeric_cols = normalized.select_dtypes(include=[np.number]).columns
            
            for col in numeric_cols:
                min_val = normalized[col].min()
                max_val = normalized[col].max()
                if max_val - min_val != 0:
                    normalized[col] = (normalized[col] - min_val) / (max_val - min_val)
            
            logger.info("✓ Features normalized")
            return normalized
        except Exception as e:
            logger.error(f"Error normalizing features: {str(e)}")
            return df
    
    @staticmethod
    def create_lag_features(data, lags=[1, 7, 14]):
        """
        Create lag features for time series
        
        Args:
            data (pd.Series): Time series data
            lags (list): Lag periods to create
        
        Returns:
            pd.DataFrame: DataFrame with lag features
        """
        try:
            df = pd.DataFrame({'value': data})
            
            for lag in lags:
                df[f'lag_{lag}'] = df['value'].shift(lag)
            
            logger.debug(f"Created lag features with periods {lags}")
            return df.dropna()
        except Exception as e:
            logger.error(f"Error creating lag features: {str(e)}")
            return None
    
    @staticmethod
    def calculate_rate_of_change(data, period=1):
        """
        Calculate rate of change
        
        Args:
            data (pd.Series or list): Time series data
            period (int): Period for rate calculation
        
        Returns:
            pd.Series: Rate of change
        """
        try:
            if isinstance(data, list):
                data = pd.Series(data)
            
            roc = data.pct_change(period) * 100
            logger.debug(f"Calculated rate of change with period {period}")
            return roc
        except Exception as e:
            logger.error(f"Error calculating rate of change: {str(e)}")
            return None


def calculate_moving_average(data, window=7):
    """Convenience function"""
    return FeatureEngineering.calculate_moving_average(data, window)


def calculate_trend(data):
    """Convenience function"""
    return FeatureEngineering.calculate_trend(data)


def normalize_features(df):
    """Convenience function"""
    return FeatureEngineering.normalize_features(df)
