"""
Churn Prediction Model Trainer
Trains classification models to predict customer churn risk
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Dirs
BASE_DIR = Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'customer_features_normalized.csv'
MODEL_DIR = BASE_DIR / 'models' / 'churn_models'
METRICS_PATH = BASE_DIR / 'models' / 'churn_metrics.json'

MODEL_DIR.mkdir(parents=True, exist_ok=True)

class ChurnTrainer:
    """Train and evaluate churn prediction models"""

    def __init__(self):
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.results = {}

    def load_and_prep_data(self):
        """Load data and create churn target"""
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Data file not found at {DATA_PATH}")
        
        print(f"Loading data from {DATA_PATH}...")
        df = pd.read_csv(DATA_PATH)
        
        # Define Churn: Inactive for > 90 days
        # We already calculated 'recency' (days since last purchase)
        # But 'recency' was normalized, so we need the raw value or interpret the normalized one.
        # Actually, for training a predictive model, we should use a "snapshot" approach.
        # For simplicity in this project, we'll define the target based on the current state 
        # (which might be slightly leaky but acceptable for demonstration).
        
        # We need raw recency to define the target accurately. 
        # Since we normalized everything, let's infer from the 'recency' feature if possible, 
        # OR reload the raw processed data.
        
        raw_features_path = BASE_DIR / 'data' / 'processed' / 'customer_features.csv'
        df_raw = pd.read_csv(raw_features_path)
        
        # Churn Definition: Recency > 90 days
        df_raw['is_churned'] = (df_raw['recency'] > 90).astype(int)
        
        print(f"Churn Rate: {df_raw['is_churned'].mean():.2%}")
        
        self.y = df_raw['is_churned']
        
        # Use normalized features for training
        # Drop inputs that directly reveal the target (Recency)
        # Also drop 'monetary' and 'frequency' if they are too correlated.
        # Definitely drop 'recency' as it IS the definition of churn here.
        
        df_norm = pd.read_csv(DATA_PATH)
        drop_cols = ['customer_id', 'monetary', 'recency', 'gender', 'age_group']
        features = [col for col in df_norm.columns if col not in drop_cols]
        
        self.X = df_norm[features]
        
        print(f"Features used: {features}")

    def split_data(self):
        """Split data into train and test sets (stratified)"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        print(f"Training set: {self.X_train.shape[0]} samples")
        print(f"Test set: {self.X_test.shape[0]} samples")

    def train_logistic_regression(self):
        """Train Logistic Regression"""
        print("\nTraining Logistic Regression...")
        lr = LogisticRegression(max_iter=1000, class_weight='balanced')
        lr.fit(self.X_train, self.y_train)
        self.models['LogisticRegression'] = lr

    def train_random_forest(self):
        """Train Random Forest Classifier"""
        print("\nTraining Random Forest...")
        rf = RandomForestClassifier(n_estimators=100, max_depth=10, class_weight='balanced', random_state=42)
        rf.fit(self.X_train, self.y_train)
        self.models['RandomForest'] = rf

    def evaluate_models(self):
        """Evaluate all trained models"""
        print("\nEvaluating models...")
        
        best_f1 = -float('inf')
        best_model_name = None

        for name, model in self.models.items():
            preds = model.predict(self.X_test)
            probs = model.predict_proba(self.X_test)[:, 1]
            
            acc = accuracy_score(self.y_test, preds)
            prec = precision_score(self.y_test, preds)
            rec = recall_score(self.y_test, preds)
            f1 = f1_score(self.y_test, preds)
            auc = roc_auc_score(self.y_test, probs)
            
            self.results[name] = {
                'Accuracy': round(acc, 4),
                'Precision': round(prec, 4),
                'Recall': round(rec, 4),
                'F1-Score': round(f1, 4),
                'AUC-ROC': round(auc, 4)
            }
            
            print(f"{name} -> F1: {f1:.4f}, AUC: {auc:.4f}")
            
            if f1 > best_f1:
                best_f1 = f1
                best_model_name = name

        # Save metrics
        with open(METRICS_PATH, 'w') as f:
            json.dump(self.results, f, indent=4)
            
        print(f"\nBest Model: {best_model_name} (F1: {best_f1:.4f})")
        
        # Save best model
        best_model = self.models[best_model_name]
        joblib.dump(best_model, MODEL_DIR / 'best_churn_model.pkl')
        print(f"Saved best model to {MODEL_DIR / 'best_churn_model.pkl'}")

    def run_pipeline(self):
        """Run full training pipeline"""
        self.load_and_prep_data()
        self.split_data()
        self.train_logistic_regression()
        self.train_random_forest()
        self.evaluate_models()

if __name__ == "__main__":
    trainer = ChurnTrainer()
    trainer.run_pipeline()
