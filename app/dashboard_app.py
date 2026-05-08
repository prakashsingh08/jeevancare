# """
# Main Dashboard Application
# Main Streamlit dashboard for JeevanCare Analytics Platform
# """

# import streamlit as st
# import pandas as pd
# from datetime import datetime
# from core.logger import get_logger
# from core.config import load_config
# from services.firebase_service import get_firebase_service
# from services.database_service import get_database_service
# from pipelines.ingestion_pipeline import IngestionPipeline
# from pipelines.processing_pipeline import ProcessingPipeline
# from domain.inventory import InventoryManagement
# from domain.alerts import AlertSystem
# from domain.recommendations import RecommendationEngine
# from app.components.charts import ChartComponents
# from app.components.kpi_cards import KPICards

# logger = get_logger(__name__)

# # Configure Streamlit page
# st.set_page_config(
#     page_title="JeevanCare Analytics",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Configure page styles
# st.markdown("""
#     <style>
#     [data-testid="stMetricLabel"] {
#         font-size: 14px;
#         font-weight: 600;
#     }
#     [data-testid="stMetricValue"] {
#         font-size: 32px;
#         font-weight: 700;
#     }
#     </style>
#     """, unsafe_allow_html=True)


# @st.cache_resource
# def initialize_services():
#     """Initialize services with caching"""
#     config = load_config()
#     firebase = get_firebase_service()
#     db = get_database_service()
#     return config, firebase, db


# @st.cache_data(ttl=300)
# def load_data():
#     """Load and process data with caching"""
#     try:
#         db = get_database_service()
#         medicines = db.load_medicine_data(use_cache=True)
#         return medicines
#     except Exception as e:
#         logger.error(f"Error loading data: {str(e)}")
#         st.error("Error loading data")
#         return pd.DataFrame()


# def main():
#     """Main dashboard function"""
#     try:
#         # Initialize services
#         config, firebase, db = initialize_services()
        
#         # Header
#         col1, col2 = st.columns([3, 1])
#         with col1:
#             st.title("🏥 JeevanCare Analytics Platform")
#             st.markdown("Medicine Inventory Optimization & Demand Forecasting")
#         with col2:
#             st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
        
#         st.divider()
        
#         # Sidebar
#         with st.sidebar:
#             st.header("📋 Navigation")
#             page = st.radio(
#                 "Select View",
#                 ["📊 Overview", "📦 Inventory", "⚠️ Alerts", "📈 Forecasts", "💡 Recommendations"]
#             )
        
#         # Load data
#         medicines_df = load_data()
        
#         if medicines_df.empty:
#             st.warning("No data available. Please ensure data is loaded into the system.")
#             return
        
#         # Page routing
#         if page == "📊 Overview":
#             show_overview(medicines_df)
#         elif page == "📦 Inventory":
#             show_inventory(medicines_df)
#         elif page == "⚠️ Alerts":
#             show_alerts(medicines_df)
#         elif page == "📈 Forecasts":
#             show_forecasts(medicines_df)
#         elif page == "💡 Recommendations":
#             show_recommendations(medicines_df)
        
#         # Footer
#         st.divider()
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.caption(f"📊 Total Records: {len(medicines_df)}")
#         with col2:
#             st.caption(f"🔄 Refresh Interval: Every 5 minutes")
#         with col3:
#             st.caption(f"✓ Last Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
#     except Exception as e:
#         logger.error(f"Dashboard error: {str(e)}")
#         st.error("An error occurred. Please refresh the page.")


# def show_overview(df):
#     """Show overview page"""
#     st.header("📊 Inventory Overview")
    
#     try:
#         # KPIs
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.metric("Total Medicines", len(df))
        
#         with col2:
#             total_value = (df['current_stock'] * df['unit_price']).sum()
#             st.metric("Total Value", f"${total_value:,.2f}")
        
