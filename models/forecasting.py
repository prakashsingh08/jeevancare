# """
# Forecasting Module
# Demand forecasting models and predictions
# """

# import pandas as pd
# import numpy as np
# from datetime import timedelta
# from core.logger import get_logger
# from models.features import FeatureEngineering

# logger = get_logger(__name__)


# class ForecastingModels:
#     """Forecasting models for demand prediction"""
    
#     @staticmethod
#     def moving_average_forecast(historical_data, periods=30, window=7):
#         """
#         Simple moving average forecast
        
#         Args:
#             historical_data (pd.Series or list): Historical values
#             periods (int): Number of periods to forecast
#             window (int): Window size for moving average
        
#         Returns:
#             pd.Series: Forecast values
#         """
#         try:
#             if isinstance(historical_data, list):
#                 historical_data = pd.Series(historical_data)
            
#             # Calculate moving average
#             ma = FeatureEngineering.calculate_moving_average(historical_data, window)
            
#             # Use the last MA value for all future predictions
#             last_ma = ma.iloc[-1]
#             forecast = pd.Series([last_ma] * periods, index=range(len(historical_data), len(historical_data) + periods))
            
#             logger.info(f"✓ Moving average forecast generated ({periods} periods)")
#             return forecast
#         except Exception as e:
#             logger.error(f"Error in moving average forecast: {str(e)}")
#             return None
    
#     @staticmethod
#     def exponential_smoothing_forecast(historical_data, periods=30, alpha=0.2):
#         """
#         Exponential smoothing forecast
        
#         Args:
#             historical_data (pd.Series or list): Historical values
#             periods (int): Number of periods to forecast
#             alpha (float): Smoothing factor (0-1)
        
#         Returns:
#             pd.Series: Forecast values
#         """
#         try:
#             if isinstance(historical_data, list):
#                 historical_data = pd.Series(historical_data)
            
#             # Simple exponential smoothing
#             smoothed = [historical_data.iloc[0]]
            
#             for i in range(1, len(historical_data)):
#                 smoothed.append(alpha * historical_data.iloc[i] + (1 - alpha) * smoothed[i-1])
            
#             # Use last smoothed value for forecast
#             last_smoothed = smoothed[-1]
#             forecast = pd.Series([last_smoothed] * periods, index=range(len(historical_data), len(historical_data) + periods))
            
#             logger.info(f"✓ Exponential smoothing forecast generated ({periods} periods)")
#             return forecast
#         except Exception as e:
#             logger.error(f"Error in exponential smoothing: {str(e)}")
#             return None
    
#     @staticmethod
#     def linear_trend_forecast(historical_data, periods=30):
#         """
#         Linear trend extrapolation forecast
        
#         Args:
#             historical_data (pd.Series or list): Historical values
#             periods (int): Number of periods to forecast
        
#         Returns:
#             pd.Series: Forecast values
#         """
#         try:
#             if isinstance(historical_data, list):
#                 historical_data = pd.Series(historical_data)
            
#             # Fit linear trend
#             x = np.arange(len(historical_data))
#             coeffs = np.polyfit(x, historical_data, 1)
            
#             # Generate forecast
#             future_x = np.arange(len(historical_data), len(historical_data) + periods)
#             forecast = np.polyval(coeffs, future_x)
#             forecast = pd.Series(forecast, index=future_x)
            
#             logger.info(f"✓ Linear trend forecast generated ({periods} periods)")
#             return forecast
#         except Exception as e:
#             logger.error(f"Error in linear trend forecast: {str(e)}")
#             return None
    
#     @staticmethod
#     def calculate_forecast_accuracy(actual, predicted):
#         """
#         Calculate forecast accuracy metrics
        
#         Args:
#             actual (pd.Series or list): Actual values
#             predicted (pd.Series or list): Predicted values
        
#         Returns:
#             dict: Accuracy metrics (MAE, RMSE, MAPE)
#         """
#         try:
#             if isinstance(actual, list):
#                 actual = np.array(actual)
#             if isinstance(predicted, list):
#                 predicted = np.array(predicted)
            
#             # Ensure same length
#             min_len = min(len(actual), len(predicted))
#             actual = actual[:min_len]
#             predicted = predicted[:min_len]
            
#             # Calculate metrics
#             mae = np.mean(np.abs(actual - predicted))
#             rmse = np.sqrt(np.mean((actual - predicted) ** 2))
#             mape = np.mean(np.abs((actual - predicted) / actual)) * 100 if np.all(actual != 0) else 0
            
