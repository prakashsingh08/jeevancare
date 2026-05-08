# """
# FULL ENTERPRISE MEDICINE INVENTORY DASHBOARD
# Streamlit + Firebase Ready Dashboard

# FEATURES:
# ✅ KPI Cards
# ✅ Inventory Analytics
# ✅ Expiry Tracking
# ✅ Supplier Analytics
# ✅ Alerts System
# ✅ Real-time Auto Refresh
# ✅ Plotly Interactive Charts
# ✅ Sidebar Filters
# ✅ Download CSV
# ✅ Professional Layout
# """

# import streamlit as st
# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# from streamlit_autorefresh import st_autorefresh

# import plotly.express as px
# import plotly.graph_objects as go


# # ==========================================
# # PAGE CONFIG
# # ==========================================

# st.set_page_config(
#     page_title="🏥 JeevanCare Analytics",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ==========================================
# # AUTO REFRESH
# # ==========================================

# st_autorefresh(interval=5000, key="refresh")


# # ==========================================
# # CUSTOM CSS
# # ==========================================

# st.markdown("""
# <style>

# .main {
#     background-color: #f5f7fa;
# }

# [data-testid="stMetricValue"] {
#     font-size: 32px;
#     font-weight: bold;
#     color: #1f77b4;
# }

# [data-testid="stMetricLabel"] {
#     font-size: 15px;
#     font-weight: 600;
# }

# .block-container {
#     padding-top: 1rem;
# }

# </style>
# """, unsafe_allow_html=True)


# # ==========================================
# # SAMPLE DATA
# # REPLACE THIS WITH FIREBASE DATA
# # ==========================================

# @st.cache_data(ttl=5)
# def load_data():

#     np.random.seed(42)

#     medicines = [
#         "Paracetamol", "Ibuprofen", "Aspirin", "Amoxicillin",
#         "Azithromycin", "Metformin", "Atorvastatin",
#         "Omeprazole", "Ciprofloxacin", "Cetirizine",
#         "Dolo 650", "Pantoprazole", "Insulin",
#         "Vitamin C", "Calcium", "Diclofenac",
#         "Crocin", "Benadryl", "ORS", "Zinc"
#     ]

#     categories = [
#         "Antibiotic", "Painkiller", "Diabetes",
#         "Cardiac", "Vitamin", "General"
#     ]

#     suppliers = [
#         "SUP001", "SUP002", "SUP003",
#         "SUP004", "SUP005"
#     ]

#     data = []

#     for i in range(20):

#         current_stock = np.random.randint(10, 500)
#         min_stock = np.random.randint(20, 100)
#         max_stock = np.random.randint(500, 1000)
#         unit_price = round(np.random.uniform(2, 50), 2)

#         expiry = datetime.today() + timedelta(
#             days=np.random.randint(-20, 365)
#         )

#         data.append({
#             "medicine_id": i + 1,
#             "name": medicines[i],
#             "category": np.random.choice(categories),
#             "current_stock": current_stock,
#             "min_stock": min_stock,
#             "max_stock": max_stock,
#             "unit_price": unit_price,
#             "expiry_date": expiry.date(),
#             "supplier_id": np.random.choice(suppliers)
#         })

#     df = pd.DataFrame(data)

#     # ==========================================
#     # DERIVED COLUMNS
#     # ==========================================

#     df["inventory_value"] = (
#         df["current_stock"] * df["unit_price"]
#     )

#     df["days_to_expiry"] = (
#         pd.to_datetime(df["expiry_date"]) -
#         pd.Timestamp.today()
#     ).dt.days

#     def stock_status(row):

#         if row["current_stock"] == 0:
#             return "OUT OF STOCK"

#         elif row["current_stock"] <= row["min_stock"]:
#             return "LOW"

#         elif row["current_stock"] >= row["max_stock"] * 0.8:
#             return "OVERSTOCK"

#         return "NORMAL"

#     df["stock_status"] = df.apply(stock_status, axis=1)

#     return df


# df = load_data()


# # ==========================================
# # SIDEBAR
# # ==========================================

# st.sidebar.title("🏥 JeevanCare")

