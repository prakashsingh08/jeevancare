"""
Constants Module
Centralized constants and enumerations for the application
"""

# ============================================
# ALERT SEVERITY LEVELS
# ============================================
ALERT_SEVERITY_CRITICAL = 'CRITICAL'
ALERT_SEVERITY_WARNING = 'WARNING'
ALERT_SEVERITY_INFO = 'INFO'

ALERT_SEVERITIES = [
    ALERT_SEVERITY_CRITICAL,
    ALERT_SEVERITY_WARNING,
    ALERT_SEVERITY_INFO
]

# ============================================
# STOCK STATUS
# ============================================
STOCK_STATUS_CRITICAL = 'CRITICAL'      # Stock below critical threshold
STOCK_STATUS_LOW = 'LOW'                # Stock between critical and warning
STOCK_STATUS_NORMAL = 'NORMAL'          # Stock between min and max
STOCK_STATUS_HIGH = 'HIGH'              # Stock above max threshold
STOCK_STATUS_OUT = 'OUT_OF_STOCK'       # No stock available

STOCK_STATUSES = [
    STOCK_STATUS_CRITICAL,
    STOCK_STATUS_LOW,
    STOCK_STATUS_NORMAL,
    STOCK_STATUS_HIGH,
    STOCK_STATUS_OUT
]

# ============================================
# MEDICINE CATEGORIES
# ============================================
CATEGORIES = [
    'Analgesic',
    'Antibiotic',
    'Antiviral',
    'Antihistamine',
    'Antiseptic',
    'Cardiac',
    'Dermatological',
    'Digestive',
    'Respiratory',
    'Vitamin',
    'Other'
]

# ============================================
# FORECASTING METHODS
# ============================================
FORECASTING_METHOD_MOVING_AVERAGE = 'moving_average'
FORECASTING_METHOD_EXPONENTIAL_SMOOTHING = 'exponential_smoothing'
FORECASTING_METHOD_SEASONAL = 'seasonal'

FORECASTING_METHODS = [
    FORECASTING_METHOD_MOVING_AVERAGE,
    FORECASTING_METHOD_EXPONENTIAL_SMOOTHING,
    FORECASTING_METHOD_SEASONAL
]

# ============================================
# DATA COLUMNS
# ============================================
REQUIRED_COLUMNS = [
    'medicine_id',
    'name',
    'category',
    'current_stock',
    'min_stock',
    'max_stock',
    'unit_price',
    'expiry_date',
    'supplier_id'
]

# ============================================
# NUMERIC RANGES
# ============================================
MIN_PRICE = 0.01
MAX_PRICE = 10000.00
MIN_STOCK = 0
MAX_STOCK = 100000

# ============================================
# TIME CONSTANTS
# ============================================
SECONDS_PER_DAY = 86400
DAYS_PER_WEEK = 7
DAYS_PER_MONTH = 30
DAYS_PER_YEAR = 365

# ============================================
# CACHE DURATIONS (in seconds)
# ============================================
CACHE_DURATION_MEDICINES = 300          # 5 minutes
CACHE_DURATION_FORECASTS = 600          # 10 minutes
CACHE_DURATION_ALERTS = 120             # 2 minutes

# ============================================
# API ENDPOINTS
# ============================================
FIREBASE_MEDICINES_PATH = 'medicines'
FIREBASE_ALERTS_PATH = 'alerts'
FIREBASE_FORECASTS_PATH = 'forecasts'
FIREBASE_SUPPLIERS_PATH = 'suppliers'
FIREBASE_LOGS_PATH = 'logs'

# ============================================
# DEFAULT VALUES
# ============================================
DEFAULT_LEAD_TIME_DAYS = 3
DEFAULT_SAFETY_STOCK_PERCENTAGE = 0.2
DEFAULT_REORDER_QUANTITY_PERCENTAGE = 0.5
