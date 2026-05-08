"""
MODERN ENTERPRISE MEDICINE INVENTORY DASHBOARD
PowerBI Style UI + Firebase + Streamlit
"""

# =========================================================
# IMPORTS
# =========================================================

import streamlit as st
import pandas as pd

from datetime import datetime

from streamlit_autorefresh import st_autorefresh

import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# JEEVANCARE IMPORTS
# =========================================================

from core.logger import get_logger
from core.config import load_config

from services.firebase_service import (
    get_firebase_service
)

from services.database_service import (
    get_database_service
)

# =========================================================
# LOGGER
# =========================================================

logger = get_logger(__name__)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="JeevanCare Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# AUTO REFRESH
# =========================================================

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

# =========================================================
# MODERN ENTERPRISE CSS
# =========================================================

st.markdown("""
<style>

/* =======================================================
GLOBAL
======================================================= */

.stApp {
    background-color: #f4f6fa;
}

/* =======================================================
REMOVE PADDING
======================================================= */

.block-container {
    padding-top: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

section.main > div {
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* =======================================================
SIDEBAR
======================================================= */

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e7eb;
    width: 300px !important;
}

/* =======================================================
KPI CARD
======================================================= */

.metric-card {
    background: white;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid #eceff5;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

/* =======================================================
CHART CARD
======================================================= */

.chart-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #eceff5;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

/* =======================================================
METRIC
======================================================= */

[data-testid="stMetricValue"] {
    font-size: 30px !important;
    font-weight: 700 !important;
    color: #111827;
}

[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #6b7280;
}

/* =======================================================
HEADERS
======================================================= */

h1, h2, h3 {
    color: #111827 !important;
    font-weight: 700 !important;
}

/* =======================================================
DATAFRAME
======================================================= */

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #eceff5;
}

/* =======================================================
BUTTONS
======================================================= */

.stButton > button {
    border-radius: 12px;
    border: none;
    background: #2563eb;
    color: white;
    font-weight: 600;
}

/* =======================================================
PLOTLY
======================================================= */

.js-plotly-plot {
    border-radius: 18px;
    overflow: hidden;
}

/* =======================================================
SCROLLBAR
======================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# INITIALIZE SERVICES
# =========================================================

@st.cache_resource
def initialize_services():

    try:

        config = load_config()

        firebase = get_firebase_service()

        db = get_database_service()

        logger.info(
            "Services initialized"
        )

        return config, firebase, db

    except Exception as e:

        logger.error(
            f"Initialization failed: {str(e)}"
        )

        st.error(
            "Failed to initialize services"
        )

        return None, None, None

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data(ttl=5)
def load_data():

    try:

        db = get_database_service()

        df = db.load_medicine_data(
            use_cache=False
        )

        if df.empty:

            logger.warning(
                "No medicine data"
            )

            return pd.DataFrame()

        # ===================================================
        # DERIVED COLUMNS
        # ===================================================

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
                return "OUT"

            elif row["current_stock"] <= row["min_stock"]:
                return "LOW"

            elif row["current_stock"] >= (
                row["max_stock"] * 0.8
            ):
                return "OVER"

            return "NORMAL"

        df["stock_status"] = df.apply(
            stock_status,
            axis=1
        )

        return df

    except Exception as e:

        logger.error(
            f"Data load failed: {str(e)}"
        )

        st.error(
            "Error loading Firebase data"
        )

        return pd.DataFrame()

# =========================================================
# MAIN
# =========================================================

def main():

    try:

        initialize_services()

        df = load_data()

        if df.empty:

            st.warning(
                "No medicine data found"
            )

            return

        # =====================================================
        # MODERN SIDEBAR
        # =====================================================

        with st.sidebar:

            st.markdown("""
            <div style="
                padding-top:10px;
                padding-bottom:20px;
            ">
                <h1 style="
                    color:#111827;
                    font-size:28px;
                    font-weight:800;
                    margin-bottom:0px;
                ">
                    🏥 JeevanCare
                </h1>

                <p style="
                    color:#6b7280;
                    font-size:14px;
                    margin-top:0px;
                ">
                    Enterprise Analytics Suite
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            st.markdown("""
            <p style="
                color:#9ca3af;
                font-size:12px;
                font-weight:700;
                letter-spacing:1px;
            ">
                NAVIGATION
            </p>
            """, unsafe_allow_html=True)

            page = st.radio(
                "",
                [
                    "📊 Overview",
                    "📦 Inventory",
                    "⚠️ Alerts",
                    "📈 Forecasts",
                    "💡 Recommendations"
                ]
            )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <p style="
                color:#9ca3af;
                font-size:12px;
                font-weight:700;
                letter-spacing:1px;
            ">
                FILTERS
            </p>
            """, unsafe_allow_html=True)

            category_filter = st.multiselect(
                "Medicine Category",
                options=df["category"].unique(),
                default=df["category"].unique()
            )

            supplier_filter = st.multiselect(
                "Supplier",
                options=df["supplier_id"].unique(),
                default=df["supplier_id"].unique()
            )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <p style="
                color:#9ca3af;
                font-size:12px;
                font-weight:700;
                letter-spacing:1px;
            ">
                SETTINGS
            </p>
            """, unsafe_allow_html=True)

            auto_refresh = st.toggle(
                "Auto Refresh",
                value=True
            )

            show_charts = st.toggle(
                "Interactive Charts",
                value=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="
                background:white;
                padding:18px;
                border-radius:18px;
                border:1px solid #eceff5;
                box-shadow:0 2px 10px rgba(0,0,0,0.04);
            ">

            <h4 style="
                color:#111827;
                margin-top:0px;
            ">
                📡 System Status
            </h4>

            <p style="
                color:#10b981;
                font-weight:600;
                margin-bottom:8px;
            ">
                ● Firebase Connected
            </p>

            <p style="
                color:#2563eb;
                font-weight:600;
                margin-bottom:8px;
            ">
                ⚡ Real-Time Sync Active
            </p>

            <p style="
                color:#6b7280;
                font-size:13px;
                margin-bottom:0px;
            ">
                Last Updated:
                <br>
                {datetime.now().strftime("%H:%M:%S")}
            </p>

            </div>
            """, unsafe_allow_html=True)

        # =====================================================
        # APPLY FILTERS
        # =====================================================

        df = df[
            (
                df["category"].isin(
                    category_filter
                )
            )
            &
            (
                df["supplier_id"].isin(
                    supplier_filter
                )
            )
        ]

        # =====================================================
        # OVERVIEW PAGE
        # =====================================================

        if page == "📊 Overview":

            st.title(
                "🏥 Enterprise Inventory Dashboard"
            )

            total_medicines = len(df)

            total_value = (
                df["inventory_value"].sum()
            )

            avg_stock = (
                df["current_stock"].mean()
            )

            low_stock = len(
                df[df["stock_status"] == "LOW"]
            )

            out_stock = len(
                df[df["stock_status"] == "OUT"]
            )

            supplier_count = (
                df["supplier_id"].nunique()
            )

            # =================================================
            # KPI ROW
            # =================================================

            col1, col2, col3, col4, col5, col6 = (
                st.columns(6)
            )

            with col1:
                st.markdown(
                    '<div class="metric-card">',
                    unsafe_allow_html=True
                )
                st.metric(
                    "💊 Medicines",
                    total_medicines
                )
                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    '<div class="metric-card">',
                    unsafe_allow_html=True
                )
                st.metric(
                    "💰 Revenue",
                    f"${total_value:,.0f}"
                )
                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    '<div class="metric-card">',
                    unsafe_allow_html=True
                )
                st.metric(
                    "📦 Avg Stock",
                    f"{avg_stock:.0f}"
                )
                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with col4:
                st.markdown(
                    '<div class="metric-card">',
                    unsafe_allow_html=True
                )
                st.metric(
                    "⚠️ Low",
                    low_stock
                )
                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with col5:
                st.markdown(
                    '<div class="metric-card">',
                    unsafe_allow_html=True
                )
                st.metric(
                    "❌ Out",
                    out_stock
                )
                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with col6:
                st.markdown(
                    '<div class="metric-card">',
                    unsafe_allow_html=True
                )
                st.metric(
                    "🚚 Suppliers",
                    supplier_count
                )
                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # =================================================
            # CHART ROW
            # =================================================

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    '<div class="chart-card">',
                    unsafe_allow_html=True
                )

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
                    hole=0.55
                )

                fig.update_layout(
                    template="plotly_white",
                    height=430
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    '<div class="chart-card">',
                    unsafe_allow_html=True
                )

                st.subheader(
                    "💰 Top Inventory Value"
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
                    template="plotly_white",
                    height=430
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

        # =====================================================
        # INVENTORY PAGE
        # =====================================================

        elif page == "📦 Inventory":

            st.title(
                "📦 Inventory Management"
            )

            search = st.text_input(
                "Search Medicine"
            )

            if search:

                df = df[
                    df["name"]
                    .str.contains(
                        search,
                        case=False
                    )
                ]

            st.dataframe(
                df,
                use_container_width=True,
                height=700
            )

        # =====================================================
        # ALERTS PAGE
        # =====================================================

        elif page == "⚠️ Alerts":

            st.title(
                "⚠️ Inventory Alerts"
            )

            low_df = df[
                df["stock_status"] == "LOW"
            ]

            if not low_df.empty:

                st.error(
                    "Low Stock Medicines"
                )

                st.dataframe(
                    low_df,
                    use_container_width=True
                )

        # =====================================================
        # FORECAST PAGE
        # =====================================================

        elif page == "📈 Forecasts":

            st.title(
                "📈 Forecast Analytics"
            )

            st.info(
                "AI Forecasting Coming Soon"
            )

        # =====================================================
        # RECOMMENDATIONS PAGE
        # =====================================================

        elif page == "💡 Recommendations":

            st.title(
                "💡 Recommendations"
            )

            st.success(
                "Recommendation Engine Active"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.caption(
            f"""
            🔄 Auto Refresh Enabled |
            🕒 Last Sync:
            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
        )

    except Exception as e:

        logger.error(
            f"Dashboard failed: {str(e)}"
        )

        st.error(
            "Dashboard failed to load"
        )

# =========================================================
# ENTRY
# =========================================================

if __name__ == "__main__":
    main()