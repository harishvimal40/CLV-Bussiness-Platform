"""
CLV Prediction Module
Loads trained model and generates predictions for new/existing customers
"""

import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'clv_models' / 'best_model.pkl'
SCALER_PATH = BASE_DIR / 'models' / 'scaler_standard.pkl'
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'customer_features_normalized.csv'

class CLVPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        
    def load_resources(self):
        """Load model and scaler"""
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Model not found. Run training first.")
        
        print("Loading model and scaler...")
        self.model = joblib.load(MODEL_PATH)
        # scaler loading can be added if we need to process raw input
        # self.scaler = joblib.load(SCALER_PATH) 

    def predict_all(self):
        """Generate predictions for all customers in the processed dataset"""
        df = pd.read_csv(DATA_PATH)
        
        # Select same features used in training (excluding ID, target, non-numeric)
        features = [col for col in df.columns if col not in ['customer_id', 'monetary', 'gender', 'age_group']]
        
        X = df[features]
        predictions = self.model.predict(X)
        
        df['predicted_clv'] = predictions
        
        # Save predictions
        output_path = BASE_DIR / 'data' / 'processed' / 'clv_predictions.csv'
        df[['customer_id', 'monetary', 'predicted_clv']].to_csv(output_path, index=False)
        print(f"Predictions saved to {output_path}")
        
        return df[['customer_id', 'monetary', 'predicted_clv']].head()

if __name__ == "__main__":
    predictor = CLVPredictor()
    predictor.load_resources()
    print(predictor.predict_all())