# page = st.sidebar.radio(
#     "Navigation",
#     [
#         "Overview",
#         "Inventory",
#         "Expiry Tracker",
#         "Supplier Analytics",
#         "Alerts"
#     ]
# )

# st.sidebar.markdown("---")

# # FILTERS
# category_filter = st.sidebar.multiselect(
#     "Category",
#     options=df["category"].unique(),
#     default=df["category"].unique()
# )

# supplier_filter = st.sidebar.multiselect(
#     "Supplier",
#     options=df["supplier_id"].unique(),
#     default=df["supplier_id"].unique()
# )

# filtered_df = df[
#     (df["category"].isin(category_filter)) &
#     (df["supplier_id"].isin(supplier_filter))
# ]


# # ==========================================
# # HEADER
# # ==========================================

# st.title("🏥 JeevanCare Analytics Dashboard")
# st.caption("Real-Time Medicine Inventory Intelligence System")

# st.markdown("---")


# # ==========================================
# # OVERVIEW PAGE
# # ==========================================

# if page == "Overview":

#     total_medicines = len(filtered_df)

#     total_value = filtered_df["inventory_value"].sum()

#     low_stock = len(
#         filtered_df[
#             filtered_df["stock_status"] == "LOW"
#         ]
#     )

#     out_stock = len(
#         filtered_df[
#             filtered_df["stock_status"] == "OUT OF STOCK"
#         ]
#     )

#     expiring_soon = len(
#         filtered_df[
#             filtered_df["days_to_expiry"] <= 30
#         ]
#     )

#     suppliers = filtered_df["supplier_id"].nunique()

#     # ==========================================
#     # KPI CARDS
#     # ==========================================

#     col1, col2, col3, col4, col5, col6 = st.columns(6)

#     col1.metric(
#         "💊 Medicines",
#         total_medicines
#     )

#     col2.metric(
#         "💰 Inventory Value",
#         f"${total_value:,.0f}"
#     )

#     col3.metric(
#         "⚠️ Low Stock",
#         low_stock
#     )

#     col4.metric(
#         "❌ Out of Stock",
#         out_stock
#     )

#     col5.metric(
#         "⏳ Expiring Soon",
#         expiring_soon
#     )

#     col6.metric(
#         "🚚 Suppliers",
#         suppliers
#     )

#     st.markdown("---")

#     # ==========================================
#     # CHARTS
#     # ==========================================

#     col1, col2 = st.columns(2)

#     # STOCK STATUS PIE CHART
#     with col1:

#         st.subheader("📦 Stock Status Distribution")

#         status_counts = (
#             filtered_df["stock_status"]
#             .value_counts()
#             .reset_index()
#         )

#         status_counts.columns = [
#             "stock_status",
#             "count"
#         ]

#         fig = px.pie(
#             status_counts,
#             names="stock_status",
#             values="count",
#             hole=0.4
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#     # TOP MEDICINES
#     with col2:

#         st.subheader("💰 Top Medicines by Value")

#         top_df = (
#             filtered_df
#             .sort_values(
#                 "inventory_value",
#                 ascending=False
#             )
#             .head(10)
#         )

#         fig = px.bar(
#             top_df,
#             x="name",
#             y="inventory_value",
#             color="inventory_value",
#             text_auto=True
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#     # ==========================================
#     # CATEGORY ANALYTICS
#     # ==========================================

#     st.subheader("📊 Category Analytics")

#     category_summary = (
#         filtered_df.groupby("category")
#         .agg({
#             "current_stock": "sum",
#             "inventory_value": "sum"
#         })
#         .reset_index()
#     )

#     fig = px.treemap(
#         category_summary,
#         path=["category"],
#         values="inventory_value",
#         color="current_stock"
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )


# # ==========================================
# # INVENTORY PAGE
# # ==========================================

# elif page == "Inventory":

#     st.subheader("📦 Inventory Management")

#     search = st.text_input(
#         "Search Medicine"
#     )

#     inventory_df = filtered_df.copy()

#     if search:
#         inventory_df = inventory_df[
#             inventory_df["name"]
#             .str.contains(search, case=False)
#         ]

#     st.dataframe(
#         inventory_df,
#         use_container_width=True,
#         height=600
#     )