#         with col3:
#             avg_stock = df['current_stock'].mean()
#             st.metric("Avg Stock", f"{avg_stock:.2f}")
        
#         with col4:
#             critical_count = len(df[df['current_stock'] == 0])
#             st.metric("Out of Stock", critical_count)
        
#         st.divider()
        
#         # Charts
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Stock status distribution
#             status_counts = df['stock_status'].value_counts()
#             fig = ChartComponents.create_pie_chart(
#                 status_counts.reset_index(),
#                 values_col='count',
#                 names_col='stock_status',
#                 title='Stock Status Distribution'
#             )
#             st.plotly_chart(fig, use_container_width=True)
        
#         with col2:
#             # Top medicines by value
#             top_medicines = df.nlargest(10, 'inventory_value')[['name', 'inventory_value']]
#             fig = ChartComponents.create_bar_chart(
#                 top_medicines,
#                 x_col='name',
#                 y_col='inventory_value',
#                 title='Top 10 Medicines by Inventory Value'
#             )
#             st.plotly_chart(fig, use_container_width=True)
        
#         # Summary statistics
#         st.subheader("Summary Statistics")
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.write(f"**Categories:** {df['category'].nunique()}")
#         with col2:
#             st.write(f"**Suppliers:** {df['supplier_id'].nunique()}")
#         with col3:
#             st.write(f"**Average Price:** ${df['unit_price'].mean():.2f}")
#         with col4:
#             st.write(f"**Stock Utilization:** {(df['current_stock'].sum() / df['max_stock'].sum() * 100):.2f}%")
    
#     except Exception as e:
#         logger.error(f"Error in overview page: {str(e)}")
#         st.error("Error displaying overview")


# def show_inventory(df):
#     """Show inventory management page"""
#     st.header("📦 Inventory Management")
    
