"""
Firebase Service Module
Handles all Firebase Realtime Database operations
"""

import firebase_admin
from firebase_admin import credentials, db
from pathlib import Path
from core.logger import get_logger
from core.config import Config
from core.constants import *
import json

logger = get_logger(__name__)


class FirebaseService:
    """Firebase database operations and management"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern - ensure only one Firebase connection"""
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Firebase connection"""
        try:
            # Check if Firebase app is already initialized
            try:
                firebase_admin.get_app()
                logger.info("Firebase app already initialized")
            except ValueError:
                # Firebase app not initialized, initialize it
                cred_path = Path(Config.FIREBASE_KEY_PATH)
                if not cred_path.exists():
                    raise FileNotFoundError(f"Firebase credentials not found at {Config.FIREBASE_KEY_PATH}")
                
                cred = credentials.Certificate(str(cred_path))
                firebase_admin.initialize_app(cred, {
                    'databaseURL': Config.FIREBASE_DATABASE_URL
                })
                logger.info("✓ Firebase initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise

    def get_data(self, path):
        """
        Retrieve data from Firebase at specified path
        
        Args:
            path (str): Database path (e.g., 'medicines/medicine_1')
        
        Returns:
            dict or list: Retrieved data
        """
        try:
            ref = db.reference(path)
            data = ref.get()
            logger.debug(f"Retrieved data from {path}")
            return data
        except Exception as e:
            logger.error(f"Error retrieving data from {path}: {str(e)}")
            return None

    def write_data(self, path, data):
        """
        Write data to Firebase at specified path
        
        Args:
            path (str): Database path
            data (dict or list): Data to write
        
        Returns:
            bool: Success status
        """
        try:
            ref = db.reference(path)
            ref.set(data)
            logger.info(f"✓ Data written to {path}")
            return True
        except Exception as e:
            logger.error(f"Error writing data to {path}: {str(e)}")
            return False

    def update_data(self, path, data):
        """
        Update existing data at specified path
        
        Args:
            path (str): Database path
            data (dict): Data to update
        
        Returns:
            bool: Success status
        """
        try:
            ref = db.reference(path)
            ref.update(data)
            logger.info(f"✓ Data updated at {path}")
            return True
        except Exception as e:
            logger.error(f"Error updating data at {path}: {str(e)}")
            return False

    def delete_data(self, path):
        """
        Delete data at specified path
        
        Args:
            path (str): Database path
        
        Returns:
            bool: Success status
        """
        try:
            ref = db.reference(path)
            ref.delete()
            logger.info(f"✓ Data deleted from {path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting data from {path}: {str(e)}")
            return False

    def batch_write(self, updates):
        """
        Write multiple updates at once
        
        Args:
            updates (dict): Dictionary of {path: data} pairs
        
        Returns:
            bool: Success status
        """
        try:
            ref = db.reference()
            ref.update(updates)
            logger.info(f"✓ Batch write completed ({len(updates)} updates)")
            return True
        except Exception as e:
            logger.error(f"Error in batch write: {str(e)}")
            return False

    def listen_to_changes(self, path, callback):
        """
        Listen for real-time changes at specified path
        
        Args:
            path (str): Database path to monitor
            callback (function): Callback function when data changes
        """
        try:
            ref = db.reference(path)
            ref.listen(callback)
            logger.info(f"✓ Listener attached to {path}")
        except Exception as e:
            logger.error(f"Error attaching listener to {path}: {str(e)}")

    def get_all_medicines(self):
        """Get all medicines from database"""
        try:
            data = self.get_data(FIREBASE_MEDICINES_PATH)
            if data is None:
                logger.warning("No medicines found in database")
                return {}
            return data
        except Exception as e:
            logger.error(f"Error retrieving medicines: {str(e)}")
            return {}

    def get_medicine(self, medicine_id):
        """Get specific medicine by ID"""
        try:
            path = f"{FIREBASE_MEDICINES_PATH}/{medicine_id}"
            return self.get_data(path)
        except Exception as e:
            logger.error(f"Error retrieving medicine {medicine_id}: {str(e)}")
            return None

    def save_medicine(self, medicine_id, medicine_data):
        """Save or update medicine data"""
        try:
            path = f"{FIREBASE_MEDICINES_PATH}/{medicine_id}"
            return self.write_data(path, medicine_data)
        except Exception as e:
            logger.error(f"Error saving medicine {medicine_id}: {str(e)}")
            return False

    def get_alerts(self):
        """Get all active alerts"""
        try:
            return self.get_data(FIREBASE_ALERTS_PATH) or {}
        except Exception as e:
            logger.error(f"Error retrieving alerts: {str(e)}")
            return {}

    def save_alert(self, alert_id, alert_data):
        """Save new alert"""
        try:
            path = f"{FIREBASE_ALERTS_PATH}/{alert_id}"
            return self.write_data(path, alert_data)
        except Exception as e:
            logger.error(f"Error saving alert: {str(e)}")
            return False

    def get_forecasts(self):
        """Get all forecasts"""
        try:
            return self.get_data(FIREBASE_FORECASTS_PATH) or {}
        except Exception as e:
            logger.error(f"Error retrieving forecasts: {str(e)}")
            return {}

    def save_forecast(self, medicine_id, forecast_data):
        """Save forecast for medicine"""
        try:
            path = f"{FIREBASE_FORECASTS_PATH}/{medicine_id}"
            return self.write_data(path, forecast_data)
        except Exception as e:
            logger.error(f"Error saving forecast: {str(e)}")
            return False

    # def check_connection(self):
    #     """Check if Firebase connection is active"""
    #     try:
    #         ref = db.reference('.info/connected')
    #         connected = ref.get()
    #         if connected:
    #             logger.info("✓ Firebase connection is active")
    #         else:
    #             logger.warning("Firebase connection is inactive")
    #         return connected
    #     except Exception as e:
    #         logger.error(f"Error checking Firebase connection: {str(e)}")
    #         return False

    def check_connection(self):
        """Check if Firebase connection is active"""
        try:
            ref = db.reference('/')   # ✅ ROOT PATH
            data = ref.get()

            logger.info("✓ Firebase connection is active")
            return True

        except Exception as e:
            logger.error(f"Error checking Firebase connection: {str(e)}")
            return False

def get_firebase_service():
    """Get singleton instance of Firebase service"""
    return FirebaseService()
