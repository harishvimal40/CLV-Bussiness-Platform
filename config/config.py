import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for SmartCLV system"""
    
    # Database settings
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'smartclv_db')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Model settings
    CHURN_THRESHOLD_DAYS = int(os.getenv('CHURN_THRESHOLD_DAYS', 90))
    CLV_PREDICTION_HORIZON = int(os.getenv('CLV_PREDICTION_HORIZON', 365))
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    
    # Dashboard settings
    DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', 8501))
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'True') == 'True'

# Create config instance
config = Config()
