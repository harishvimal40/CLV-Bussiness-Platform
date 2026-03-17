"""
CLV Model Training Module
Trains and evaluates multiple ML models to predict Customer Lifetime Value
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Dirs
BASE_DIR = Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'customer_features_normalized.csv'
MODEL_DIR = BASE_DIR / 'models' / 'clv_models'
METRICS_PATH = BASE_DIR / 'models' / 'model_metrics.json'

MODEL_DIR.mkdir(parents=True, exist_ok=True)

class CLVTrainer:
    """Train and evaluate CLV prediction models"""

    def __init__(self):
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.results = {}

    def load_data(self):
        """Load normalized features"""
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Data file not found at {DATA_PATH}. Run Phase 3 first.")
        
        print(f"Loading data from {DATA_PATH}...")
        df = pd.read_csv(DATA_PATH)
        
        # Define features and target
        # Target: 'monetary' (Total spend so far) represents historical CLV. 
        # In a real-world predictive scenario, we would aim to predict FUTURE value.
        # For this project scope, we typically split by time (holdout set), 
        # but here we'll use the engineered 'monetary' value as the proxy for Life Time Value 
        # to learn the relationship between behavior/demographics and value.
        
        target_col = 'monetary'
        
        # Drop ID and other non-predictive columns available at training time
        drop_cols = ['customer_id', 'monetary', 'recency', 'frequency'] 
        # Note: We drop R,F,M from inputs to avoid data leakage if predicting M, 
        # BUT for a 'Current Value' estimation model, R and F are valid predictors.
        # Let's keep R and F as features to predict M.
        
        features = [col for col in df.columns if col not in ['customer_id', 'monetary', 'gender', 'age_group']]
        
        self.X = df[features]
        self.y = df[target_col]
        
        print(f"Features: {features}")
        print(f"Target: {target_col}")

    def split_data(self):
        """Split data into train and test sets"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        print(f"Training set: {self.X_train.shape[0]} samples")
        print(f"Test set: {self.X_test.shape[0]} samples")

    def train_baseline(self):
        """Train simple Linear Regression baseline"""
        print("\nTraining Baseline (Linear Regression)...")
        lr = LinearRegression()
        lr.fit(self.X_train, self.y_train)
        self.models['LinearRegression'] = lr

    def train_random_forest(self):
        """Train Random Forest Regressor"""
        print("\nTraining Random Forest...")
        rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        rf.fit(self.X_train, self.y_train)
        self.models['RandomForest'] = rf

    def train_xgboost(self):
        """Train XGBoost Regressor"""
        print("\nTraining XGBoost...")
        xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
        xgb.fit(self.X_train, self.y_train)
        self.models['XGBoost'] = xgb

    def evaluate_models(self):
        """Evaluate all trained models"""
        print("\nEvaluating models...")
        
        best_r2 = -float('inf')
        best_model_name = None

        for name, model in self.models.items():
            preds = model.predict(self.X_test)
            rmse = np.sqrt(mean_squared_error(self.y_test, preds))
            mae = mean_absolute_error(self.y_test, preds)
            r2 = r2_score(self.y_test, preds)
            
            self.results[name] = {
                'RMSE': round(rmse, 2),
                'MAE': round(mae, 2),
                'R2': round(r2, 4)
            }
            
            print(f"{name} -> RMSE: {rmse:.2f}, R²: {r2:.4f}")
            
            if r2 > best_r2:
                best_r2 = r2
                best_model_name = name

        # Save metrics
        with open(METRICS_PATH, 'w') as f:
            json.dump(self.results, f, indent=4)
            
        print(f"\nBest Model: {best_model_name} (R²: {best_r2:.4f})")
        
        # Save best model
        best_model = self.models[best_model_name]
        joblib.dump(best_model, MODEL_DIR / 'best_model.pkl')
        print(f"Saved best model to {MODEL_DIR / 'best_model.pkl'}")

    def plot_feature_importance(self):
        """Plot feature importance for the best model (RF or XGB)"""
        # Load best model logic or just plot XGBoost if available
        if 'XGBoost' in self.models:
            model = self.models['XGBoost']
            importances = model.feature_importances_
            feature_names = self.X.columns
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x=importances, y=feature_names)
            plt.title("Constraint Feature Importance (XGBoost)")
            plt.tight_layout()
            plt.savefig(BASE_DIR / 'models' / 'feature_importance.png')
            print("Feature importance plot saved.")

    def run_pipeline(self):
        """Run full training pipeline"""
        self.load_data()
        self.split_data()
        self.train_baseline()
        self.train_random_forest()
        self.train_xgboost()
        self.evaluate_models()
        self.plot_feature_importance()

if __name__ == "__main__":
    trainer = CLVTrainer()
    trainer.run_pipeline()
