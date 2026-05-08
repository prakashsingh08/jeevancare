"""
Database Service Module
Handles local data persistence and caching
"""

import pandas as pd
from pathlib import Path
from core.logger import get_logger
from core.config import Config
from datetime import datetime
import json

logger = get_logger(__name__)


class DatabaseService:
    """Local database operations and caching"""
    
    def __init__(self):
        """Initialize database service"""
        self.processed_data_path = Path(Config.DATA_PROCESSED_PATH)
        self.processed_data_path.mkdir(parents=True, exist_ok=True)
        self.medicines_file = self.processed_data_path / 'medicines.csv'
        self.medicines_cache = None
        logger.info("✓ Database service initialized")
    
    def save_medicine_data(self, df):
        """
        Save medicine data to local storage
        
        Args:
            df (pd.DataFrame): Medicine data to save
        
        Returns:
            bool: Success status
        """
        try:
            df.to_csv(self.medicines_file, index=False)
            self.medicines_cache = df  # Update cache
            logger.info(f"✓ Saved {len(df)} medicine records to {self.medicines_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving medicine data: {str(e)}")
            return False
    
    def load_medicine_data(self, use_cache=True):
        """
        Load medicine data from local storage
        
        Args:
            use_cache (bool): Use cached data if available
        
        Returns:
            pd.DataFrame: Medicine data
        """
        try:
            # Return cached data if requested and available
            if use_cache and self.medicines_cache is not None:
                logger.debug("Using cached medicine data")
                return self.medicines_cache
            
            # Load from file
            if self.medicines_file.exists():
                df = pd.read_csv(self.medicines_file)
                self.medicines_cache = df
                logger.info(f"✓ Loaded {len(df)} medicine records from {self.medicines_file}")
                return df
            else:
                logger.warning(f"Medicine data file not found at {self.medicines_file}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading medicine data: {str(e)}")
            return pd.DataFrame()
    
    def save_processed_data(self, data, filename):
        """
        Save processed data with custom filename
        
        Args:
            data (pd.DataFrame): Data to save
            filename (str): Output filename
        
        Returns:
            bool: Success status
        """
        try:
            filepath = self.processed_data_path / filename
            data.to_csv(filepath, index=False)
            logger.info(f"✓ Saved {len(data)} records to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")
            return False
    
    def get_all_medicines(self):
        """Get all medicines from cache or database"""
        try:
            df = self.load_medicine_data(use_cache=True)
            if df.empty:
                logger.warning("No medicines found")
                return []
            
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error retrieving medicines: {str(e)}")
            return []
    
    def get_medicine_by_id(self, medicine_id):
        """
        Get specific medicine by ID
        
        Args:
            medicine_id: ID of medicine to retrieve
        
        Returns:
            dict: Medicine data
        """
        try:
            df = self.load_medicine_data(use_cache=True)
            if df.empty:
                return None
            
            medicine = df[df['medicine_id'] == medicine_id]
            if medicine.empty:
                logger.warning(f"Medicine {medicine_id} not found")
                return None
            
            return medicine.iloc[0].to_dict()
        except Exception as e:
            logger.error(f"Error retrieving medicine {medicine_id}: {str(e)}")
            return None
    
    def update_stock_levels(self, updates):
        """
        Update stock levels for medicines
        
        Args:
            updates (dict): Dictionary of {medicine_id: new_stock}
        
        Returns:
            bool: Success status
        """
        try:
            df = self.load_medicine_data(use_cache=True)
            if df.empty:
                logger.warning("No medicines to update")
                return False
            
            for medicine_id, new_stock in updates.items():
                mask = df['medicine_id'] == medicine_id
                if mask.any():
                    df.loc[mask, 'current_stock'] = new_stock
            
            self.save_medicine_data(df)
            logger.info(f"✓ Updated {len(updates)} medicine stock levels")
            return True
        except Exception as e:
            logger.error(f"Error updating stock levels: {str(e)}")
            return False
    
    def save_json_data(self, data, filename):
        """
        Save data as JSON file
        
        Args:
            data (dict or list): Data to save
            filename (str): Output filename
        
        Returns:
            bool: Success status
        """
        try:
            filepath = self.processed_data_path / filename
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"✓ Saved JSON data to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON data: {str(e)}")
            return False
    
    def load_json_data(self, filename):
        """
        Load data from JSON file
        
        Args:
            filename (str): Input filename
        
        Returns:
            dict or list: Loaded data
        """
        try:
            filepath = self.processed_data_path / filename
            if not filepath.exists():
                logger.warning(f"File not found: {filepath}")
                return None
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            logger.info(f"✓ Loaded JSON data from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON data: {str(e)}")
            return None
    
    def get_data_summary(self):
        """
        Get summary statistics about stored data
        
        Returns:
            dict: Summary information
        """
        try:
            df = self.load_medicine_data(use_cache=True)
            if df.empty:
                return {"total_medicines": 0}
            
            summary = {
                "total_medicines": len(df),
                "total_inventory_value": df['current_stock'].sum() * df['unit_price'].mean(),
                "average_stock": df['current_stock'].mean(),
                "categories": df['category'].nunique(),
                "suppliers": df['supplier_id'].nunique(),
                "last_updated": datetime.now().isoformat()
            }
            return summary
        except Exception as e:
            logger.error(f"Error generating data summary: {str(e)}")
            return {}


def get_database_service():
    """Get singleton instance of database service"""
    return DatabaseService()
