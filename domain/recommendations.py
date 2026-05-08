"""
Recommendations Module
Recommendation engine for inventory optimization
"""

import pandas as pd
from core.logger import get_logger
from core.constants import *

logger = get_logger(__name__)


class RecommendationEngine:
    """Generate recommendations for inventory management"""
    
    @staticmethod
    def get_purchase_recommendations(df, forecast_data=None):
        """
        Get purchase recommendations
        
        Args:
            df (pd.DataFrame): Medicine data
            forecast_data (dict): Optional forecast data
        
        Returns:
            list: Purchase recommendations
        """
        try:
            recommendations = []
            
            for _, row in df.iterrows():
                if row['stock_status'] == STOCK_STATUS_CRITICAL or row['stock_status'] == STOCK_STATUS_LOW:
                    # Calculate recommended quantity
                    reorder_qty = row['max_stock'] - row['current_stock']
                    
                    recommendation = {
                        'medicine_id': row['medicine_id'],
                        'medicine_name': row['name'],
                        'current_stock': row['current_stock'],
                        'recommended_quantity': reorder_qty,
                        'estimated_cost': reorder_qty * row['unit_price'],
                        'priority': 'HIGH' if row['stock_status'] == STOCK_STATUS_CRITICAL else 'MEDIUM',
                        'reason': f"Stock at {row['current_stock']}, reorder to {row['max_stock']}"
                    }
                    
                    recommendations.append(recommendation)
            
            logger.info(f"✓ Generated {len(recommendations)} purchase recommendations")
            return recommendations
        except Exception as e:
            logger.error(f"Error getting purchase recommendations: {str(e)}")
            return []
    
    @staticmethod
    def get_supplier_recommendations(df):
        """
        Get supplier recommendations
        
        Args:
            df (pd.DataFrame): Medicine data with supplier info
        
        Returns:
            list: Supplier recommendations
        """
        try:
            recommendations = []
            
            if 'supplier_id' not in df.columns:
                logger.warning("No supplier information available")
                return recommendations
            
            # Group by supplier and get performance metrics
            supplier_stats = df.groupby('supplier_id').agg({
                'medicine_id': 'count',
                'inventory_value': 'sum',
                'unit_price': 'mean'
            }).rename(columns={'medicine_id': 'medicines_count'})
            
            for supplier_id, stats in supplier_stats.iterrows():
                recommendation = {
                    'supplier_id': supplier_id,
                    'medicines_count': int(stats['medicines_count']),
                    'total_value': stats['inventory_value'],
                    'avg_price': stats['unit_price'],
                    'recommendation': 'OPTIMIZE' if stats['medicines_count'] > 10 else 'MONITOR'
                }
                
                recommendations.append(recommendation)
            
            logger.info(f"✓ Generated supplier recommendations for {len(recommendations)} suppliers")
            return recommendations
        except Exception as e:
            logger.error(f"Error getting supplier recommendations: {str(e)}")
            return []
    
    @staticmethod
    def get_cost_optimization_suggestions(df):
        """
        Get cost optimization suggestions
        
        Args:
            df (pd.DataFrame): Medicine data
        
        Returns:
            list: Cost optimization suggestions
        """
        try:
            suggestions = []
            
            # High cost low usage items
            high_cost_low_usage = df[
                (df['unit_price'] > df['unit_price'].quantile(0.75)) &
                (df['current_stock'] < df['current_stock'].quantile(0.25))
            ]
            
            for _, row in high_cost_low_usage.iterrows():
                suggestion = {
                    'medicine_id': row['medicine_id'],
                    'medicine_name': row['name'],
                    'type': 'HIGH_COST_LOW_USAGE',
                    'current_stock': row['current_stock'],
                    'unit_price': row['unit_price'],
                    'suggestion': f"Consider reducing stock for {row['name']} - high cost ({row['unit_price']}) but low usage",
                    'potential_savings': row['current_stock'] * row['unit_price'] * 0.5
                }
                suggestions.append(suggestion)
            
            logger.info(f"✓ Generated {len(suggestions)} cost optimization suggestions")
            return suggestions
        except Exception as e:
            logger.error(f"Error getting cost optimization suggestions: {str(e)}")
            return []
    
    @staticmethod
    def get_demand_insights(df):
        """
        Get insights about demand patterns
        
        Args:
            df (pd.DataFrame): Medicine data
        
        Returns:
            dict: Demand insights
        """
        try:
            insights = {
                'total_medicines': len(df),
                'high_demand': len(df[df['stock_status'] == STOCK_STATUS_LOW]) + len(df[df['stock_status'] == STOCK_STATUS_CRITICAL]),
                'normal_demand': len(df[df['stock_status'] == STOCK_STATUS_NORMAL]),
                'low_demand': len(df[df['stock_status'] == STOCK_STATUS_HIGH]),
                'out_of_stock': len(df[df['stock_status'] == STOCK_STATUS_OUT]),
                'total_value': df['inventory_value'].sum() if 'inventory_value' in df.columns else 0,
                'average_stock': df['current_stock'].mean(),
                'critical_items': len(df[df['current_stock'] == 0])
            }
            
            logger.info(f"✓ Generated demand insights")
            return insights
        except Exception as e:
            logger.error(f"Error getting demand insights: {str(e)}")
            return {}
    
    @staticmethod
    def get_action_plan(df, forecast_data=None):
        """
        Generate comprehensive action plan
        
        Args:
            df (pd.DataFrame): Medicine data
            forecast_data (dict): Optional forecast data
        
        Returns:
            dict: Comprehensive action plan
        """
        try:
            action_plan = {
                'urgent_actions': [],
                'planned_actions': [],
                'monitoring_items': [],
                'insights': {}
            }
            
            # Urgent: Critical stock or expired items
            urgent_items = df[
                (df['stock_status'] == STOCK_STATUS_CRITICAL) |
                (df['days_to_expiry'] < 0) |
                (df['current_stock'] == 0)
            ]
            
            for _, item in urgent_items.iterrows():
                action_plan['urgent_actions'].append({
                    'medicine': item['name'],
                    'action': f"Immediate restock required",
                    'priority': 'CRITICAL'
                })
            
            # Planned: Low stock items
            planned_items = df[df['stock_status'] == STOCK_STATUS_LOW]
            for _, item in planned_items.iterrows():
                action_plan['planned_actions'].append({
                    'medicine': item['name'],
                    'action': f"Schedule restock within 1-2 days",
                    'priority': 'HIGH'
                })
            
            # Monitoring: Normal or high stock
            monitoring_items = df[df['stock_status'].isin([STOCK_STATUS_NORMAL, STOCK_STATUS_HIGH])]
            action_plan['monitoring_items'] = len(monitoring_items)
            
            # Add insights
            action_plan['insights'] = RecommendationEngine.get_demand_insights(df)
            
            logger.info(f"✓ Generated action plan with {len(action_plan['urgent_actions'])} urgent actions")
            return action_plan
        except Exception as e:
            logger.error(f"Error generating action plan: {str(e)}")
            return {}


def get_purchase_recommendations(df):
    """Convenience function"""
    return RecommendationEngine.get_purchase_recommendations(df)


def get_demand_insights(df):
    """Convenience function"""
    return RecommendationEngine.get_demand_insights(df)