#     try:
#         # Filters
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             selected_category = st.multiselect(
#                 "Filter by Category",
#                 options=df['category'].unique(),
#                 default=df['category'].unique()[:5]
#             )
        
#         with col2:
#             selected_status = st.multiselect(
#                 "Filter by Status",
#                 options=df['stock_status'].unique(),
#                 default=df['stock_status'].unique()
#             )
        
#         with col3:
#             sort_by = st.selectbox(
#                 "Sort By",
#                 options=['name', 'current_stock', 'inventory_value', 'unit_price']
#             )
        
#         # Filter data
#         filtered_df = df[
#             (df['category'].isin(selected_category)) &
#             (df['stock_status'].isin(selected_status))
#         ].sort_values(by=sort_by, ascending=False)
        
#         st.divider()
        
#         # Display table
#         st.subheader(f"Medicines ({len(filtered_df)} items)")
        
#         # Select columns to display
#         display_columns = ['medicine_id', 'name', 'category', 'current_stock', 'min_stock', 'max_stock', 'unit_price', 'stock_status']
        
#         st.dataframe(
#             filtered_df[display_columns],
#             use_container_width=True,
#             height=400
#         )
        
#         # Export option
#         if st.button("📥 Export as CSV"):
#             csv = filtered_df.to_csv(index=False)
#             st.download_button(
#                 label="Download CSV",
#                 data=csv,
#                 file_name=f"inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#                 mime="text/csv"
#             )
    
#     except Exception as e:
#         logger.error(f"Error in inventory page: {str(e)}")
#         st.error("Error displaying inventory")


# def show_alerts(df):
#     """Show alerts page"""
#     st.header("⚠️ Alerts & Issues")
    
#     try:
#         # Generate alerts
#         alert_system = AlertSystem()
#         alerts = alert_system.generate_alerts(df)
        
#         if not alerts:
#             st.success("✓ No alerts at this time")
#             return
        
#         # Group alerts by severity
#         critical_alerts = [a for a in alerts if a['severity'] == 'CRITICAL']
#         warning_alerts = [a for a in alerts if a['severity'] == 'WARNING']
#         info_alerts = [a for a in alerts if a['severity'] == 'INFO']
        
#         # Display critical alerts
#         if critical_alerts:
#             st.markdown("### 🔴 Critical Alerts")
#             for alert in critical_alerts:
#                 with st.container():
#                     col1, col2 = st.columns([4, 1])
#                     with col1:
#                         st.error(f"**{alert['type']}**: {alert['message']}")
#                     with col2:
#                         if st.button("Resolve", key=alert['id']):
#                             st.success("Alert resolved")
        
#         # Display warning alerts
#         if warning_alerts:
#             st.markdown("### 🟠 Warning Alerts")
#             for alert in warning_alerts:
#                 st.warning(f"**{alert['type']}**: {alert['message']}")
        
#         # Display info alerts
#         if info_alerts:
#             st.markdown("### 🟡 Info Alerts")
#             for alert in info_alerts:
#                 st.info(f"**{alert['type']}**: {alert['message']}")
    
#     except Exception as e:
#         logger.error(f"Error in alerts page: {str(e)}")
#         st.error("Error displaying alerts")


# def show_forecasts(df):
#     """Show forecasts page"""
#     st.header("📈 Demand Forecasts")
    
#     try:
#         st.info("Forecast feature will display demand predictions for selected medicines.")
        
#         # Select medicine
#         selected_medicine = st.selectbox(
#             "Select Medicine",
#             options=df['name'].unique()
#         )
        
#         medicine_data = df[df['name'] == selected_medicine].iloc[0]
        
#         st.markdown(f"### {selected_medicine}")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Current Stock", int(medicine_data['current_stock']))
#         with col2:
#             st.metric("Unit Price", f"${medicine_data['unit_price']:.2f}")
#         with col3:
#             st.metric("Status", medicine_data['stock_status'])
        
#         st.warning("Forecast data will be updated when historical data is available")
    
#     except Exception as e:
#         logger.error(f"Error in forecasts page: {str(e)}")
#         st.error("Error displaying forecasts")


# def show_recommendations(df):
#     """Show recommendations page"""
#     st.header("💡 Recommendations")
    
#     try:
#         # Get recommendations
#         rec_engine = RecommendationEngine()
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("📦 Purchase Recommendations")
#             purchase_recs = rec_engine.get_purchase_recommendations(df)
            
#             if purchase_recs:
#                 for rec in purchase_recs[:5]:
#                     with st.container():
#                         st.write(f"**{rec['medicine_name']}**")
#                         st.write(f"Recommended Qty: {rec['recommended_quantity']}")
#                         st.write(f"Est. Cost: ${rec['estimated_cost']:.2f}")
#                         st.divider()
#             else:
#                 st.info("No purchase recommendations at this time")
        
#         with col2:
#             st.subheader("📊 Demand Insights")
#             insights = rec_engine.get_demand_insights(df)
            
#             st.metric("Total Medicines", insights['total_medicines'])
#             st.metric("High Demand Items", insights['high_demand'])
#             st.metric("Normal Demand Items", insights['normal_demand'])
#             st.metric("Total Inventory Value", f"${insights['total_value']:,.2f}")
    
#     except Exception as e:
#         logger.error(f"Error in recommendations page: {str(e)}")
#         st.error("Error displaying recommendations")


# if __name__ == '__main__':
#     main()



#==============

"""
Main Dashboard Application
Main Streamlit dashboard for JeevanCare Analytics Platform
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

from core.logger import get_logger
from core.config import load_config
from services.firebase_service import get_firebase_service
from services.database_service import get_database_service
from pipelines.ingestion_pipeline import IngestionPipeline
from pipelines.processing_pipeline import ProcessingPipeline
from domain.inventory import InventoryManagement
from domain.alerts import AlertSystem
from domain.recommendations import RecommendationEngine
from app.components.charts import ChartComponents
from app.components.kpi_cards import KPICards

logger = get_logger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="JeevanCare Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AUTO REFRESH EVERY 2 SECONDS
st_autorefresh(interval=2000, key="dashboard_refresh")

# Configure page styles
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def initialize_services():
    """Initialize services with caching"""
    config = load_config()
    firebase = get_firebase_service()
    db = get_database_service()
    return config, firebase, db


# REDUCED CACHE TTL TO 2 SECONDS
@st.cache_data(ttl=2)
def load_data():
    """Load and process data with caching"""
    try:
        db = get_database_service()
        medicines = db.load_medicine_data(use_cache=False)
        return medicines
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        st.error("Error loading data")
        return pd.DataFrame()


def main():
    """Main dashboard function"""
    try:
        # Initialize services
        config, firebase, db = initialize_services()

        # Header
        col1, col2 = st.columns([3, 1])

        with col1:
            st.title("🏥 JeevanCare Analytics Platform")
            st.markdown("Medicine Inventory Optimization & Demand Forecasting")

        with col2:
            st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))

        st.divider()

        # Sidebar
        with st.sidebar:
            st.header("📋 Navigation")

            page = st.radio(
                "Select View",
                [
                    "📊 Overview",
                    "📦 Inventory",
                    "⚠️ Alerts",
                    "📈 Forecasts",
                    "💡 Recommendations"
                ]
            )

        # Load latest data
        medicines_df = load_data()

        if medicines_df.empty:
            st.warning("No data available. Please ensure data is loaded into the system.")
            return

        # Page routing
        if page == "📊 Overview":
            show_overview(medicines_df)

        elif page == "📦 Inventory":
            show_inventory(medicines_df)

        elif page == "⚠️ Alerts":
            show_alerts(medicines_df)

        elif page == "📈 Forecasts":
            show_forecasts(medicines_df)

        elif page == "💡 Recommendations":
            show_recommendations(medicines_df)

        # Footer
        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption(f"📊 Total Records: {len(medicines_df)}")

        with col2:
            st.caption("🔄 Auto Refresh: Every 2 seconds")

        with col3:
            st.caption(
                f"✓ Last Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        st.error("An error occurred. Please refresh the page.")


def show_overview(df):
    """Show overview page"""

    st.header("📊 Inventory Overview")

    try:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Medicines", len(df))

        with col2:
            total_value = (df['current_stock'] * df['unit_price']).sum()
            st.metric("Total Value", f"${total_value:,.2f}")

        with col3:
            avg_stock = df['current_stock'].mean()
            st.metric("Avg Stock", f"{avg_stock:.2f}")

        with col4:
            critical_count = len(df[df['current_stock'] == 0])
            st.metric("Out of Stock", critical_count)

        st.divider()

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            status_counts = df['stock_status'].value_counts()

            fig = ChartComponents.create_pie_chart(
                status_counts.reset_index(),
                values_col='count',
                names_col='stock_status',
                title='Stock Status Distribution'
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            top_medicines = df.nlargest(
                10,
                'inventory_value'
            )[['name', 'inventory_value']]

            fig = ChartComponents.create_bar_chart(
                top_medicines,
                x_col='name',
                y_col='inventory_value',
                title='Top 10 Medicines by Inventory Value'
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        logger.error(f"Error in overview page: {str(e)}")
        st.error("Error displaying overview")


def show_inventory(df):
    """Show inventory management page"""

    st.header("📦 Inventory Management")

    try:
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_category = st.multiselect(
                "Filter by Category",
                options=df['category'].unique(),
                default=df['category'].unique()[:5]
            )

        with col2:
            selected_status = st.multiselect(
                "Filter by Status",
                options=df['stock_status'].unique(),
                default=df['stock_status'].unique()
            )

        with col3:
            sort_by = st.selectbox(
                "Sort By",
                options=[
                    'name',
                    'current_stock',
                    'inventory_value',
                    'unit_price'
                ]
            )

        filtered_df = df[
            (df['category'].isin(selected_category)) &
            (df['stock_status'].isin(selected_status))
        ].sort_values(by=sort_by, ascending=False)

        st.divider()

        st.subheader(f"Medicines ({len(filtered_df)} items)")

        display_columns = [
            'medicine_id',
            'name',
            'category',
            'current_stock',
            'min_stock',
            'max_stock',
            'unit_price',
            'stock_status'
        ]

        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            height=400
        )

    except Exception as e:
        logger.error(f"Error in inventory page: {str(e)}")
        st.error("Error displaying inventory")


def show_alerts(df):
    """Show alerts page"""

    st.header("⚠️ Alerts & Issues")

    try:
        alert_system = AlertSystem()
        alerts = alert_system.generate_alerts(df)

        if not alerts:
            st.success("✓ No alerts at this time")
            return

        critical_alerts = [
            a for a in alerts
            if a['severity'] == 'CRITICAL'
        ]

        warning_alerts = [
            a for a in alerts
            if a['severity'] == 'WARNING'
        ]

        info_alerts = [
            a for a in alerts
            if a['severity'] == 'INFO'
        ]

        if critical_alerts:
            st.markdown("### 🔴 Critical Alerts")

            for alert in critical_alerts:
                st.error(
                    f"**{alert['type']}**: {alert['message']}"
                )

        if warning_alerts:
            st.markdown("### 🟠 Warning Alerts")

            for alert in warning_alerts:
                st.warning(
                    f"**{alert['type']}**: {alert['message']}"
                )

        if info_alerts:
            st.markdown("### 🟡 Info Alerts")

            for alert in info_alerts:
                st.info(
                    f"**{alert['type']}**: {alert['message']}"
                )

    except Exception as e:
        logger.error(f"Error in alerts page: {str(e)}")
        st.error("Error displaying alerts")


def show_forecasts(df):
    """Show forecasts page"""

    st.header("📈 Demand Forecasts")

    try:
        st.info(
            "Forecast feature will display demand predictions "
            "for selected medicines."
        )

        selected_medicine = st.selectbox(
            "Select Medicine",
            options=df['name'].unique()
        )

        medicine_data = df[
            df['name'] == selected_medicine
        ].iloc[0]

        st.markdown(f"### {selected_medicine}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current Stock",
                int(medicine_data['current_stock'])
            )

        with col2:
            st.metric(
                "Unit Price",
                f"${medicine_data['unit_price']:.2f}"
            )

        with col3:
            st.metric(
                "Status",
                medicine_data['stock_status']
            )

    except Exception as e:
        logger.error(f"Error in forecasts page: {str(e)}")
        st.error("Error displaying forecasts")


def show_recommendations(df):
    """Show recommendations page"""

    st.header("💡 Recommendations")

    try:
        rec_engine = RecommendationEngine()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📦 Purchase Recommendations")

            purchase_recs = rec_engine.get_purchase_recommendations(df)

            if purchase_recs:
                for rec in purchase_recs[:5]:
                    st.write(f"**{rec['medicine_name']}**")
                    st.write(
                        f"Recommended Qty: "
                        f"{rec['recommended_quantity']}"
                    )
                    st.write(
                        f"Est. Cost: "
                        f"${rec['estimated_cost']:.2f}"
                    )
                    st.divider()

            else:
                st.info("No purchase recommendations at this time")

        with col2:
            st.subheader("📊 Demand Insights")

            insights = rec_engine.get_demand_insights(df)

            st.metric(
                "Total Medicines",
                insights['total_medicines']
            )

            st.metric(
                "High Demand Items",
                insights['high_demand']
            )

            st.metric(
                "Normal Demand Items",
                insights['normal_demand']
            )

            st.metric(
                "Total Inventory Value",
                f"${insights['total_value']:,.2f}"
            )

    except Exception as e:
        logger.error(f"Error in recommendations page: {str(e)}")
        st.error("Error displaying recommendations")


if __name__ == '__main__':
    main()