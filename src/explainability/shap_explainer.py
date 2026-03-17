"""
SHAP Explainer Module
Provides interpretability for CLV and Churn models
"""

import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
MODEL_DIR = BASE_DIR / 'models'
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'customer_features_normalized.csv'
IMAGES_DIR = BASE_DIR / 'dashboard' / 'assets' / 'images'

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

class ModelExplainer:
    def __init__(self):
        self.clv_model = None
        self.churn_model = None
        self.X = None
        self.feature_names = None
        
    def load_resources(self):
        # Load models
        print("Loading models...")
        self.clv_model = joblib.load(MODEL_DIR / 'clv_models' / 'best_model.pkl')
        self.churn_model = joblib.load(MODEL_DIR / 'churn_models' / 'best_churn_model.pkl')
        
        # Load data (sample for speed - take 500 samples)
        print("Loading data...")
        df = pd.read_csv(DATA_PATH)
        # Match features used in model_training/trainer.py
        # Trainer drops: ['customer_id', 'monetary', 'gender', 'age_group']
        drop_cols = ['customer_id', 'monetary', 'gender', 'age_group']
        # Note: 'recency' WAS used in training (trainer.py line 54 doesn't include it in drop list)
        
        feature_cols = [c for c in df.columns if c not in drop_cols]
        self.X = df[feature_cols].sample(500, random_state=42)
        self.feature_names = self.X.columns.tolist()
        
    def generate_clv_explanations(self):
        print("Generating CLV Global Explanations (XGBoost)...")
        # XGBoost TreeExplainer is efficient
        explainer = shap.TreeExplainer(self.clv_model)
        shap_values = explainer.shap_values(self.X)
        
        # Summary Plot
        plt.figure()
        shap.summary_plot(shap_values, self.X, show=False)
        output_path = IMAGES_DIR / 'clv_feature_importance.png'
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        print(f"Saved CLV summary plot to {output_path}")

    def generate_churn_explanations(self):
        print("Generating Churn Global Explanations (Random Forest)...")
        # Random Forest might be slower with TreeExplainer on large datasets, 
        # so we used a sample of 500 above.
        explainer = shap.TreeExplainer(self.churn_model)
        
        # RF Classifier returns list of shap values (one for each class). We want Class 1 (Churn).
        shap_values = explainer.shap_values(self.X)
        
        if isinstance(shap_values, list):
            # For binary classification, shap_values[1] entails the "positive" class (Churn)
            churn_shap_values = shap_values[1]
        else:
            churn_shap_values = shap_values
            
        # Summary Plot
        plt.figure()
        shap.summary_plot(churn_shap_values, self.X, show=False)
        output_path = IMAGES_DIR / 'churn_feature_importance.png'
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        print(f"Saved Churn summary plot to {output_path}")

if __name__ == "__main__":
    explainer = ModelExplainer()
    explainer.load_resources()
    explainer.generate_clv_explanations()
    explainer.generate_churn_explanations()
