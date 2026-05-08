"""
Core Configuration Module
Handles all application-wide configuration and environment setup
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application Configuration Class"""

    # ============================================
    # FIREBASE CONFIGURATION
    # ============================================
    FIREBASE_KEY_PATH = os.getenv('FIREBASE_KEY_PATH', 'config/serviceAccountKey.json')
    FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL', 'https://jeevancare-analytics-dev.firebaseio.com')
    FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET', 'jeevancare-analytics-dev.appspot.com')

    # ============================================
    # APPLICATION CONFIGURATION
    # ============================================
    APP_ENV = os.getenv('APP_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    APP_PORT = int(os.getenv('APP_PORT', 8501))
    APP_NAME = 'JeevanCare Analytics Platform'
    APP_VERSION = '1.0.0'

    # ============================================
    # DATA CONFIGURATION
    # ============================================
    DATA_RAW_PATH = os.getenv('DATA_RAW_PATH', 'data/raw/')
    DATA_PROCESSED_PATH = os.getenv('DATA_PROCESSED_PATH', 'data/processed/')
    SAMPLE_DATA_FILE = 'medicine_inventory.csv'

    # ============================================
    # LOGGING CONFIGURATION
    # ============================================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'logs/jeevancare.log')

    # ============================================
    # EMAIL CONFIGURATION (Optional)
    # ============================================
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', 587))
    EMAIL_SENDER_ADDRESS = os.getenv('EMAIL_SENDER_ADDRESS', '')
    EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD', '')
    ALERT_EMAIL_RECIPIENTS = os.getenv('ALERT_EMAIL_RECIPIENTS', '').split(',')

    # ============================================
    # FORECASTING CONFIGURATION
    # ============================================
    FORECAST_PERIODS = int(os.getenv('FORECAST_PERIODS', 30))
    MOVING_AVERAGE_WINDOW = int(os.getenv('MOVING_AVERAGE_WINDOW', 7))
    MIN_STOCK_THRESHOLD_PERCENTAGE = float(os.getenv('MIN_STOCK_THRESHOLD_PERCENTAGE', 0.2))
    MAX_STOCK_THRESHOLD_PERCENTAGE = float(os.getenv('MAX_STOCK_THRESHOLD_PERCENTAGE', 0.9))

    # ============================================
    # ALERT CONFIGURATION
    # ============================================
    ALERT_ENABLED = os.getenv('ALERT_ENABLED', 'True').lower() == 'true'
    CRITICAL_STOCK_THRESHOLD = int(os.getenv('CRITICAL_STOCK_THRESHOLD', 10))
    WARNING_STOCK_THRESHOLD = int(os.getenv('WARNING_STOCK_THRESHOLD', 50))
    EXPIRY_DAYS_WARNING = int(os.getenv('EXPIRY_DAYS_WARNING', 30))

    @staticmethod
    def load_firebase_credentials():
        """Load Firebase service account credentials from JSON file"""
        try:
            credentials_path = Path(Config.FIREBASE_KEY_PATH)
            if not credentials_path.exists():
                raise FileNotFoundError(f"Firebase credentials not found at {Config.FIREBASE_KEY_PATH}")
            
            with open(credentials_path, 'r') as f:
                credentials = json.load(f)
            return credentials
        except Exception as e:
            logging.error(f"Error loading Firebase credentials: {str(e)}")
            raise

    @staticmethod
    def validate_configuration():
        """Validate all required configuration"""
        required_configs = {
            'FIREBASE_DATABASE_URL': Config.FIREBASE_DATABASE_URL,
            'DATA_RAW_PATH': Config.DATA_RAW_PATH,
            'DATA_PROCESSED_PATH': Config.DATA_PROCESSED_PATH,
        }
        
        missing_configs = [key for key, value in required_configs.items() if not value]
        
        if missing_configs:
            raise ValueError(f"Missing required configuration: {', '.join(missing_configs)}")
        
        return True

    @staticmethod
    def create_directories():
        """Create required directories if they don't exist"""
        directories = [
            Config.DATA_RAW_PATH,
            Config.DATA_PROCESSED_PATH,
            'logs',
            'config',
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


def load_config():
    """Load and validate configuration"""
    Config.validate_configuration()
    Config.create_directories()
    return Config


if __name__ == '__main__':
    config = load_config()
    print(f"✓ Configuration loaded successfully")
    print(f"✓ App Environment: {config.APP_ENV}")
    print(f"✓ Debug Mode: {config.DEBUG}")
    print(f"✓ Firebase Database URL: {config.FIREBASE_DATABASE_URL}")
