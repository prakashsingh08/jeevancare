"""
Data Ingestion Pipeline Module
Loads and validates raw data from sources
"""

import pandas as pd
from pathlib import Path
from core.logger import get_logger
from core.config import Config
from core.constants import REQUIRED_COLUMNS
import os

logger = get_logger(__name__)


class IngestionPipeline:
    """Data ingestion and validation pipeline"""
    
    def __init__(self):
        """Initialize ingestion pipeline"""
        self.raw_data_path = Path(Config.DATA_RAW_PATH)
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        self.validation_report = {}
        logger.info("✓ Ingestion pipeline initialized")
    
    def load_raw_data(self, file_path=None):
        """
        Load raw data from CSV file
        
        Args:
            file_path (str): Path to CSV file. If None, uses default path
        
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            if file_path is None:
                # Use default path
                file_path = self.raw_data_path / Config.SAMPLE_DATA_FILE
            
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Data file not found: {file_path}")
            
            df = pd.read_csv(file_path)
            logger.info(f"✓ Loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Error loading raw data: {str(e)}")
            raise
    
    def validate_data_schema(self, df):
        """
        Validate data structure and schema
        
        Args:
            df (pd.DataFrame): Data to validate
        
        Returns:
            bool: Validation result
        """
        try:
            missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
            
            if missing_columns:
                error_msg = f"Missing required columns: {missing_columns}"
                logger.error(error_msg)
                self.validation_report['schema_valid'] = False
                self.validation_report['missing_columns'] = list(missing_columns)
                return False
            
            logger.info("✓ Data schema validation passed")
            self.validation_report['schema_valid'] = True
            return True
        except Exception as e:
            logger.error(f"Error validating schema: {str(e)}")
            return False
    
    def handle_missing_values(self, df):
        """
        Handle missing or null values
        
        Args:
            df (pd.DataFrame): Data to process
        
        Returns:
            pd.DataFrame: Processed data
        """
        try:
            # Check for missing values
            missing_count = df.isnull().sum().sum()
            if missing_count > 0:
                logger.warning(f"Found {missing_count} missing values")
                
                # Fill numeric columns with median
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                
                # Fill text columns with 'Unknown'
                text_cols = df.select_dtypes(include=['object']).columns
                df[text_cols] = df[text_cols].fillna('Unknown')
                
                logger.info(f"✓ Handled missing values")
            
            self.validation_report['missing_values'] = missing_count
            return df
        except Exception as e:
            logger.error(f"Error handling missing values: {str(e)}")
            return df
    
    def validate_data_types(self, df):
        """
        Validate data types
        
        Args:
            df (pd.DataFrame): Data to validate
        
        Returns:
            bool: Validation result
        """
        try:
            # Validate numeric fields
            numeric_fields = ['medicine_id', 'current_stock', 'min_stock', 'max_stock', 'unit_price']
            for field in numeric_fields:
                if field in df.columns:
                    if not pd.api.types.is_numeric_dtype(df[field]):
                        logger.warning(f"Converting {field} to numeric")
                        df[field] = pd.to_numeric(df[field], errors='coerce')
            
            # Validate date fields
            if 'expiry_date' in df.columns:
                df['expiry_date'] = pd.to_datetime(df['expiry_date'], errors='coerce')
            
            logger.info("✓ Data type validation completed")
            self.validation_report['type_valid'] = True
            return True
        except Exception as e:
            logger.error(f"Error validating data types: {str(e)}")
            return False
    
    def remove_duplicates(self, df):
        """
        Remove duplicate records
        
        Args:
            df (pd.DataFrame): Data to process
        
        Returns:
            pd.DataFrame: Data without duplicates
        """
        try:
            duplicate_count = df.duplicated().sum()
            if duplicate_count > 0:
                logger.warning(f"Found {duplicate_count} duplicate records")
                df = df.drop_duplicates()
                logger.info(f"✓ Removed {duplicate_count} duplicates")
            
            self.validation_report['duplicates_removed'] = duplicate_count
            return df
        except Exception as e:
            logger.error(f"Error removing duplicates: {str(e)}")
            return df
    
    def get_ingestion_report(self):
        """Get validation report"""
        return self.validation_report
    
    def ingest_data(self, file_path=None):
        """
        Main ingestion pipeline
        
        Args:
            file_path (str): Path to raw data file
        
        Returns:
            pd.DataFrame: Validated and processed data
        """
        try:
            logger.info("=" * 60)
            logger.info("STARTING DATA INGESTION PIPELINE")
            logger.info("=" * 60)
            
            # Load raw data
            df = self.load_raw_data(file_path)
            
            # Validate schema
            if not self.validate_data_schema(df):
                raise ValueError("Schema validation failed")
            
            # Handle missing values
            df = self.handle_missing_values(df)
            
            # Validate data types
            self.validate_data_types(df)
            
            # Remove duplicates
            df = self.remove_duplicates(df)
            
            logger.info(f"✓ Ingestion completed: {len(df)} records processed")
            logger.info("=" * 60)
            
            return df
        except Exception as e:
            logger.error(f"Ingestion pipeline failed: {str(e)}")
            raise


def ingest_data(file_path=None):
    """Convenience function for data ingestion"""
    pipeline = IngestionPipeline()
    return pipeline.ingest_data(file_path)

if __name__ == "__main__":
    print("🚀 Running ingestion pipeline...")

    try:
        df = ingest_data()
        print(f"✅ Ingestion successful: {len(df)} records")

    except Exception as e:
        print(f"❌ Ingestion failed: {e}")