#             metrics = {
#                 'MAE': round(mae, 2),
#                 'RMSE': round(rmse, 2),
#                 'MAPE': round(mape, 2)
#             }
            
#             logger.info(f"✓ Forecast accuracy calculated: MAE={mae}, RMSE={rmse}, MAPE={mape}%")
#             return metrics
#         except Exception as e:
#             logger.error(f"Error calculating forecast accuracy: {str(e)}")
#             return {}
    
#     @staticmethod
#     def generate_confidence_interval(forecast, std_dev, confidence=0.95):
#         """
#         Generate confidence intervals for forecast
        
#         Args:
#             forecast (pd.Series): Forecast values
#             std_dev (float): Standard deviation of historical data
#             confidence (float): Confidence level (0-1)
        
#         Returns:
#             dict: Upper and lower bounds
#         """
#         try:
#             # Z-score for confidence level (1.96 for 95%)
#             z_score = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
#             z = z_score.get(confidence, 1.96)
            
#             margin = z * std_dev
            
#             result = {
#                 'forecast': forecast,
#                 'upper_bound': forecast + margin,
#                 'lower_bound': forecast - margin,
#                 'margin': margin
#             }
            
#             logger.info(f"✓ Confidence interval generated ({confidence*100}% confidence)")
#             return result
#         except Exception as e:
#             logger.error(f"Error generating confidence interval: {str(e)}")
#             return {}
    
#     @staticmethod
#     def forecast_demand(historical_data, periods=30, method='moving_average'):
#         """
#         Main forecasting function
        
#         Args:
#             historical_data (pd.Series or list): Historical demand data
#             periods (int): Number of periods to forecast
#             method (str): Forecasting method
        
#         Returns:
#             dict: Forecast results with predictions and metrics
#         """
#         try:
#             if isinstance(historical_data, list):
#                 historical_data = pd.Series(historical_data)
            
#             logger.info("=" * 60)
#             logger.info("STARTING DEMAND FORECASTING")
#             logger.info("=" * 60)
            
#             # Select forecasting method
#             if method == 'moving_average':
#                 forecast = ForecastingModels.moving_average_forecast(historical_data, periods)
#             elif method == 'exponential_smoothing':
#                 forecast = ForecastingModels.exponential_smoothing_forecast(historical_data, periods)
#             elif method == 'linear_trend':
#                 forecast = ForecastingModels.linear_trend_forecast(historical_data, periods)
#             else:
#                 logger.warning(f"Unknown method {method}, using moving average")
#                 forecast = ForecastingModels.moving_average_forecast(historical_data, periods)
            
#             # Calculate statistics
#             std_dev = historical_data.std()
            
#             # Generate confidence intervals
#             ci = ForecastingModels.generate_confidence_interval(forecast, std_dev)
            
#             result = {
#                 'forecast': forecast,
#                 'confidence_interval': ci,
#                 'method': method,
#                 'periods': periods,
#                 'historical_mean': historical_data.mean(),
#                 'historical_std': std_dev
#             }
            
#             logger.info("✓ Forecasting completed")
#             logger.info("=" * 60)
            
#             return result
#         except Exception as e:
#             logger.error(f"Forecasting failed: {str(e)}")
#             raise


# def forecast_demand(historical_data, periods=30, method='moving_average'):
#     """Convenience function"""
#     return ForecastingModels.forecast_demand(historical_data, periods, method)

