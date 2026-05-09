# """
# Data Processing Pipeline Module
# Transforms and cleans data for analysis
# """

# import pandas as pd
# from datetime import datetime, timedelta
# from core.logger import get_logger
# from core.config import Config
# from core.constants import *

# logger = get_logger(__name__)


# class ProcessingPipeline:
#     """Data processing and transformation pipeline"""
    
#     def __init__(self):
#         """Initialize processing pipeline"""
#         logger.info("✓ Processing pipeline initialized")
    
#     def normalize_prices(self, df):
#         """
#         Normalize and validate price data
        
#         Args:
#             df (pd.DataFrame): Data to process
        
#         Returns:
#             pd.DataFrame: Processed data
#         """
#         try:
#             # Ensure prices are within valid range
#             df['unit_price'] = df['unit_price'].clip(lower=MIN_PRICE, upper=MAX_PRICE)
#             logger.info("✓ Prices normalized")
#             return df
#         except Exception as e:
#             logger.error(f"Error normalizing prices: {str(e)}")
#             return df
    
#     def normalize_stock_levels(self, df):
#         """
#         Normalize stock levels
        
#         Args:
#             df (pd.DataFrame): Data to process
        
#         Returns:
#             pd.DataFrame: Processed data
#         """
#         try:
#             # Ensure stock levels are non-negative
#             stock_columns = ['current_stock', 'min_stock', 'max_stock']
#             for col in stock_columns:
#                 if col in df.columns:
#                     df[col] = df[col].clip(lower=0)
            
#             logger.info("✓ Stock levels normalized")
#             return df
#         except Exception as e:
#             logger.error(f"Error normalizing stock levels: {str(e)}")
#             return df
    
#     def calculate_inventory_value(self, df):
#         """
#         Calculate inventory value per medicine
        
#         Args:
#             df (pd.DataFrame): Data to process
        
#         Returns:
#             pd.DataFrame: Data with inventory_value column
#         """
#         try:
#             df['inventory_value'] = df['current_stock'] * df['unit_price']
#             logger.info("✓ Inventory values calculated")
#             return df
#         except Exception as e:
#             logger.error(f"Error calculating inventory value: {str(e)}")
#             return df
    
#     def calculate_stock_status(self, df):
#         """
#         Calculate stock status for each medicine
        
#         Args:
#             df (pd.DataFrame): Data to process
        
#         Returns:
#             pd.DataFrame: Data with stock_status column
#         """
#         try:
#             def get_status(row):
#                 current = row['current_stock']
#                 min_stock = row['min_stock']
#                 max_stock = row['max_stock']
                
#                 if current == 0:
#                     return STOCK_STATUS_OUT
#                 elif current < min_stock:
#                     return STOCK_STATUS_CRITICAL
#                 elif current < min_stock * 2:
#                     return STOCK_STATUS_LOW
#                 elif current > max_stock:
#                     return STOCK_STATUS_HIGH
#                 else:
#                     return STOCK_STATUS_NORMAL
            
#             df['stock_status'] = df.apply(get_status, axis=1)
#             logger.info("✓ Stock status calculated")
#             return df
#         except Exception as e:
#             logger.error(f"Error calculating stock status: {str(e)}")
#             return df
    
#     def calculate_days_to_expiry(self, df):
#         """
#         Calculate days until expiry for each medicine
        
#         Args:
#             df (pd.DataFrame): Data to process
        
#         Returns:
#             pd.DataFrame: Data with days_to_expiry column
#         """
#         try:
#             df['expiry_date'] = pd.to_datetime(df['expiry_date'])
#             today = pd.Timestamp.now()
#             df['days_to_expiry'] = (df['expiry_date'] - today).dt.days
#             logger.info("✓ Days to expiry calculated")
#             return df
#         except Exception as e:
#             logger.error(f"Error calculating days to expiry: {str(e)}")
#             return df
    
#     def categorize_medicines(self, df):
#         """
#         Ensure medicine categories are valid
        
#         Args:
#             df (pd.DataFrame): Data to process
        
