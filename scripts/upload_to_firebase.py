"""
Firebase Data Upload Script
Uploads processed data to Firebase Realtime Database
"""

import sys
import time
from pathlib import Path
from core.logger import get_logger
from core.config import Config
from services.firebase_service import get_firebase_service
from services.database_service import get_database_service
from core.constants import FIREBASE_MEDICINES_PATH
import argparse

logger = get_logger(__name__)


def upload_medicines_to_firebase(db_service, firebase_service):
    """
    Upload medicines data to Firebase
    
    Args:
        db_service: Database service instance
        firebase_service: Firebase service instance
    
    Returns:
        bool: Success status
    """
    try:
        logger.info("=" * 60)
        logger.info("UPLOADING MEDICINES TO FIREBASE")
        logger.info("=" * 60)
        
        # Load medicine data from local database
        medicines = db_service.get_all_medicines()
        
        if not medicines:
            logger.warning("No medicines found to upload")
            return False
        
        logger.info(f"Found {len(medicines)} medicines to upload")
        
        # Prepare data for Firebase
        firebase_data = {}
        for i, medicine in enumerate(medicines):
            if 'medicine_id' in medicine:
                medicine_id = f"medicine_{medicine['medicine_id']}"
                firebase_data[medicine_id] = medicine
                
                # Show progress
                progress = int((i + 1) / len(medicines) * 100)
                if progress % 25 == 0:
                    logger.info(f"Upload progress: {progress}%")
        
        # Batch write to Firebase
        upload_data = {f"{FIREBASE_MEDICINES_PATH}/{key}": value for key, value in firebase_data.items()}
        
        success = firebase_service.batch_write(upload_data)
        
        if success:
            logger.info("=" * 60)
            logger.info(f"✓ Successfully uploaded {len(medicines)} medicines to Firebase")
            logger.info("=" * 60)
            return True
        else:
            logger.error("Failed to upload medicines to Firebase")
            return False
    
    except Exception as e:
        logger.error(f"Error uploading medicines: {str(e)}")
        return False


def main():
    """Main upload function"""
    parser = argparse.ArgumentParser(description='Upload processed data to Firebase')
    parser.add_argument('--file', type=str, help='Specific file to upload')
    parser.add_argument('--force', action='store_true', help='Force re-upload')
    
    args = parser.parse_args()
    
    try:
        logger.info("Initializing services...")
        
        # Initialize services
        db_service = get_database_service()
        firebase_service = get_firebase_service()
        
        # Check Firebase connection
        if not firebase_service.check_connection():
            logger.error("Firebase connection failed")
            return False
        
        # Upload medicines data
        success = upload_medicines_to_firebase(db_service, firebase_service)
        
        if success:
            logger.info("✓ Upload completed successfully")
            return True
        else:
            logger.error("✗ Upload failed")
            return False
    
    except Exception as e:
        logger.error(f"Upload script failed: {str(e)}")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
