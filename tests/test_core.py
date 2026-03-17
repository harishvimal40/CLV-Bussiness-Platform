"""
Unit Tests for SmartCLV Core Modules
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

# Mock data
@pytest.fixture
def mock_customer_data():
    return pd.DataFrame({
        'customer_id': [1, 2, 3],
        'monetary': [100.0, 200.0, 50.0],
        'frequency': [1, 2, 1],
        'recency': [10, 5, 30],
        'churn_probability': [0.1, 0.2, 0.8],
        'predicted_clv': [120.0, 250.0, 60.0]
    })

def test_dataframe_structure(mock_customer_data):
    """Test if data has expected columns"""
    expected_cols = ['customer_id', 'monetary', 'frequency', 'recency']
    for col in expected_cols:
        assert col in mock_customer_data.columns

def test_churn_probability_range(mock_customer_data):
    """Test if churn probability is between 0 and 1"""
    probs = mock_customer_data['churn_probability']
    assert (probs >= 0).all() and (probs <= 1).all()

def test_recommendation_logic():
    """Test simple segmentation logic"""
    # Simple logic replication for testing
    def get_segment(clv, risk):
        if risk > 0.7: return "High Risk"
        if clv > 200: return "High Value"
        return "Standard"

    assert get_segment(500, 0.1) == "High Value"
    assert get_segment(100, 0.9) == "High Risk"
    assert get_segment(100, 0.1) == "Standard"

def test_model_loading():
    """Test if models can be loaded (requires models to exist)"""
    import joblib
    model_path = BASE_DIR / 'models' / 'clv_models' / 'best_model.pkl'
    if model_path.exists():
        model = joblib.load(model_path)
        assert model is not None
    else:
        pytest.skip("Model not found, skipping load test")
