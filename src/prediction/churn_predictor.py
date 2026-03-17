"""
Churn Risk Predictor
Generates churn probability scores for customers
"""

import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'churn_models' / 'best_churn_model.pkl'
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'customer_features_normalized.csv'

class ChurnPredictor:
    def __init__(self):
        self.model = None
        
    def load_model(self):
        """Load trained churn model"""
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Churn model not found. Run training first.")
        print("Loading churn model...")
        self.model = joblib.load(MODEL_PATH)

    def predict_churn_risk(self):
        """Generate churn probabilities"""
        df = pd.read_csv(DATA_PATH)
        
        # Use same features as training
        drop_cols = ['customer_id', 'monetary', 'recency', 'gender', 'age_group']
        features = [col for col in df.columns if col not in drop_cols]
        
        X = df[features]
        probabilities = self.model.predict_proba(X)[:, 1] # Probability of Churn (Class 1)
        
        df['churn_probability'] = probabilities
        df['churn_risk_level'] = pd.cut(
            df['churn_probability'], 
            bins=[0, 0.3, 0.7, 1.0], 
            labels=['Low', 'Medium', 'High'],
            include_lowest=True
        )
        
        # Save results
        output_path = BASE_DIR / 'data' / 'processed' / 'churn_predictions.csv'
        df[['customer_id', 'churn_probability', 'churn_risk_level']].to_csv(output_path, index=False)
        print(f"Churn predictions saved to {output_path}")
        
        # Check distribution
        print("\nRisk Level Distribution:")
        print(df['churn_risk_level'].value_counts(normalize=True))
        
        return df[['customer_id', 'churn_probability', 'churn_risk_level']].head()

if __name__ == "__main__":
    predictor = ChurnPredictor()
    predictor.load_model()
    predictor.predict_churn_risk()
