# JeevanCare Analytics 2.0 - Quick Start Guide

## ⚡ 5-Minute Setup

### Prerequisites Check
```bash
python --version    # Should be 3.9+
pip --version      # Should be 20+
```

### 1. Clone & Setup (2 minutes)
```bash
git clone https://github.com/yourusername/jeevancare-analytics2.git
cd jeevancare-analytics2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Firebase Setup (2 minutes)
```bash
# Download Firebase credentials from Firebase Console
# Save to: config/serviceAccountKey.json

# Copy environment template
cp .env.example .env

# Edit .env with your Firebase credentials
nano .env
```

**Required .env values:**
```
FIREBASE_KEY_PATH=config/serviceAccountKey.json
FIREBASE_DATABASE_URL=https://YOUR_PROJECT.firebaseio.com
FIREBASE_STORAGE_BUCKET=YOUR_PROJECT.appspot.com
```

### 3. Run Application (1 minute)

**Terminal 1: Upload Data**
```bash
python scripts/upload_to_firebase.py
```

**Terminal 2: Start Simulator**
```bash
python scripts/simulate_updates.py --interval 10
```

**Terminal 3: Launch Dashboard**
```bash
streamlit run main.py
```

### 4. Access Dashboard
Open browser: `http://localhost:8501`

---

## 📊 Project Features at a Glance

| Feature | Location | Purpose |
|---------|----------|---------|
| **Dashboard** | `app/dashboard_app.py` | Real-time inventory visualization |
| **Alerts** | `domain/alerts.py` | Alert generation & management |
| **Forecasting** | `models/forecasting.py` | Demand prediction |
| **Inventory Logic** | `domain/inventory.py` | Stock calculations |
| **Firebase Sync** | `services/firebase_service.py` | Cloud database |
| **Data Upload** | `scripts/upload_to_firebase.py` | Push data to cloud |
| **Simulator** | `scripts/simulate_updates.py` | Test real-time updates |

---

## 🔑 Key Modules Overview

### Core (`core/`)
- **config.py**: Application configuration
- **logger.py**: Centralized logging
- **constants.py**: App constants

### Services (`services/`)
- **firebase_service.py**: Firebase operations
- **database_service.py**: Local data storage

### Pipelines (`pipelines/`)
- **ingestion_pipeline.py**: Load & validate data
- **processing_pipeline.py**: Transform data
- **update_pipeline.py**: Real-time sync

### Models (`models/`)
- **features.py**: Feature engineering
- **forecasting.py**: Demand forecasting

### Domain (`domain/`)
- **inventory.py**: Inventory management
- **alerts.py**: Alert system
- **recommendations.py**: Recommendations engine

### App (`app/`)
- **dashboard_app.py**: Main dashboard
- **admin_app.py**: Admin interface
- **components/**: Reusable UI components

### Scripts (`scripts/`)
- **upload_to_firebase.py**: Data uploader
- **simulate_updates.py**: Data simulator

---

## 📁 Directory Structure

```
jeevancare-analytics2/
├── main.py                      ← Application entry point
├── requirements.txt             ← Dependencies
├── README.md                    ← Full documentation
├── QUICKSTART.md               ← This file
├── .env.example                ← Config template
│
├── core/                        ← Core utilities
├── services/                    ← External integrations
├── pipelines/                   ← Data processing
├── models/                      ← Analytics models
├── domain/                      ← Business logic
├── app/                         ← Dashboard & UI
├── scripts/                     ← Utility scripts
│
├── data/
│   ├── raw/                     ← Input CSV files
│   └── processed/               ← Processed data
├── logs/                        ← Application logs
├── config/                      ← Firebase credentials
└── tests/                       ← Test files
```

---

## 🚀 Common Tasks

### Upload Sample Data to Firebase
```bash
python scripts/upload_to_firebase.py
```

### Run Real-time Simulator
```bash
python scripts/simulate_updates.py --interval 5
```

### Check Logs
```bash
tail -f logs/jeevancare.log
```

### Test Configuration
```bash
python -c "from core.config import load_config; load_config(); print('✓ Config OK')"
```

### Test Firebase Connection
```bash
python -c "
from services.firebase_service import get_firebase_service
fb = get_firebase_service()
print('✓ Firebase Connected')
"
```

---

## ⚙️ Configuration Reference

### Environment Variables

```plaintext
# Firebase
FIREBASE_KEY_PATH=config/serviceAccountKey.json
FIREBASE_DATABASE_URL=https://jeevancare-analytics-dev.firebaseio.com
FIREBASE_STORAGE_BUCKET=jeevancare-analytics-dev.appspot.com

# Application
APP_ENV=development
DEBUG=True
APP_PORT=8501

# Data
DATA_RAW_PATH=data/raw/
DATA_PROCESSED_PATH=data/processed/

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/jeevancare.log

# Alerts
CRITICAL_STOCK_THRESHOLD=10
WARNING_STOCK_THRESHOLD=50
EXPIRY_DAYS_WARNING=30

# Forecasting
FORECAST_PERIODS=30
MOVING_AVERAGE_WINDOW=7
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Firebase connection error | Check `config/serviceAccountKey.json` exists |
| Port 8501 in use | Use `streamlit run main.py --server.port 8502` |
| Missing dependencies | Run `pip install -r requirements.txt` |
| Data file not found | Create CSV in `data/raw/medicine_inventory.csv` |
| Virtual env not activated | Run `source venv/bin/activate` |

---

## 📊 Dashboard Pages

1. **📊 Overview**: Real-time inventory KPIs and charts
2. **📦 Inventory**: Detailed medicine list with filters
3. **⚠️ Alerts**: Active alerts and issues
4. **📈 Forecasts**: Demand predictions
5. **💡 Recommendations**: Purchase and optimization suggestions

---

## 🎯 Next Steps

1. ✅ Complete setup (5 minutes)
2. ✅ Launch dashboard
3. 📖 Read full README.md for detailed documentation
4. 🔧 Customize configuration in .env
5. 📊 Upload your actual data
6. 🚀 Deploy to production

---

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review logs: `logs/jeevancare.log`
- Check Firebase console for connectivity
- Verify .env configuration

---

**Happy Analyzing! 🏥📊**
