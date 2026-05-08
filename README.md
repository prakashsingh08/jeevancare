# JeevanCare Analytics Platform 2.0

## 🏥 Medicine Inventory Optimization & Demand Forecasting System

A comprehensive data analytics and decision support system designed for healthcare institutions to optimize medicine inventory management, forecast demand accurately, and make data-driven decisions.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Local Setup Guide](#local-setup-guide)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [Scripts & Components Guide](#scripts--components-guide)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

JeevanCare Analytics Platform is a modern, cloud-based solution that helps healthcare institutions:

- **Monitor** real-time inventory levels of medicines
- **Forecast** future demand using statistical models
- **Identify** low stock, overstock, and expiry risks
- **Generate** actionable alerts and recommendations
- **Optimize** inventory management and reduce waste

### Key Capabilities:

✅ Real-time inventory monitoring with Firebase  
✅ Demand forecasting with multiple algorithms  
✅ Automated alert system for critical situations  
✅ Interactive Streamlit dashboards  
✅ Data-driven recommendations  
✅ Comprehensive logging and audit trails  

---

## ✨ Features

### 1. **Inventory Management**
   - Track current stock levels
   - Monitor minimum and maximum thresholds
   - Identify overstock and understock situations
   - Calculate inventory turnover ratios

### 2. **Demand Forecasting**
   - Moving average forecasting
   - Exponential smoothing
   - Linear trend analysis
   - Confidence intervals for forecasts

### 3. **Alert System**
   - Critical stock alerts
   - Expiry warnings
   - Overstock notifications
   - Severity-based alert categorization

### 4. **Analytics Dashboard**
   - KPI cards with real-time metrics
   - Interactive charts and visualizations
   - Inventory status overview
   - Supplier performance analysis

### 5. **Recommendations Engine**
   - Purchase recommendations
   - Supplier optimization suggestions
   - Cost optimization insights
   - Demand pattern analysis

---

## 📁 Project Structure

```
jeevancare-analytics2/
│
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── .env.example                     # Example environment variables
├── .gitignore                       # Git configuration
│
├── core/                            # Core utilities
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── constants.py                 # Application constants
│   └── logger.py                    # Logging setup
│
├── services/                        # External service integrations
│   ├── __init__.py
│   ├── firebase_service.py          # Firebase operations
│   └── database_service.py          # Local database operations
│
├── pipelines/                       # Data processing pipelines
│   ├── __init__.py
│   ├── ingestion_pipeline.py        # Data loading & validation
│   ├── processing_pipeline.py       # Data transformation
│   └── update_pipeline.py           # Real-time updates
│
├── models/                          # ML models & analytics
│   ├── __init__.py
│   ├── features.py                  # Feature engineering
│   └── forecasting.py               # Forecasting models
│
├── domain/                          # Business logic
│   ├── __init__.py
│   ├── inventory.py                 # Inventory management logic
│   ├── alerts.py                    # Alert generation
│   └── recommendations.py           # Recommendation engine
│
├── app/                             # Streamlit dashboard
│   ├── __init__.py
│   ├── dashboard_app.py             # Main dashboard
│   ├── admin_app.py                 # Admin interface
│   └── components/
│       ├── __init__.py
│       ├── charts.py                # Chart components
│       ├── kpi_cards.py             # KPI components
│       └── tables.py                # Table components
│
├── scripts/                         # Utility scripts
│   ├── upload_to_firebase.py        # Firebase data uploader
│   └── simulate_updates.py          # Real-time data simulator
│
├── data/                            # Data storage
│   ├── raw/                         # Raw data (not in Git)
│   └── processed/                   # Processed data (not in Git)
│
├── logs/                            # Application logs (not in Git)
│
└── config/                          # Configuration files
    └── serviceAccountKey.json       # Firebase credentials (not in Git)
```

---

## ✅ Prerequisites

### System Requirements
- **Python**: 3.9 or higher
- **pip**: Latest version
- **Git**: Version control
- **8GB RAM** minimum
- **2GB** free disk space

### Required Accounts
- **Firebase Project**: Free tier available at [firebase.google.com](https://firebase.google.com)
- **Kaggle Dataset**: Medical inventory data (optional)

### Verify Prerequisites
```bash
python --version       # Should be 3.9+
pip --version         # Should be 20.0+
git --version         # Should be 2.0+
```

---

## 🚀 Local Setup Guide

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/jeevancare-analytics2.git
cd jeevancare-analytics2
```

### Step 2: Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Create Required Directories
```bash
mkdir -p data/raw data/processed logs config
```

### Step 6: Setup Firebase Configuration

#### 6.1 Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click "Create a new project"
3. Name it: `jeevancare-analytics-dev`
4. Accept terms and create

#### 6.2 Enable Firebase Services
1. **Realtime Database**
   - Go to Realtime Database → Create Database
   - Start in Test Mode
   - Copy database URL

2. **Storage** (optional)
   - Go to Storage → Create Bucket
   - Copy bucket name

#### 6.3 Generate Service Account Key
1. Go to Project Settings (⚙️ gear icon)
2. Click **Service Accounts** tab
3. Click **Generate New Private Key**
4. Save JSON file to `config/serviceAccountKey.json`

### Step 7: Configure Environment Variables
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your values
nano .env  # or use your editor
```

Update these values in `.env`:
```
FIREBASE_KEY_PATH=config/serviceAccountKey.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
```

### Step 8: Prepare Sample Data
Create `data/raw/medicine_inventory.csv`:

```csv
medicine_id,name,category,current_stock,min_stock,max_stock,unit_price,expiry_date,supplier_id
1,Aspirin,Analgesic,500,100,1000,5.99,2026-12-31,SUP001
2,Paracetamol,Analgesic,300,50,600,3.50,2026-11-30,SUP002
3,Amoxicillin,Antibiotic,200,30,400,2.80,2026-10-15,SUP001
4,Ibuprofen,Analgesic,450,80,900,4.25,2026-09-20,SUP003
5,Vitamin C,Vitamin,600,100,1200,1.50,2027-01-30,SUP002
```

### Step 9: Verify Installation
```bash
python -c "import pandas; import streamlit; import firebase_admin; print('✓ All dependencies installed')"
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```plaintext
# Firebase
FIREBASE_KEY_PATH=config/serviceAccountKey.json
FIREBASE_DATABASE_URL=https://jeevancare-analytics-dev.firebaseio.com
FIREBASE_STORAGE_BUCKET=jeevancare-analytics-dev.appspot.com

# Application
APP_ENV=development
DEBUG=True
APP_PORT=8501

# Data Paths
DATA_RAW_PATH=data/raw/
DATA_PROCESSED_PATH=data/processed/

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/jeevancare.log

# Forecasting
FORECAST_PERIODS=30
MOVING_AVERAGE_WINDOW=7

# Alerts
CRITICAL_STOCK_THRESHOLD=10
WARNING_STOCK_THRESHOLD=50
EXPIRY_DAYS_WARNING=30
```

### Important Notes:
- **Never commit `.env`** to version control
- Use **relative paths** for file paths
- **Sample URLs** provided; replace with actual values
- Keep **Firebase key secure** (use .gitignore)

---

## ▶️ Running the Application

### Complete Workflow

#### Terminal 1: Data Preparation
```bash
# Activate virtual environment
source venv/bin/activate

# Test configuration
python -c "from core.config import load_config; config = load_config(); print('✓ Config loaded')"

# Test data ingestion
python -c "
from pipelines.ingestion_pipeline import ingest_data
data = ingest_data('data/raw/medicine_inventory.csv')
print(f'✓ Loaded {len(data)} records')
"
```

#### Terminal 1: Upload to Firebase
```bash
python scripts/upload_to_firebase.py

# Expected output:
# ✓ Firebase connection established
# ✓ Uploading medicines...
# ✓ Successfully uploaded X medicines to Firebase
```

#### Terminal 2: Start Data Simulator
```bash
# Open new terminal and activate venv
source venv/bin/activate

python scripts/simulate_updates.py --interval 10

# Expected output:
# ✓ Data simulator initialized
# Update #1: 2026-05-05 10:30:45 - Updated medicine_id=1
# Update #2: 2026-05-05 10:30:55 - Updated medicine_id=3
# (Continues indefinitely until Ctrl+C)
```

#### Terminal 3: Launch Dashboard
```bash
# Open new terminal and activate venv
source venv/bin/activate

streamlit run main.py

# Expected output:
# You can now view your Streamlit app in your browser
# Local URL: http://localhost:8501
```

#### Access Dashboard
Open browser and go to: `http://localhost:8501`

You should see:
- 📊 Real-time inventory overview
- 📦 Inventory management view
- ⚠️ Active alerts
- 📈 Demand forecasts
- 💡 Recommendations

---

## 📜 Scripts & Components Guide

### Scripts

#### 1. `upload_to_firebase.py`
**Purpose**: Upload processed data to Firebase

```bash
# Basic usage
python scripts/upload_to_firebase.py

# With specific file
python scripts/upload_to_firebase.py --file data/processed/medicines.csv

# Force re-upload
python scripts/upload_to_firebase.py --force
```

**Output**: Console logs showing upload progress

#### 2. `simulate_updates.py`
**Purpose**: Simulate real-time inventory changes

```bash
# Run indefinitely
python scripts/simulate_updates.py --interval 10

# Run specific iterations
python scripts/simulate_updates.py --iterations 100 --interval 5

# Stop anytime with Ctrl+C
```

**What it does**:
- Randomly changes stock levels
- Updates medicines in Firebase
- Useful for testing alerts

### Core Modules

#### `core/config.py`
- Loads environment variables
- Validates configuration
- Creates required directories
- Manages all app settings

#### `core/logger.py`
- Centralized logging
- Console and file output
- Log rotation
- Debug support

#### `core/constants.py`
- Application constants
- Alert severities
- Stock statuses
- Firebase paths

### Services

#### `services/firebase_service.py`
- Firebase database operations
- Real-time listeners
- Batch writes
- Connection management

#### `services/database_service.py`
- Local CSV storage
- Data caching
- Quick access
- JSON export

### Pipelines

#### `pipelines/ingestion_pipeline.py`
- Load raw CSV data
- Validate schema
- Handle missing values
- Remove duplicates

#### `pipelines/processing_pipeline.py`
- Normalize prices
- Calculate inventory values
- Determine stock status
- Calculate days to expiry

#### `pipelines/update_pipeline.py`
- Real-time sync
- Alert triggering
- Data updates
- Continuous monitoring

### Models

#### `models/features.py`
- Moving averages
- Trend analysis
- Volatility calculations
- Lag features
- Feature normalization

#### `models/forecasting.py`
- Moving average forecast
- Exponential smoothing
- Linear trend analysis
- Accuracy metrics
- Confidence intervals

### Domain Logic

#### `domain/inventory.py`
- Reorder point calculation
- Stock status determination
- Inventory turnover
- Overstock/understock detection

#### `domain/alerts.py`
- Low stock alerts
- Expiry warnings
- Overstock notifications
- Alert resolution

#### `domain/recommendations.py`
- Purchase recommendations
- Supplier optimization
- Cost savings suggestions
- Demand insights

### Dashboard Components

#### `app/components/charts.py`
- Line charts (trends)
- Bar charts (comparisons)
- Pie charts (distributions)
- Scatter plots
- Heatmaps
- Histograms

#### `app/components/kpi_cards.py`
- KPI displays
- Metric cards
- Status indicators
- Trend indicators

#### `app/components/tables.py`
- Data table formatting
- Filtering
- Sorting
- Pagination

---

## 🔍 Troubleshooting

### Issue 1: Firebase Connection Error
**Error**: `credentials.not_found` or connection timeout

**Solution**:
```bash
# Check Firebase key exists
ls -la config/serviceAccountKey.json

# Verify path in .env
grep FIREBASE_KEY_PATH .env

# Test connection
python -c "
from services.firebase_service import get_firebase_service
fb = get_firebase_service()
print('✓ Connected')
"
```

### Issue 2: Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
# Reinstall requirements
pip install -r requirements.txt

# Or specific package
pip install pandas==2.0.3
```

### Issue 3: Port Already in Use
**Error**: `Address already in use (port 8501)`

**Solution**:
```bash
# Use different port
streamlit run main.py --server.port 8502

# Or kill existing process
lsof -ti:8501 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8501   # Windows
```

### Issue 4: Data File Not Found
**Error**: `FileNotFoundError: medicine_inventory.csv`

**Solution**:
```bash
# Create sample file
mkdir -p data/raw

# Add CSV file to data/raw/
# Ensure columns match: medicine_id, name, category, current_stock, ...
```

### Issue 5: Streamlit Not Found
**Error**: `streamlit: command not found`

**Solution**:
```bash
# Check venv is activated
source venv/bin/activate  # Should show (venv) prefix

# Reinstall Streamlit
pip install streamlit==1.28.1
```

---

## 📊 Sample Data Format

### Input CSV (data/raw/medicine_inventory.csv)
```csv
medicine_id,name,category,current_stock,min_stock,max_stock,unit_price,expiry_date,supplier_id
1,Aspirin,Analgesic,500,100,1000,5.99,2026-12-31,SUP001
2,Paracetamol,Analgesic,300,50,600,3.50,2026-11-30,SUP002
3,Amoxicillin,Antibiotic,200,30,400,2.80,2026-10-15,SUP001
```

### Firebase Structure
```json
{
  "medicines": {
    "medicine_1": {
      "name": "Aspirin",
      "category": "Analgesic",
      "current_stock": 450,
      "stock_status": "normal",
      "inventory_value": 2695.50,
      "updated_at": "2026-05-05T10:30:45Z"
    }
  },
  "alerts": {...},
  "forecasts": {...}
}
```

---

## 🎓 Quick Start Commands

```bash
# 1. Clone and setup
git clone <repo>
cd jeevancare-analytics2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with Firebase credentials

# 3. Prepare data
mkdir -p data/raw
# Add medicine_inventory.csv to data/raw/

# 4. Upload to Firebase
python scripts/upload_to_firebase.py

# 5. Start simulator (Terminal 2)
python scripts/simulate_updates.py --interval 10

# 6. Launch dashboard (Terminal 3)
streamlit run main.py

# 7. Open browser
# Navigate to http://localhost:8501
```

---

## 📞 Support & Contribution

For issues or contributions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review logs: `tail -f logs/jeevancare.log`
3. Check Firebase console for connectivity
4. Verify data format in CSV

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🙏 Acknowledgments

- **Streamlit** for dashboard framework
- **Firebase** for cloud infrastructure
- **Pandas & NumPy** for data processing
- **Plotly** for interactive visualizations

---

**Last Updated**: May 5, 2026  
**Version**: 2.0.0  
**Status**: ✓ Production Ready
