"""
Update Pipeline Module
Handles real-time data updates and synchronization
"""

import time
from datetime import datetime
from core.logger import get_logger
from services.firebase_service import get_firebase_service
from core.constants import *
import threading

logger = get_logger(__name__)


class UpdatePipeline:
    """Real-time data update and synchronization pipeline"""
    
    def __init__(self):
        """Initialize update pipeline"""
        self.firebase = get_firebase_service()
        self.is_running = False
        self.update_count = 0
        logger.info("✓ Update pipeline initialized")
    
    def handle_data_update(self, updated_data):
        """
        Process incoming data updates
        
        Args:
            updated_data (dict): Updated medicine or alert data
        """
        try:
            self.update_count += 1
            timestamp = datetime.now().isoformat()
            logger.info(f"Update #{self.update_count}: {timestamp} - Processing update")
            
            if updated_data is None:
                logger.warning("Received null update")
                return
            
            # Log the update
            logger.debug(f"Updated data: {updated_data}")
        except Exception as e:
            logger.error(f"Error handling data update: {str(e)}")
    
    def sync_with_firebase(self):
        """Synchronize local data with Firebase"""
        try:
            logger.info("✓ Syncing with Firebase...")
            medicines = self.firebase.get_all_medicines()
            logger.info(f"✓ Synced {len(medicines) if medicines else 0} medicines from Firebase")
            return medicines
        except Exception as e:
            logger.error(f"Error syncing with Firebase: {str(e)}")
            return {}
    
    def trigger_alerts(self, medicine_data):
        """
        Generate alerts based on data changes
        
        Args:
            medicine_data (dict): Medicine data to check
        """
        try:
            if medicine_data is None:
                return
            
            alerts = []
            
            # Check stock level alerts
            if medicine_data.get('current_stock', 0) <= CRITICAL_STOCK_THRESHOLD:
                alerts.append({
                    'type': 'LOW_STOCK',
                    'severity': ALERT_SEVERITY_CRITICAL,
                    'message': f"Critical: {medicine_data.get('name')} stock at {medicine_data.get('current_stock')}"
                })
            
            # Check expiry alerts
            days_to_expiry = medicine_data.get('days_to_expiry', 999)
            if days_to_expiry <= EXPIRY_DAYS_WARNING and days_to_expiry >= 0:
                alerts.append({
                    'type': 'EXPIRY_WARNING',
                    'severity': ALERT_SEVERITY_WARNING,
                    'message': f"Warning: {medicine_data.get('name')} expires in {days_to_expiry} days"
                })
            
            # Log alerts
            for alert in alerts:
                logger.warning(f"ALERT [{alert['severity']}]: {alert['message']}")
            
            return alerts
        except Exception as e:
            logger.error(f"Error triggering alerts: {str(e)}")
            return []
    
    def start_real_time_listener(self):
        """Start listening for real-time changes"""
        try:
            logger.info("Starting real-time data listener...")
            
            def callback(message):
                if message.event == 'put':
                    self.handle_data_update(message.data)
                elif message.event == 'patch':
                    self.handle_data_update(message.data)
            
            # Listen to medicines path
            self.firebase.listen_to_changes(FIREBASE_MEDICINES_PATH, callback)
            self.is_running = True
            logger.info("✓ Real-time listener started")
        except Exception as e:
            logger.error(f"Error starting real-time listener: {str(e)}")
    
    def run_update_cycle(self, interval=10):
        """
        Run periodic update cycle
        
        Args:
            interval (int): Update interval in seconds
        """
        try:
            logger.info(f"Starting update cycle (interval: {interval}s)")
            self.is_running = True
            
            while self.is_running:
                try:
                    # Sync with Firebase
                    medicines = self.sync_with_firebase()
                    
                    # Process each medicine
                    if medicines:
                        for medicine_id, medicine_data in medicines.items():
                            # Check and trigger alerts
                            self.trigger_alerts(medicine_data)
                    
                    # Wait before next update
                    time.sleep(interval)
                except KeyboardInterrupt:
                    logger.info("Update cycle interrupted by user")
                    break
                except Exception as e:
                    logger.error(f"Error in update cycle: {str(e)}")
                    time.sleep(interval)
        except Exception as e:
            logger.error(f"Update cycle failed: {str(e)}")
        finally:
            self.is_running = False
            logger.info("Update cycle stopped")
    
    def stop_updates(self):
        """Stop the update pipeline"""
        self.is_running = False
        logger.info("Update pipeline stopped")


def start_update_pipeline(interval=10):
    """Start the update pipeline"""
    pipeline = UpdatePipeline()
    pipeline.run_update_cycle(interval)