#         Returns:
#             pd.DataFrame: Processed data
#         """
#         try:
#             # Replace invalid categories with 'Other'
#             df['category'] = df['category'].apply(
#                 lambda x: x if x in CATEGORIES else 'Other'
#             )
#             logger.info("✓ Medicine categories validated")
#             return df
#         except Exception as e:
#             logger.error(f"Error categorizing medicines: {str(e)}")
#             return df
    
#     def aggregate_by_category(self, df):
#         """
#         Aggregate data by medicine category
        
#         Args:
#             df (pd.DataFrame): Data to process
        
#         Returns:
#             pd.DataFrame: Aggregated data
#         """
#         try:
#             aggregated = df.groupby('category').agg({
#                 'medicine_id': 'count',
#                 'current_stock': 'sum',
#                 'unit_price': 'mean',
#                 'inventory_value': 'sum'
#             }).rename(columns={'medicine_id': 'count'})
            
#             logger.info("✓ Data aggregated by category")
#             return aggregated
#         except Exception as e:
#             logger.error(f"Error aggregating by category: {str(e)}")
#             return df
    
#     def identify_fast_moving_medicines(self, df, top_n=10):
#         """
#         Identify fast-moving medicines (high turnover)
        
#         Args:
#             df (pd.DataFrame): Data to process
#             top_n (int): Number of top medicines to identify
        
#         Returns:
#             pd.DataFrame: Fast-moving medicines
#         """
#         try:
#             # Sort by inventory value and current stock usage pattern
#             fast_moving = df.nlargest(top_n, 'inventory_value')
#             logger.info(f"✓ Identified {len(fast_moving)} fast-moving medicines")
#             return fast_moving
#         except Exception as e:
#             logger.error(f"Error identifying fast-moving medicines: {str(e)}")
#             return pd.DataFrame()
    
#     def identify_slow_moving_medicines(self, df, bottom_n=10):
#         """
#         Identify slow-moving medicines (low turnover)
        
#         Args:
#             df (pd.DataFrame): Data to process
#             bottom_n (int): Number of bottom medicines to identify
        
#         Returns:
#             pd.DataFrame: Slow-moving medicines
#         """
#         try:
#             slow_moving = df.nsmallest(bottom_n, 'inventory_value')
#             logger.info(f"✓ Identified {len(slow_moving)} slow-moving medicines")
#             return slow_moving
#         except Exception as e:
#             logger.error(f"Error identifying slow-moving medicines: {str(e)}")
#             return pd.DataFrame()
    
#     def process_data(self, df):
#         """
#         Main data processing pipeline
        
#         Args:
#             df (pd.DataFrame): Raw data to process
        
#         Returns:
#             pd.DataFrame: Processed data ready for analysis
#         """
#         try:
#             logger.info("=" * 60)
#             logger.info("STARTING DATA PROCESSING PIPELINE")
#             logger.info("=" * 60)
            
#             # Apply processing steps
#             df = self.normalize_prices(df)
#             df = self.normalize_stock_levels(df)
#             df = self.calculate_inventory_value(df)
#             df = self.calculate_stock_status(df)
#             df = self.calculate_days_to_expiry(df)
#             df = self.categorize_medicines(df)
            
#             logger.info(f"✓ Processing completed: {len(df)} records processed")
#             logger.info("=" * 60)
            
#             return df
#         except Exception as e:
#             logger.error(f"Processing pipeline failed: {str(e)}")
#             raise


# def process_data(df):
#     """Convenience function for data processing"""
#     pipeline = ProcessingPipeline()
#     return pipeline.process_data(df)


# if __name__ == "__main__":
#     print("🚀 Running processing pipeline...")

#     try:
#         # Load data from ingestion
#         from pipelines.ingestion_pipeline import ingest_data
#         df = ingest_data()

#         # Process data
#         processed_df = process_data(df)

#         # Save to processed folder
#         from services.database_service import get_database_service
#         db = get_database_service()
#         db.save_medicine_data(processed_df)