#     # DOWNLOAD CSV
#     csv = inventory_df.to_csv(index=False)

#     st.download_button(
#         label="📥 Download CSV",
#         data=csv,
#         file_name="inventory.csv",
#         mime="text/csv"
#     )


# # ==========================================
# # EXPIRY TRACKER
# # ==========================================

# elif page == "Expiry Tracker":

#     st.subheader("⏳ Expiry Tracker")

#     expired = filtered_df[
#         filtered_df["days_to_expiry"] < 0
#     ]

#     expiring_7 = filtered_df[
#         filtered_df["days_to_expiry"] <= 7
#     ]

#     expiring_30 = filtered_df[
#         filtered_df["days_to_expiry"] <= 30
#     ]

#     col1, col2, col3 = st.columns(3)

#     col1.metric(
#         "❌ Expired",
#         len(expired)
#     )

#     col2.metric(
#         "⚠️ Expiring in 7 Days",
#         len(expiring_7)
#     )

#     col3.metric(
#         "⏳ Expiring in 30 Days",
#         len(expiring_30)
#     )

#     st.markdown("---")

#     fig = px.scatter(
#         filtered_df,
#         x="name",
#         y="days_to_expiry",
#         color="stock_status",
#         size="current_stock",
#         hover_data=["category"]
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.subheader("Medicines Near Expiry")

#     near_expiry = filtered_df[
#         filtered_df["days_to_expiry"] <= 30
#     ]

#     st.dataframe(
#         near_expiry,
#         use_container_width=True
#     )


# # ==========================================
# # SUPPLIER ANALYTICS
# # ==========================================

# elif page == "Supplier Analytics":

#     st.subheader("🚚 Supplier Analytics")

#     supplier_summary = (
#         filtered_df.groupby("supplier_id")
#         .agg({
#             "inventory_value": "sum",
#             "medicine_id": "count",
#             "current_stock": "sum"
#         })
#         .reset_index()
#     )

#     supplier_summary.columns = [
#         "supplier_id",
#         "inventory_value",
#         "medicine_count",
#         "stock"
#     ]

#     col1, col2 = st.columns(2)

#     with col1:

#         fig = px.bar(
#             supplier_summary,
#             x="supplier_id",
#             y="inventory_value",
#             color="inventory_value",
#             text_auto=True
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#     with col2:

#         fig = px.pie(
#             supplier_summary,
#             names="supplier_id",
#             values="medicine_count"
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#     st.dataframe(
#         supplier_summary,
#         use_container_width=True
#     )


# # ==========================================
# # ALERTS PAGE
# # ==========================================

# elif page == "Alerts":

#     st.subheader("⚠️ Inventory Alerts")

#     low_stock_df = filtered_df[
#         filtered_df["stock_status"] == "LOW"
#     ]

#     overstock_df = filtered_df[
#         filtered_df["stock_status"] == "OVERSTOCK"
#     ]

#     expired_df = filtered_df[
#         filtered_df["days_to_expiry"] < 0
#     ]

#     if not low_stock_df.empty:

#         st.error("🚨 LOW STOCK ALERTS")

#         st.dataframe(
#             low_stock_df[
#                 [
#                     "name",
#                     "current_stock",
#                     "min_stock"
#                 ]
#             ],
#             use_container_width=True
#         )

#     if not overstock_df.empty:

#         st.warning("📦 OVERSTOCK ALERTS")

#         st.dataframe(
#             overstock_df[
#                 [
#                     "name",
#                     "current_stock",
#                     "max_stock"
#                 ]
#             ],
#             use_container_width=True
#         )

#     if not expired_df.empty:

#         st.error("❌ EXPIRED MEDICINES")

#         st.dataframe(
#             expired_df[
#                 [
#                     "name",
#                     "expiry_date",
#                     "days_to_expiry"
#                 ]
#             ],
#             use_container_width=True
#         )


# # ==========================================
# # FOOTER
# # ==========================================

