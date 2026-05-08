"""
Alerts Module
Alert generation and management
"""

import pandas as pd
from datetime import datetime
from core.logger import get_logger
from core.constants import *

logger = get_logger(__name__)


class AlertSystem:
    """Alert generation and management system"""
    
    def __init__(self):
        """Initialize alert system"""
        self.alerts = []
        logger.info("✓ Alert system initialized")
    
    def create_alert(self, alert_type, severity, medicine_id, message):
        """
        Create an alert
        
        Args:
            alert_type (str): Type of alert (LOW_STOCK, EXPIRY, etc.)
            severity (str): Severity level (CRITICAL, WARNING, INFO)
            medicine_id: ID of affected medicine
            message (str): Alert message
        
        Returns:
            dict: Alert object
        """
        try:
            alert = {
                'id': f"{alert_type}_{medicine_id}_{datetime.now().timestamp()}",
                'type': alert_type,
                'severity': severity,
                'medicine_id': medicine_id,
                'message': message,
                'created_at': datetime.now().isoformat(),
                'resolved': False
            }
            
            self.alerts.append(alert)
            logger.warning(f"[{severity}] {alert_type}: {message}")
            
            return alert
        except Exception as e:
            logger.error(f"Error creating alert: {str(e)}")
            return None
    
    def check_low_stock_alerts(self, df):
        """
        Check for low stock alerts
        
        Args:
            df (pd.DataFrame): Medicine data
        
        Returns:
            list: Generated alerts
        """
        try:
            alerts_generated = []
            
            for _, row in df.iterrows():
                current_stock = row['current_stock']
                min_stock = row['min_stock']
                medicine_name = row['name']
                medicine_id = row['medicine_id']
                
                if current_stock == 0:
                    alert = self.create_alert(
                        'STOCKOUT',
                        ALERT_SEVERITY_CRITICAL,
                        medicine_id,
                        f"{medicine_name}: OUT OF STOCK!"
                    )
                    alerts_generated.append(alert)
                
                elif current_stock <= min_stock:
                    alert = self.create_alert(
                        'LOW_STOCK',
                        ALERT_SEVERITY_WARNING,
                        medicine_id,
                        f"{medicine_name}: Stock at {current_stock} (min: {min_stock})"
                    )
                    alerts_generated.append(alert)
            
            logger.info(f"✓ Generated {len(alerts_generated)} low stock alerts")
            return alerts_generated
        except Exception as e:
            logger.error(f"Error checking low stock: {str(e)}")
            return []
    
    def check_expiry_alerts(self, df):
        """
        Check for expiry alerts
        
        Args:
            df (pd.DataFrame): Medicine data
        
        Returns:
            list: Generated alerts
        """
        try:
            alerts_generated = []
            
            for _, row in df.iterrows():
                days_to_expiry = row['days_to_expiry']
                medicine_name = row['name']
                medicine_id = row['medicine_id']
                
                if 0 <= days_to_expiry <= 7:
                    alert = self.create_alert(
                        'EXPIRY_CRITICAL',
                        ALERT_SEVERITY_CRITICAL,
                        medicine_id,
                        f"{medicine_name}: Expires in {days_to_expiry} days!"
                    )
                    alerts_generated.append(alert)
                
                elif 8 <= days_to_expiry <= 30:
                    alert = self.create_alert(
                        'EXPIRY_WARNING',
                        ALERT_SEVERITY_WARNING,
                        medicine_id,
                        f"{medicine_name}: Expires in {days_to_expiry} days"
                    )
                    alerts_generated.append(alert)
                
                elif days_to_expiry < 0:
                    alert = self.create_alert(
                        'EXPIRED',
                        ALERT_SEVERITY_CRITICAL,
                        medicine_id,
                        f"{medicine_name}: EXPIRED!"
                    )
                    alerts_generated.append(alert)
            
            logger.info(f"✓ Generated {len(alerts_generated)} expiry alerts")
            return alerts_generated
        except Exception as e:
            logger.error(f"Error checking expiry: {str(e)}")
            return []
    
    def check_overstock_alerts(self, df):
        """
        Check for overstock situations
        
        Args:
            df (pd.DataFrame): Medicine data
        
        Returns:
            list: Generated alerts
        """
        try:
            alerts_generated = []
            
            for _, row in df.iterrows():
                current_stock = row['current_stock']
                max_stock = row['max_stock']
                medicine_name = row['name']
                medicine_id = row['medicine_id']
                
                if current_stock >= max_stock * 0.95:
                    alert = self.create_alert(
                        'OVERSTOCK',
                        ALERT_SEVERITY_INFO,
                        medicine_id,
                        f"{medicine_name}: Overstock detected ({current_stock}>{max_stock})"
                    )
                    alerts_generated.append(alert)
            
            logger.info(f"✓ Generated {len(alerts_generated)} overstock alerts")
            return alerts_generated
        except Exception as e:
            logger.error(f"Error checking overstock: {str(e)}")
            return []
    
    def generate_alerts(self, df):
        """
        Main alert generation function
        
        Args:
            df (pd.DataFrame): Medicine data
        
        Returns:
            list: All generated alerts
        """
        try:
            logger.info("=" * 60)
            logger.info("GENERATING ALERTS")
            logger.info("=" * 60)
            
            all_alerts = []
            
            # Generate different types of alerts
            all_alerts.extend(self.check_low_stock_alerts(df))
            all_alerts.extend(self.check_expiry_alerts(df))
            all_alerts.extend(self.check_overstock_alerts(df))
            
            logger.info(f"✓ Total alerts generated: {len(all_alerts)}")
            logger.info("=" * 60)
            
            return all_alerts
        except Exception as e:
            logger.error(f"Alert generation failed: {str(e)}")
            return []
    
    def get_critical_alerts(self):
        """Get all critical alerts"""
        return [a for a in self.alerts if a['severity'] == ALERT_SEVERITY_CRITICAL]
    
    def get_warning_alerts(self):
        """Get all warning alerts"""
        return [a for a in self.alerts if a['severity'] == ALERT_SEVERITY_WARNING]
    
    def resolve_alert(self, alert_id):
        """Mark alert as resolved"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['resolved'] = True
                logger.info(f"✓ Alert {alert_id} resolved")
                return True
        return False


def generate_alerts(df):
    """Convenience function"""
    system = AlertSystem()
    return system.generate_alerts(df)
