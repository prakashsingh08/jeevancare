"""
Real-time Data Simulator Script
Simulates real-time inventory updates for testing and demonstration
"""

import sys
import time
import random
from datetime import datetime, timedelta
from core.logger import get_logger
from services.firebase_service import get_firebase_service
from services.database_service import get_database_service
from core.constants import FIREBASE_MEDICINES_PATH
import argparse

logger = get_logger(__name__)


class DataSimulator:
    """Simulates real-time data updates"""
    
    def __init__(self):
        """Initialize simulator"""
        self.firebase = get_firebase_service()
        self.db = get_database_service()
        self.update_count = 0
        logger.info("✓ Data simulator initialized")
    
    def generate_random_update(self):
        """
        Generate random medicine data update
        
        Returns:
            dict: Updated medicine data
        """
        try:
            # Get all medicines
            medicines = self.db.get_all_medicines()
            
            if not medicines:
                logger.warning("No medicines to simulate")
                return None
            
            # Select random medicine
            medicine = random.choice(medicines)
            medicine_id = medicine.get('medicine_id')
            
            # Generate random stock change (-5 to +10)
            stock_change = random.randint(-5, 10)
            new_stock = max(0, medicine.get('current_stock', 0) + stock_change)
            
            # Update medicine data
            updated_medicine = medicine.copy()
            updated_medicine['current_stock'] = new_stock
            updated_medicine['updated_at'] = datetime.now().isoformat()
            updated_medicine['change'] = stock_change
            
            return medicine_id, updated_medicine
        
        except Exception as e:
            logger.error(f"Error generating update: {str(e)}")
            return None
    
    def simulate_update(self):
        """Simulate a single data update"""
        try:
            result = self.generate_random_update()
            
            if result is None:
                return False
            
            medicine_id, updated_data = result
            
            # Update in Firebase
            path = f"{FIREBASE_MEDICINES_PATH}/medicine_{medicine_id}"
            self.firebase.update_data(path, updated_data)
            
            # Update local database
            updates = {medicine_id: updated_data['current_stock']}
            self.db.update_stock_levels(updates)
            
            self.update_count += 1
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"Update #{self.update_count}: {timestamp} - Updated medicine_id={medicine_id}, "
                       f"new_stock={updated_data['current_stock']}, change={updated_data['change']}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error simulating update: {str(e)}")
            return False
    
    def run_simulation(self, iterations=None, interval=10):
        """
        Run data simulation
        
        Args:
            iterations (int): Number of updates to simulate (None for infinite)
            interval (int): Interval between updates in seconds
        """
        try:
            logger.info("=" * 60)
            logger.info("STARTING REAL-TIME DATA SIMULATOR")
            logger.info("=" * 60)
            logger.info(f"Interval: {interval} seconds")
            
            if iterations:
                logger.info(f"Iterations: {iterations}")
            else:
                logger.info("Iterations: Infinite (press Ctrl+C to stop)")
            
            logger.info("=" * 60)
            
            count = 0
            while True:
                # Simulate update
                self.simulate_update()
                
                count += 1
                if iterations and count >= iterations:
                    logger.info(f"Simulation completed: {count} updates")
                    break
                
                # Wait before next update
                time.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("\n✓ Simulation stopped by user")
            logger.info(f"Total updates simulated: {self.update_count}")
        
        except Exception as e:
            logger.error(f"Simulation failed: {str(e)}")
        
        finally:
            logger.info("=" * 60)


def main():
    """Main simulator function"""
    parser = argparse.ArgumentParser(description='Simulate real-time inventory updates')
    parser.add_argument('--iterations', type=int, default=None,
                       help='Number of updates to simulate (default: infinite)')
    parser.add_argument('--interval', type=int, default=10,
                       help='Interval between updates in seconds (default: 10)')
    
    args = parser.parse_args()
    
    try:
        logger.info("Initializing simulator...")
        
        # Initialize simulator
        simulator = DataSimulator()
        
        # Check Firebase connection
        if not simulator.firebase.check_connection():
            logger.error("Firebase connection failed")
            return False
        
        # Run simulation
        simulator.run_simulation(iterations=args.iterations, interval=args.interval)
        
        return True
    
    except Exception as e:
        logger.error(f"Simulator failed: {str(e)}")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