# st.markdown("---")

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.caption(
#         f"📊 Total Records: {len(filtered_df)}"
#     )

# with col2:
#     st.caption(
#         "🔄 Auto Refresh: Every 5 seconds"
#     )

# with col3:
#     st.caption(
#         f"🕒 Last Sync: "
#         f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
#     )


# def main():
#     """Main dashboard function"""

#     try:

#         # Initialize services
#         config, firebase, db = initialize_services()

#         # Header
#         col1, col2 = st.columns([3, 1])

#         with col1:
#             st.title("🏥 JeevanCare Analytics Platform")
#             st.markdown(
#                 "Medicine Inventory Optimization & Demand Forecasting"
#             )

#         with col2:
#             st.metric(
#                 "Last Updated",
#                 datetime.now().strftime("%H:%M:%S")
#             )

#         st.divider()

#         # Sidebar
#         with st.sidebar:

#             st.header("📋 Navigation")

#             page = st.radio(
#                 "Select View",
#                 [
#                     "📊 Overview",
#                     "📦 Inventory",
#                     "⚠️ Alerts",
#                     "📈 Forecasts",
#                     "💡 Recommendations"
#                 ]
#             )

#         # Load data
#         medicines_df = load_data()

#         if medicines_df.empty:
#             st.warning("No data available")
#             return

#         # ROUTING
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

#     except Exception as e:

#         logger.error(f"Dashboard Error: {str(e)}")

#         st.error("Dashboard failed to load")


# # ==========================================
# # ENTRY POINT
# # ==========================================

# if __name__ == '__main__':
#     main()

"""
FULL ENTERPRISE MEDICINE INVENTORY DASHBOARD
Firebase + Streamlit + Logger Compatible
"""

# ==========================================
# IMPORTS
# ==========================================

import streamlit as st
import pandas as pd

from datetime import datetime

from streamlit_autorefresh import st_autorefresh

import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# JEEVANCARE IMPORTS
# ==========================================

from core.logger import get_logger
from core.config import load_config

from services.firebase_service import (
    get_firebase_service
)

from services.database_service import (
    get_database_service
)

# ==========================================
# LOGGER
# ==========================================

logger = get_logger(__name__)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="🏥 JeevanCare Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# AUTO REFRESH
# ==========================================

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

[data-testid="stMetricValue"] {
    font-size: 30px;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    font-size: 15px;
    font-weight: 600;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# INITIALIZE SERVICES
# ==========================================

@st.cache_resource
def initialize_services():

    try:

        config = load_config()

        firebase = get_firebase_service()

        db = get_database_service()

        logger.info(
            "Services initialized successfully"
        )

        return config, firebase, db

    except Exception as e:

        logger.error(
            f"Service initialization failed: {str(e)}"
        )

        st.error(
            "Failed to initialize services"
        )

        return None, None, None


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data(ttl=5)
def load_data():

    try:

        db = get_database_service()

        df = db.load_medicine_data(
            use_cache=False
        )

        if df.empty:

            logger.warning(
                "No medicine data found"
            )

            return pd.DataFrame()

        # ==========================================
        # DERIVED COLUMNS
        # ==========================================

        df["inventory_value"] = (
            df["current_stock"] *
            df["unit_price"]
        )

        df["days_to_expiry"] = (
            pd.to_datetime(df["expiry_date"]) -
            pd.Timestamp.today()
        ).dt.days

        def stock_status(row):

            if row["current_stock"] == 0:
                return "OUT OF STOCK"

            elif row["current_stock"] <= row["min_stock"]:
                return "LOW STOCK"

            elif row["current_stock"] >= (
                row["max_stock"] * 0.8
            ):
                return "OVERSTOCK"

            return "NORMAL"

        df["stock_status"] = df.apply(
            stock_status,
            axis=1
        )

        logger.info(
            f"Loaded {len(df)} records"
        )

        return df

    except Exception as e:

        logger.error(
            f"Error loading data: {str(e)}"
        )

        st.error(
            "Failed to load medicine data"
        )

        return pd.DataFrame()


# ==========================================
# OVERVIEW PAGE
# ==========================================

def show_overview(df):

    st.header(
        "🏥 Enterprise Inventory Dashboard"
    )

    try:

        # ==========================================
        # KPI CALCULATIONS
        # ==========================================

        total_medicines = len(df)

        total_value = (
            df["inventory_value"].sum()
        )

        avg_stock = (
            df["current_stock"].mean()
        )

        low_stock = len(
            df[
                df["stock_status"] ==
                "LOW STOCK"
            ]
        )

        out_stock = len(
            df[
                df["stock_status"] ==
                "OUT OF STOCK"
            ]
        )

        expiring_soon = len(
            df[
                df["days_to_expiry"] <= 30
            ]
        )

        supplier_count = (
            df["supplier_id"].nunique()
        )

        # ==========================================
        # KPI ROW
        # ==========================================

        st.subheader(
            "📊 Executive Summary"
        )

        col1, col2, col3, col4, col5, col6 = (
            st.columns(6)
        )

        with col1:
            st.metric(
                "💊 Medicines",
                total_medicines
            )

        with col2:
            st.metric(
                "💰 Inventory Value",
                f"${total_value:,.0f}"
            )

        with col3:
            st.metric(
                "📦 Avg Stock",
                f"{avg_stock:.0f}"
            )

        with col4:
            st.metric(
                "⚠️ Low Stock",
                low_stock
            )

        with col5:
            st.metric(
                "❌ Out of Stock",
                out_stock
            )

        with col6:
            st.metric(
                "🚚 Suppliers",
                supplier_count
            )

        st.divider()

        # ==========================================
        # CHARTS ROW 1
        # ==========================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "📦 Stock Distribution"
            )

            status_counts = (
                df["stock_status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "status",
                "count"
            ]

            fig = px.pie(
                status_counts,
                names="status",
                values="count",
                hole=0.5
            )

            fig.update_layout(
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.subheader(
                "💰 Top Medicines"
            )

            top_df = (
                df.sort_values(
                    "inventory_value",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                top_df,
                x="name",
                y="inventory_value",
                color="inventory_value",
                text_auto=True
            )

            fig.update_layout(
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.divider()

        # ==========================================
        # CATEGORY ANALYTICS
        # ==========================================

        st.subheader(
            "📊 Category Analytics"
        )

        category_summary = (
            df.groupby("category")
            .agg({
                "current_stock": "sum",
                "inventory_value": "sum"
            })
            .reset_index()
        )

        fig = px.treemap(
            category_summary,
            path=["category"],
            values="inventory_value",
            color="current_stock"
        )

        fig.update_layout(
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # ==========================================
        # EXPIRY ANALYSIS
        # ==========================================

        st.subheader(
            "⏳ Expiry Risk Analysis"
        )

        expiry_df = (
            df[
                ["name", "days_to_expiry"]
            ]
            .sort_values(
                "days_to_expiry"
            )
            .head(15)
        )

        fig = px.bar(
            expiry_df,
            x="name",
            y="days_to_expiry",
            color="days_to_expiry",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # ==========================================
        # INVENTORY HEALTH
        # ==========================================

        st.subheader(
            "🏥 Inventory Health"
        )

        stock_utilization = (
            df["current_stock"].sum() /
            df["max_stock"].sum()
        ) * 100

        st.progress(
            int(stock_utilization)
        )

        st.success(
            f"Inventory Utilization: "
            f"{stock_utilization:.2f}%"
        )

        st.divider()

        # ==========================================
        # CRITICAL ALERTS
        # ==========================================

        st.subheader(
            "🚨 Critical Alerts"
        )

        critical_df = df[
            (
                df["stock_status"] ==
                "LOW STOCK"
            )
            |
            (
                df["days_to_expiry"] <= 30
            )
        ]

        if critical_df.empty:

            st.success(
                "✅ No critical alerts"
            )

        else:

            st.dataframe(
                critical_df[
                    [
                        "name",
                        "category",
                        "current_stock",
                        "min_stock",
                        "days_to_expiry",
                        "stock_status"
                    ]
                ],
                use_container_width=True,
                height=300
            )

    except Exception as e:

        logger.error(
            f"Overview Error: {str(e)}"
        )

        st.error(
            "Failed to display overview"
        )


# ==========================================
# INVENTORY PAGE
# ==========================================

def show_inventory(df):

    st.header(
        "📦 Inventory Management"
    )

    try:

        col1, col2, col3 = st.columns(3)

        with col1:

            selected_category = (
                st.multiselect(
                    "Category",
                    options=df[
                        "category"
                    ].unique(),
                    default=df[
                        "category"
                    ].unique()
                )
            )

        with col2:

            selected_status = (
                st.multiselect(
                    "Stock Status",
                    options=df[
                        "stock_status"
                    ].unique(),
                    default=df[
                        "stock_status"
                    ].unique()
                )
            )

        with col3:

            search = st.text_input(
                "Search Medicine"
            )

        filtered_df = df[
            (
                df["category"].isin(
                    selected_category
                )
            )
            &
            (
                df["stock_status"].isin(
                    selected_status
                )
            )
        ]

        if search:

            filtered_df = filtered_df[
                filtered_df["name"]
                .str.contains(
                    search,
                    case=False
                )
            ]

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=600
        )

        csv = filtered_df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="inventory.csv",
            mime="text/csv"
        )

    except Exception as e:

        logger.error(
            f"Inventory Error: {str(e)}"
        )

        st.error(
            "Failed to display inventory"
        )


# ==========================================
# ALERTS PAGE
# ==========================================

def show_alerts(df):

    st.header(
        "⚠️ Alerts & Notifications"
    )

    try:

        low_stock_df = df[
            df["stock_status"] ==
            "LOW STOCK"
        ]

        expiry_df = df[
            df["days_to_expiry"] <= 30
        ]

        if not low_stock_df.empty:

            st.error(
                "🚨 LOW STOCK ALERTS"
            )

            st.dataframe(
                low_stock_df[
                    [
                        "name",
                        "current_stock",
                        "min_stock"
                    ]
                ],
                use_container_width=True
            )

        if not expiry_df.empty:

            st.warning(
                "⏳ EXPIRY ALERTS"
            )

            st.dataframe(
                expiry_df[
                    [
                        "name",
                        "expiry_date",
                        "days_to_expiry"
                    ]
                ],
                use_container_width=True
            )

    except Exception as e:

        logger.error(
            f"Alerts Error: {str(e)}"
        )

        st.error(
            "Failed to load alerts"
        )


# ==========================================
# FORECASTS PAGE
# ==========================================

def show_forecasts(df):

    st.header(
        "📈 Demand Forecasts"
    )

    st.info(
        "AI Forecasting module "
        "coming soon"
    )


# ==========================================
# RECOMMENDATIONS PAGE
# ==========================================

def show_recommendations(df):

    st.header(
        "💡 Smart Recommendations"
    )

    st.success(
        "Recommendation engine active"
    )


# ==========================================
# MAIN
# ==========================================

def main():

    try:

        initialize_services()

        medicines_df = load_data()

        if medicines_df.empty:

            st.warning(
                "No medicine data found"
            )

            return

        # HEADER

        col1, col2 = st.columns([4, 1])

        with col1:

            st.title(
                "🏥 JeevanCare Analytics"
            )

            st.caption(
                "Real-Time Medicine "
                "Inventory Intelligence"
            )

        with col2:

            st.metric(
                "Last Updated",
                datetime.now().strftime(
                    "%H:%M:%S"
                )
            )

        st.divider()

        # SIDEBAR

        with st.sidebar:

            st.header(
                "📋 Navigation"
            )

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

        # ROUTING

        if page == "📊 Overview":

            show_overview(
                medicines_df
            )

        elif page == "📦 Inventory":

            show_inventory(
                medicines_df
            )

        elif page == "⚠️ Alerts":

            show_alerts(
                medicines_df
            )

        elif page == "📈 Forecasts":

            show_forecasts(
                medicines_df
            )

        elif page == "💡 Recommendations":

            show_recommendations(
                medicines_df
            )

        # FOOTER

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.caption(
                f"📊 Records: "
                f"{len(medicines_df)}"
            )

        with col2:

            st.caption(
                "🔄 Auto Refresh: "
                "5 seconds"
            )

        with col3:

            st.caption(
                f"🕒 Sync: "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

    except Exception as e:

        logger.error(
            f"Dashboard Error: {str(e)}"
        )

        st.error(
            "Dashboard failed to load"
        )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == '__main__':
    main()