"""
Forecasting Module
Demand forecasting models and predictions
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from core.logger import get_logger
from models.features import FeatureEngineering

logger = get_logger(__name__)


class ForecastingModels:
    """Forecasting models for demand prediction"""

    @staticmethod
    def moving_average_forecast(
        historical_data,
        periods=30,
        window=7
    ):
        """
        Simple moving average forecast
        """

        try:

            if isinstance(historical_data, list):
                historical_data = pd.Series(historical_data)

            # Feature: Moving Average
            ma = FeatureEngineering.calculate_moving_average(
                historical_data,
                window
            )

            # Use latest MA value
            last_ma = ma.iloc[-1]

            forecast = pd.Series(
                [last_ma] * periods,
                index=range(
                    len(historical_data),
                    len(historical_data) + periods
                )
            )

            logger.info(
                f"✓ Moving average forecast generated "
                f"({periods} periods)"
            )

            return forecast

        except Exception as e:

            logger.error(
                f"Error in moving average forecast: {str(e)}"
            )

            return None

    @staticmethod
    def exponential_smoothing_forecast(
        historical_data,
        periods=30,
        alpha=0.2
    ):
        """
        Exponential smoothing forecast
        """

        try:

            if isinstance(historical_data, list):
                historical_data = pd.Series(historical_data)

            smoothed = [historical_data.iloc[0]]

            for i in range(1, len(historical_data)):

                smoothed.append(
                    alpha * historical_data.iloc[i]
                    + (1 - alpha) * smoothed[i - 1]
                )

            last_smoothed = smoothed[-1]

            forecast = pd.Series(
                [last_smoothed] * periods,
                index=range(
                    len(historical_data),
                    len(historical_data) + periods
                )
            )

            logger.info(
                f"✓ Exponential smoothing forecast generated "
                f"({periods} periods)"
            )

            return forecast

        except Exception as e:

            logger.error(
                f"Error in exponential smoothing: {str(e)}"
            )

            return None

    @staticmethod
    def linear_trend_forecast(
        historical_data,
        periods=30
    ):
        """
        Linear trend extrapolation forecast
        """

        try:

            if isinstance(historical_data, list):
                historical_data = pd.Series(historical_data)

            # Feature: Trend Detection
            trend = FeatureEngineering.calculate_trend(
                historical_data
            )

            x = np.arange(len(historical_data))

            coeffs = np.polyfit(
                x,
                historical_data,
                1
            )

            future_x = np.arange(
                len(historical_data),
                len(historical_data) + periods
            )

            forecast = np.polyval(
                coeffs,
                future_x
            )

            forecast = pd.Series(
                forecast,
                index=future_x
            )

            logger.info(
                f"✓ Linear trend forecast generated "
                f"({periods} periods)"
            )

            logger.info(f"✓ Detected trend: {trend}")

            return forecast

        except Exception as e:

            logger.error(
                f"Error in linear trend forecast: {str(e)}"
            )

            return None

    @staticmethod
    def advanced_feature_forecast(
        historical_data,
        periods=30
    ):
        """
        Advanced forecasting using multiple features
        """

        try:

            if isinstance(historical_data, list):
                historical_data = pd.Series(historical_data)

            # ==================================================
            # FEATURE ENGINEERING
            # ==================================================

            moving_avg = (
                FeatureEngineering.calculate_moving_average(
                    historical_data
                )
            )

            volatility = (
                FeatureEngineering.calculate_volatility(
                    historical_data
                )
            )

            rate_of_change = (
                FeatureEngineering.calculate_rate_of_change(
                    historical_data
                )
            )

            seasonality = (
                FeatureEngineering.calculate_seasonality(
                    historical_data
                )
            )

            trend = (
                FeatureEngineering.calculate_trend(
                    historical_data
                )
            )

            # ==================================================
            # FORECAST LOGIC
            # ==================================================

            base_value = moving_avg.iloc[-1]

            # Trend adjustment
            if trend == 'increasing':
                growth_factor = 1.10

            elif trend == 'decreasing':
                growth_factor = 0.90

            else:
                growth_factor = 1.00

            forecast_values = []

            for i in range(periods):

                seasonal_adjustment = (
                    seasonality.iloc[-1]
                    if len(seasonality) > 0
                    else 0
                )

                future_value = (
                    base_value
                    * growth_factor
                )

                # Add seasonality influence
                future_value += seasonal_adjustment * 0.05

                # Add volatility adjustment
                if not volatility.empty:
                    future_value += (
                        volatility.iloc[-1] * 0.02
                    )

                forecast_values.append(
                    round(future_value, 2)
                )

            forecast = pd.Series(
                forecast_values,
                index=range(
                    len(historical_data),
                    len(historical_data) + periods
                )
            )

            logger.info(
                "✓ Advanced feature-based forecast generated"
            )

            logger.info(f"✓ Trend: {trend}")

            return forecast

        except Exception as e:

            logger.error(
                f"Error in advanced forecasting: {str(e)}"
            )

            return None

    @staticmethod
    def calculate_forecast_accuracy(
        actual,
        predicted
    ):
        """
        Calculate forecast accuracy metrics
        """

        try:

            if isinstance(actual, list):
                actual = np.array(actual)

            if isinstance(predicted, list):
                predicted = np.array(predicted)

            min_len = min(
                len(actual),
                len(predicted)
            )

            actual = actual[:min_len]
            predicted = predicted[:min_len]

            mae = np.mean(
                np.abs(actual - predicted)
            )

            rmse = np.sqrt(
                np.mean(
                    (actual - predicted) ** 2
                )
            )

            if np.all(actual != 0):

                mape = np.mean(
                    np.abs(
                        (actual - predicted) / actual
                    )
                ) * 100

            else:
                mape = 0

            metrics = {
                'MAE': round(mae, 2),
                'RMSE': round(rmse, 2),
                'MAPE': round(mape, 2)
            }

            logger.info(
                "✓ Forecast accuracy calculated"
            )

            return metrics

        except Exception as e:

            logger.error(
                f"Error calculating forecast accuracy: "
                f"{str(e)}"
            )

            return {}

    @staticmethod
    def generate_confidence_interval(
        forecast,
        std_dev,
        confidence=0.95
    ):
        """
        Generate confidence intervals
        """

        try:

            z_score = {
                0.90: 1.645,
                0.95: 1.96,
                0.99: 2.576
            }

            z = z_score.get(
                confidence,
                1.96
            )

            margin = z * std_dev

            result = {
                'forecast': forecast,
                'upper_bound': forecast + margin,
                'lower_bound': forecast - margin,
                'margin': margin
            }

            logger.info(
                f"✓ Confidence interval generated "
                f"({confidence*100}% confidence)"
            )

            return result

        except Exception as e:

            logger.error(
                f"Error generating confidence interval: "
                f"{str(e)}"
            )

            return {}

    @staticmethod
    def forecast_demand(
        historical_data,
        periods=30,
        method='advanced'
    ):
        """
        Main forecasting function
        """

        try:

            if isinstance(historical_data, list):
                historical_data = pd.Series(
                    historical_data
                )

            logger.info("=" * 60)
            logger.info(
                "STARTING DEMAND FORECASTING"
            )
            logger.info("=" * 60)

            # ==================================================
            # SELECT FORECAST METHOD
            # ==================================================

            if method == 'moving_average':

                forecast = (
                    ForecastingModels.moving_average_forecast(
                        historical_data,
                        periods
                    )
                )

            elif method == 'exponential_smoothing':

                forecast = (
                    ForecastingModels.exponential_smoothing_forecast(
                        historical_data,
                        periods
                    )
                )

            elif method == 'linear_trend':

                forecast = (
                    ForecastingModels.linear_trend_forecast(
                        historical_data,
                        periods
                    )
                )

            elif method == 'advanced':

                forecast = (
                    ForecastingModels.advanced_feature_forecast(
                        historical_data,
                        periods
                    )
                )

            else:

                logger.warning(
                    f"Unknown method {method}, "
                    f"using advanced forecasting"
                )

                forecast = (
                    ForecastingModels.advanced_feature_forecast(
                        historical_data,
                        periods
                    )
                )

            # ==================================================
            # FEATURE ANALYTICS
            # ==================================================

            trend = FeatureEngineering.calculate_trend(
                historical_data
            )

            volatility = (
                FeatureEngineering.calculate_volatility(
                    historical_data
                )
            )

            roc = (
                FeatureEngineering.calculate_rate_of_change(
                    historical_data
                )
            )

            # ==================================================
            # STATISTICS
            # ==================================================

            std_dev = historical_data.std()

            ci = (
                ForecastingModels.generate_confidence_interval(
                    forecast,
                    std_dev
                )
            )

            result = {

                'forecast': forecast,

                'confidence_interval': ci,

                'method': method,

                'periods': periods,

                'historical_mean': historical_data.mean(),

                'historical_std': std_dev,

                # ==============================================
                # FEATURE OUTPUTS
                # ==============================================

                'trend': trend,

                'latest_volatility': (
                    volatility.iloc[-1]
                    if volatility is not None
                    else None
                ),

                'latest_rate_of_change': (
                    roc.iloc[-1]
                    if roc is not None
                    else None
                )
            }

            logger.info(
                "✓ Forecasting completed successfully"
            )

            logger.info("=" * 60)

            return result

        except Exception as e:

            logger.error(
                f"Forecasting failed: {str(e)}"
            )

            raise


def forecast_demand(
    historical_data,
    periods=30,
    method='advanced'
):
    """
    Convenience function
    """

    return ForecastingModels.forecast_demand(
        historical_data,
        periods,
        method
    )


# ==============================================================
# MAIN EXECUTION
# ==============================================================

if __name__ == "__main__":

    print("🚀 Running forecasting module...")

    sample_data = [
        100,
        120,
        130,
        150,
        170,
        180,
        200,
        210,
        230,
        250
    ]

    result = forecast_demand(
        historical_data=sample_data,
        periods=7,
        method='advanced'
    )

    print("\n📈 Forecast Results:")
    print(result['forecast'])

    print("\n📊 Trend:")
    print(result['trend'])

    print("\n📉 Volatility:")
    print(result['latest_volatility'])

    print("\n📈 Rate of Change:")
    print(result['latest_rate_of_change'])