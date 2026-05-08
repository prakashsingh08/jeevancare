"""
KPI Cards Component Module
Key Performance Indicator display components
"""

from core.logger import get_logger

logger = get_logger(__name__)


class KPICards:
    """KPI card components for dashboard"""
    
    @staticmethod
    def create_kpi_card_data(title, value, change=None, trend=None):
        """
        Create KPI card data structure
        
        Args:
            title (str): KPI title
            value (str or float): KPI value
            change (float): Change percentage
            trend (str): 'up', 'down', or 'stable'
        
        Returns:
            dict: KPI card data
        """
        try:
            card = {
                'title': title,
                'value': str(value),
                'change': change,
                'trend': trend or 'stable',
                'color': 'green' if trend == 'up' else 'red' if trend == 'down' else 'gray'
            }
            logger.debug(f"Created KPI card: {title}")
            return card
        except Exception as e:
            logger.error(f"Error creating KPI card: {str(e)}")
            return None
    
    @staticmethod
    def create_metric_card(label, value, unit='', color='blue'):
        """
        Create metric card
        
        Args:
            label (str): Metric label
            value (float): Metric value
            unit (str): Unit of measurement
            color (str): Card color
        
        Returns:
            dict: Metric card data
        """
        try:
            card = {
                'label': label,
                'value': value,
                'unit': unit,
                'color': color,
                'display': f"{value} {unit}"
            }
            return card
        except Exception as e:
            logger.error(f"Error creating metric card: {str(e)}")
            return None
    
    @staticmethod
    def create_status_card(title, status, message=''):
        """
        Create status card
        
        Args:
            title (str): Card title
            status (str): Status ('OK', 'WARNING', 'CRITICAL')
            message (str): Status message
        
        Returns:
            dict: Status card data
        """
        try:
            color_map = {
                'OK': 'green',
                'WARNING': 'orange',
                'CRITICAL': 'red',
                'INFO': 'blue'
            }
            
            card = {
                'title': title,
                'status': status,
                'message': message,
                'color': color_map.get(status, 'gray')
            }
            return card
        except Exception as e:
            logger.error(f"Error creating status card: {str(e)}")
            return None


# Example KPIs that can be displayed
INVENTORY_KPIS = {
    'total_medicines': 'Total Medicines',
    'total_value': 'Total Inventory Value',
    'average_stock': 'Average Stock Level',
    'low_stock_items': 'Low Stock Items',
    'overstock_items': 'Overstock Items',
    'critical_items': 'Critical Items',
    'expiry_risk_items': 'Items at Expiry Risk',
    'stock_utilization': 'Stock Utilization Rate'
}
