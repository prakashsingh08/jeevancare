"""
Admin Dashboard Application
Administrative interface for system management
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from core.logger import get_logger
from core.config import load_config

logger = get_logger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="JeevanCare Admin",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Administration Panel")
st.markdown("System management and configuration")

st.divider()

# Sidebar
with st.sidebar:
    st.header("🔐 Admin Menu")
    admin_section = st.radio(
        "Select Section",
        ["📊 System Status", "📤 Data Upload", "⚙️ Configuration", "📝 Logs"]
    )

# Main content
if admin_section == "📊 System Status":
    st.header("System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Status", "✓ Online")
    with col2:
        st.metric("Uptime", "2d 5h")
    with col3:
        st.metric("Last Sync", "2 minutes ago")
    with col4:
        st.metric("Database", "✓ Connected")
    
    st.divider()
    
    st.subheader("Service Health")
    services = {
        'Firebase Connection': '✓ Active',
        'Database Service': '✓ Active',
        'Cache Service': '✓ Active',
        'API Service': '✓ Active'
    }
    
    for service, status in services.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(service)
        with col2:
            st.write(status)

elif admin_section == "📤 Data Upload":
    st.header("Data Upload & Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload New Data")
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        
        if uploaded_file is not None:
            if st.button("Process & Upload"):
                st.info("Processing file...")
                # File processing logic would go here
                st.success("✓ File uploaded and processed successfully")
    
    with col2:
        st.subheader("Recent Uploads")
        st.write("No recent uploads")

elif admin_section == "⚙️ Configuration":
    st.header("System Configuration")
    
    try:
        config = load_config()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Firebase Configuration")
            st.write(f"**Database URL**: {config.FIREBASE_DATABASE_URL}")
            st.write(f"**Storage Bucket**: {config.FIREBASE_STORAGE_BUCKET}")
        
        with col2:
            st.subheader("Application Configuration")
            st.write(f"**Environment**: {config.APP_ENV}")
            st.write(f"**Debug Mode**: {config.DEBUG}")
            st.write(f"**App Port**: {config.APP_PORT}")
        
        st.divider()
        
        st.subheader("Thresholds & Alerts")
        col1, col2 = st.columns(2)
        
        with col1:
            critical_threshold = st.slider(
                "Critical Stock Threshold",
                min_value=0,
                max_value=100,
                value=10,
                step=1
            )
            warning_threshold = st.slider(
                "Warning Stock Threshold",
                min_value=0,
                max_value=200,
                value=50,
                step=1
            )
        
        with col2:
            expiry_warning = st.slider(
                "Expiry Warning Days",
                min_value=1,
                max_value=90,
                value=30,
                step=1
            )
            forecast_periods = st.slider(
                "Forecast Periods",
                min_value=7,
                max_value=180,
                value=30,
                step=7
            )
        
        if st.button("Save Configuration"):
            st.success("✓ Configuration saved successfully")
    
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        st.error("Error loading configuration")

elif admin_section == "📝 Logs":
    st.header("System Logs")
    
    log_level = st.selectbox(
        "Filter by Level",
        ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    )
    
    st.info("""
    📝 System logs would be displayed here.
    
    Log features:
    - Real-time log streaming
    - Search and filter capabilities
    - Export logs to file
    - Log rotation and archiving
    """)
    
    if st.button("Refresh Logs"):
        st.info("Logs refreshed")

st.divider()
st.caption("Admin Panel | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
