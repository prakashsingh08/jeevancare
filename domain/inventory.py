"""
Inventory Management Logic Module
Core inventory business logic and calculations
"""

import pandas as pd
from datetime import datetime, timedelta
from core.logger import get_logger
from core.constants import *

logger = get_logger(__name__)


class InventoryManagement:
    """Inventory management and optimization"""
    
    @staticmethod
    def calculate_reorder_point(avg_daily_usage, lead_time_days, safety_stock=None):
        """
        Calculate reorder point for a medicine
        
        Args:
            avg_daily_usage (float): Average daily consumption
            lead_time_days (int): Supplier lead time in days
            safety_stock (float): Optional safety stock
        
        Returns:
            float: Reorder point
        """
        try:
            if safety_stock is None:
                safety_stock = avg_daily_usage * 0.2
            
            reorder_point = (avg_daily_usage * lead_time_days) + safety_stock
            logger.debug(f"Calculated reorder point: {reorder_point}")
            return reorder_point
        except Exception as e:
            logger.error(f"Error calculating reorder point: {str(e)}")
            return 0
    
    @staticmethod
    def calculate_reorder_quantity(avg_daily_usage, max_stock, current_stock, lead_time_days):
        """
        Calculate optimal reorder quantity
        
        Args:
            avg_daily_usage (float): Average daily usage
            max_stock (float): Maximum stock level
            current_stock (float): Current stock level
            lead_time_days (int): Lead time
        
        Returns:
            float: Recommended order quantity
        """
        try:
            # Economic Order Quantity approximation
            # EOQ = Max stock - (Average daily usage * Lead time)
            quantity = max_stock - (avg_daily_usage * lead_time_days) - current_stock
            quantity = max(0, quantity)  # Ensure non-negative
            
            logger.debug(f"Calculated reorder quantity: {quantity}")
            return quantity
        except Exception as e:
            logger.error(f"Error calculating reorder quantity: {str(e)}")
            return 0
    
    @staticmethod
    def check_stock_status(current_stock, min_stock, max_stock):
        """
        Check and categorize stock status
        
        Args:
            current_stock (float): Current stock level
            min_stock (float): Minimum stock level
            max_stock (float): Maximum stock level
        
        Returns:
            str: Stock status
        """
        try:
            if current_stock == 0:
                return STOCK_STATUS_OUT
            elif current_stock <= min_stock:
                return STOCK_STATUS_CRITICAL
            elif current_stock < min_stock * 2:
                return STOCK_STATUS_LOW
            elif current_stock >= max_stock:
                return STOCK_STATUS_HIGH
            else:
                return STOCK_STATUS_NORMAL
        except Exception as e:
            logger.error(f"Error checking stock status: {str(e)}")
            return STOCK_STATUS_NORMAL
    
    @staticmethod
    def calculate_inventory_turnover(cost_of_goods_sold, average_inventory):
        """
        Calculate inventory turnover ratio
        
        Args:
            cost_of_goods_sold (float): Total COGS
            average_inventory (float): Average inventory value
        
        Returns:
            float: Turnover ratio
        """
        try:
            if average_inventory == 0:
                return 0
            
            turnover = cost_of_goods_sold / average_inventory
            logger.debug(f"Calculated inventory turnover: {turnover}")
            return turnover
        except Exception as e:
            logger.error(f"Error calculating inventory turnover: {str(e)}")
            return 0
    
    @staticmethod
    def calculate_days_of_stock(current_stock, avg_daily_usage):
        """
        Calculate days of stock remaining
        
        Args:
            current_stock (float): Current stock quantity
            avg_daily_usage (float): Average daily usage
        
        Returns:
            float: Days of stock remaining
        """
        try:
            if avg_daily_usage == 0:
                return 0
            
            days = current_stock / avg_daily_usage
            logger.debug(f"Calculated days of stock: {days}")
            return days
        except Exception as e:
            logger.error(f"Error calculating days of stock: {str(e)}")
            return 0
    
    @staticmethod
    def identify_overstock_items(df, threshold=0.9):
        """
        Identify overstocked items
        
        Args:
            df (pd.DataFrame): Medicine data
            threshold (float): Overstock threshold ratio
        
        Returns:
            pd.DataFrame: Overstocked items
        """
        try:
            overstock = df[df['current_stock'] >= df['max_stock'] * threshold]
            logger.info(f"✓ Identified {len(overstock)} overstock items")
            return overstock
        except Exception as e:
            logger.error(f"Error identifying overstock items: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def identify_understock_items(df, threshold=0.2):
        """
        Identify understocked items
        
        Args:
            df (pd.DataFrame): Medicine data
            threshold (float): Understock threshold ratio
        
        Returns:
            pd.DataFrame: Understocked items
        """
        try:
            understock = df[df['current_stock'] <= df['min_stock'] * threshold]
            logger.info(f"✓ Identified {len(understock)} understock items")
            return understock
        except Exception as e:
            logger.error(f"Error identifying understock items: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def calculate_total_inventory_value(df):
        """
        Calculate total inventory value
        
        Args:
            df (pd.DataFrame): Medicine data with current_stock and unit_price
        
        Returns:
            float: Total inventory value
        """
        try:
            if df.empty:
                return 0
            
            total_value = (df['current_stock'] * df['unit_price']).sum()
            logger.info(f"✓ Total inventory value: ${total_value:.2f}")
            return total_value
        except Exception as e:
            logger.error(f"Error calculating inventory value: {str(e)}")
            return 0
    
    @staticmethod
    def identify_expiry_risk_items(df, days_threshold=None):
        try:
            if days_threshold is None:
                from core.constants import EXPIRY_DAYS_WARNING
                days_threshold = EXPIRY_DAYS_WARNING

            expiry_risk = df[df['days_to_expiry'] <= days_threshold]
            logger.info(f"✓ Identified {len(expiry_risk)} items at expiry risk")
            return expiry_risk

        except Exception as e:
            logger.error(f"Error identifying expiry risk items: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def get_low_stock_alerts(df, critical_threshold=None):
        """
        Get items with low stock requiring alerts
        
        Args:
            df (pd.DataFrame): Medicine data
            critical_threshold (int): Critical stock threshold
        
        Returns:
            pd.DataFrame: Items requiring attention
        """
        try:
            if critical_threshold is None:
                critical_threshold = CRITICAL_STOCK_THRESHOLD
            
            low_stock = df[df['current_stock'] <= critical_threshold]
            logger.info(f"✓ Found {len(low_stock)} items with low stock")
            return low_stock
        except Exception as e:
            logger.error(f"Error getting low stock alerts: {str(e)}")
            return pd.DataFrame()


def calculate_reorder_point(avg_daily_usage, lead_time_days):
    """Convenience function"""
    return InventoryManagement.calculate_reorder_point(avg_daily_usage, lead_time_days)
