"""
Tables Component Module
Data table display components
"""

from core.logger import get_logger

logger = get_logger(__name__)


class TableComponents:
    """Data table components for dashboard"""
    
    @staticmethod
    def format_dataframe_for_display(df, column_formats=None):
        """
        Format dataframe for display
        
        Args:
            df (pd.DataFrame): Data to format
            column_formats (dict): Format specifications per column
        
        Returns:
            pd.DataFrame: Formatted dataframe
        """
        try:
            formatted_df = df.copy()
            
            if column_formats:
                for col, fmt in column_formats.items():
                    if col in formatted_df.columns:
                        if fmt == 'currency':
                            formatted_df[col] = formatted_df[col].apply(lambda x: f"${x:.2f}")
                        elif fmt == 'percent':
                            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.2f}%")
                        elif fmt == 'decimal':
                            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.2f}")
            
            logger.debug("Dataframe formatted for display")
            return formatted_df
        except Exception as e:
            logger.error(f"Error formatting dataframe: {str(e)}")
            return df
    
    @staticmethod
    def create_summary_table(data, title='Summary'):
        """
        Create summary table
        
        Args:
            data (dict or list): Summary data
            title (str): Table title
        
        Returns:
            dict: Table data structure
        """
        try:
            table = {
                'title': title,
                'data': data,
                'type': 'summary'
            }
            logger.debug(f"Created summary table: {title}")
            return table
        except Exception as e:
            logger.error(f"Error creating summary table: {str(e)}")
            return None
    
    @staticmethod
    def get_column_display_config():
        """Get default column display configuration"""
        return {
            'medicine_id': {'type': 'number', 'width': 80},
            'name': {'type': 'text', 'width': 200},
            'category': {'type': 'text', 'width': 120},
            'current_stock': {'type': 'number', 'width': 100},
            'min_stock': {'type': 'number', 'width': 100},
            'max_stock': {'type': 'number', 'width': 100},
            'unit_price': {'type': 'currency', 'width': 100},
            'inventory_value': {'type': 'currency', 'width': 120},
            'stock_status': {'type': 'status', 'width': 100},
            'days_to_expiry': {'type': 'number', 'width': 100},
            'supplier_id': {'type': 'text', 'width': 100}
        }
    
    @staticmethod
    def filter_table_data(df, filters):
        """
        Filter table data based on criteria
        
        Args:
            df (pd.DataFrame): Data to filter
            filters (dict): Filter criteria
        
        Returns:
            pd.DataFrame: Filtered data
        """
        try:
            filtered_df = df.copy()
            
            for column, value in filters.items():
                if column in filtered_df.columns:
                    if isinstance(value, list):
                        filtered_df = filtered_df[filtered_df[column].isin(value)]
                    else:
                        filtered_df = filtered_df[filtered_df[column] == value]
            
            logger.debug(f"Filtered data: {len(filtered_df)} rows")
            return filtered_df
        except Exception as e:
            logger.error(f"Error filtering data: {str(e)}")
            return df
    
    @staticmethod
    def sort_table_data(df, sort_by, ascending=True):
        """
        Sort table data
        
        Args:
            df (pd.DataFrame): Data to sort
            sort_by (str): Column to sort by
            ascending (bool): Sort direction
        
        Returns:
            pd.DataFrame: Sorted data
        """
        try:
            if sort_by in df.columns:
                sorted_df = df.sort_values(by=sort_by, ascending=ascending)
                logger.debug(f"Sorted data by {sort_by}")
                return sorted_df
            return df
        except Exception as e:
            logger.error(f"Error sorting data: {str(e)}")
            return df
    
    @staticmethod
    def paginate_table(df, page=1, page_size=10):
        """
        Paginate table data
        
        Args:
            df (pd.DataFrame): Data to paginate
            page (int): Page number (1-indexed)
            page_size (int): Records per page
        
        Returns:
            tuple: (paginated_df, total_pages, current_page)
        """
        try:
            total_rows = len(df)
            total_pages = (total_rows + page_size - 1) // page_size
            
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            
            paginated_df = df.iloc[start_idx:end_idx]
            
            return paginated_df, total_pages, page
        except Exception as e:
            logger.error(f"Error paginating data: {str(e)}")
            return df, 1, 1