#         print(f"✅ Processing complete: {len(processed_df)} records saved")

#     except Exception as e:
#         print(f"❌ Processing failed: {e}")

"""
Data Processing Pipeline Module
Transforms and cleans data for analysis
"""

import pandas as pd
from datetime import datetime, timedelta
from core.logger import get_logger
from core.config import Config
from core.constants import *

# NEW IMPORT
from models.features import FeatureEngineering

logger = get_logger(__name__)


class ProcessingPipeline:
    """Data processing and transformation pipeline"""

    def __init__(self):
        """Initialize processing pipeline"""
        logger.info("✓ Processing pipeline initialized")

    def normalize_prices(self, df):
        """
        Normalize and validate price data

        Args:
            df (pd.DataFrame): Data to process

        Returns:
            pd.DataFrame: Processed data
        """
        try:
            # Ensure prices are within valid range
            df['unit_price'] = df['unit_price'].clip(
                lower=MIN_PRICE,
                upper=MAX_PRICE
            )

            logger.info("✓ Prices normalized")
            return df

        except Exception as e:
            logger.error(f"Error normalizing prices: {str(e)}")
            return df

    def normalize_stock_levels(self, df):
        """
        Normalize stock levels

        Args:
            df (pd.DataFrame): Data to process

        Returns:
            pd.DataFrame: Processed data
        """
        try:
            # Ensure stock levels are non-negative
            stock_columns = [
                'current_stock',
                'min_stock',
                'max_stock'
            ]

            for col in stock_columns:
                if col in df.columns:
                    df[col] = df[col].clip(lower=0)

            logger.info("✓ Stock levels normalized")
            return df

        except Exception as e:
            logger.error(f"Error normalizing stock levels: {str(e)}")
            return df

    def calculate_inventory_value(self, df):
        """
        Calculate inventory value per medicine
        """
        try:
            df['inventory_value'] = (
                df['current_stock'] * df['unit_price']
            )

            logger.info("✓ Inventory values calculated")
            return df

        except Exception as e:
            logger.error(f"Error calculating inventory value: {str(e)}")
            return df

    def calculate_stock_status(self, df):
        """
        Calculate stock status for each medicine
        """
        try:

            def get_status(row):

                current = row['current_stock']
                min_stock = row['min_stock']
                max_stock = row['max_stock']

                if current == 0:
                    return STOCK_STATUS_OUT

                elif current < min_stock:
                    return STOCK_STATUS_CRITICAL

                elif current < min_stock * 2:
                    return STOCK_STATUS_LOW

                elif current > max_stock:
                    return STOCK_STATUS_HIGH

                else:
                    return STOCK_STATUS_NORMAL

            df['stock_status'] = df.apply(
                get_status,
                axis=1
            )

            logger.info("✓ Stock status calculated")
            return df

        except Exception as e:
            logger.error(f"Error calculating stock status: {str(e)}")
            return df

    def calculate_days_to_expiry(self, df):
        """
        Calculate days until expiry for each medicine
        """
        try:

            df['expiry_date'] = pd.to_datetime(
                df['expiry_date']
            )

            today = pd.Timestamp.now()

            df['days_to_expiry'] = (
                df['expiry_date'] - today
            ).dt.days

            logger.info("✓ Days to expiry calculated")
            return df

        except Exception as e:
            logger.error(f"Error calculating days to expiry: {str(e)}")
            return df

    def categorize_medicines(self, df):
        """
        Ensure medicine categories are valid
        """
        try:

            # Replace invalid categories with 'Other'
            df['category'] = df['category'].apply(
                lambda x: x if x in CATEGORIES else 'Other'
            )

            logger.info("✓ Medicine categories validated")
            return df

        except Exception as e:
            logger.error(f"Error categorizing medicines: {str(e)}")
            return df

    def aggregate_by_category(self, df):
        """
        Aggregate data by medicine category
        """
        try:

            aggregated = df.groupby('category').agg({
                'medicine_id': 'count',
                'current_stock': 'sum',
                'unit_price': 'mean',
                'inventory_value': 'sum'
            }).rename(columns={'medicine_id': 'count'})

            logger.info("✓ Data aggregated by category")
            return aggregated

        except Exception as e:
            logger.error(f"Error aggregating by category: {str(e)}")
            return df

    def identify_fast_moving_medicines(self, df, top_n=10):
        """
        Identify fast-moving medicines
        """
        try:

            fast_moving = df.nlargest(
                top_n,
                'inventory_value'
            )

            logger.info(
                f"✓ Identified {len(fast_moving)} fast-moving medicines"
            )

            return fast_moving

        except Exception as e:
            logger.error(
                f"Error identifying fast-moving medicines: {str(e)}"
            )

            return pd.DataFrame()

    def identify_slow_moving_medicines(self, df, bottom_n=10):
        """
        Identify slow-moving medicines
        """
        try:

            slow_moving = df.nsmallest(
                bottom_n,
                'inventory_value'
            )

            logger.info(
                f"✓ Identified {len(slow_moving)} slow-moving medicines"
            )

            return slow_moving

        except Exception as e:
            logger.error(
                f"Error identifying slow-moving medicines: {str(e)}"
            )

            return pd.DataFrame()

    # ==========================================================
    # NEW FEATURE ENGINEERING METHOD
    # ==========================================================

    def generate_features(self, df):
        """
        Generate analytical features
        """

        try:

            # Moving Average
            df['moving_avg'] = (
                FeatureEngineering.calculate_moving_average(
                    df['current_stock']
                )
            )

            # Volatility
            df['volatility'] = (
                FeatureEngineering.calculate_volatility(
                    df['current_stock']
                )
            )

            # Rate of Change
            df['rate_of_change'] = (
                FeatureEngineering.calculate_rate_of_change(
                    df['current_stock']
                )
            )

            # Trend
            trend = FeatureEngineering.calculate_trend(
                df['current_stock']
            )

            df['trend'] = trend

            logger.info("✓ Feature engineering completed")

            return df

        except Exception as e:
            logger.error(
                f"Error generating features: {str(e)}"
            )

            return df

    def process_data(self, df):
        """
        Main data processing pipeline
        """
        try:

            logger.info("=" * 60)
            logger.info("STARTING DATA PROCESSING PIPELINE")
            logger.info("=" * 60)

            # Existing processing steps
            df = self.normalize_prices(df)

            df = self.normalize_stock_levels(df)

            df = self.calculate_inventory_value(df)

            df = self.calculate_stock_status(df)

            df = self.calculate_days_to_expiry(df)

            df = self.categorize_medicines(df)

            # ==================================================
            # NEW FEATURE ENGINEERING STEP
            # ==================================================

            df = self.generate_features(df)

            logger.info(
                f"✓ Processing completed: {len(df)} records processed"
            )

            logger.info("=" * 60)

            return df

        except Exception as e:
            logger.error(
                f"Processing pipeline failed: {str(e)}"
            )

            raise


def process_data(df):
    """
    Convenience function for data processing
    """
    pipeline = ProcessingPipeline()
    return pipeline.process_data(df)


# ==============================================================
# MAIN EXECUTION
# ==============================================================

if __name__ == "__main__":

    print("🚀 Running processing pipeline...")

    try:

        # Load data from ingestion
        from pipelines.ingestion_pipeline import ingest_data

        df = ingest_data()

        # Process data
        processed_df = process_data(df)

        # ======================================================
        # SAVE ENRICHED CSV
        # ======================================================

        processed_df.to_csv(
            "data/processed/enriched_inventory.csv",
            index=False
        )

        print(
            "✓ Enriched inventory saved to "
            "data/processed/enriched_inventory.csv"
        )

        # Save to database
        from services.database_service import get_database_service

        db = get_database_service()

        db.save_medicine_data(processed_df)

        print(
            f"✅ Processing complete: "
            f"{len(processed_df)} records saved"
        )

    except Exception as e:

        print(f"❌ Processing failed: {e}")