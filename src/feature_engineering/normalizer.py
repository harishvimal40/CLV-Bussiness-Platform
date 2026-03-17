"""
Feature normalization module for SmartCLV
Scales features for machine learning models
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib

DATA_DIR = Path(__file__).parent.parent.parent / 'data' / 'processed'
MODEL_DIR = Path(__file__).parent.parent.parent / 'models'

class FeatureNormalizer:
    """Normalize and scale features"""
    
    def __init__(self, method='standard'):
        """
        Initialize normalizer
        method: 'standard' (StandardScaler) or 'minmax' (MinMaxScaler)
        """
        self.method = method
        if method == 'standard':
            self.scaler = StandardScaler()
        else:
            self.scaler = MinMaxScaler()
    
    def load_features(self):
        """Load engineered features"""
        print("Loading features...")
        self.features = pd.read_csv(DATA_DIR / 'customer_features.csv')
        print(f"Loaded {len(self.features)} customer records")
    
    def select_numerical_features(self):
        """Select only numerical features for scaling"""
        # Exclude categorical and ID columns
        exclude_cols = ['customer_id', 'gender', 'age_group']
        
        numerical_cols = [col for col in self.features.columns 
                         if col not in exclude_cols and 
                         self.features[col].dtype in ['int64', 'float64']]
        
        print(f"\nNumerical features to scale: {len(numerical_cols)}")
        return numerical_cols
    
    def normalize_features(self):
        """Normalize numerical features"""
        print(f"\nNormalizing features using {self.method} scaling...")
        
        numerical_cols = self.select_numerical_features()
        
        # Fit and transform
        scaled_values = self.scaler.fit_transform(self.features[numerical_cols])
        
        # Create scaled dataframe
        scaled_features = self.features.copy()
        scaled_features[numerical_cols] = scaled_values
        
        print("[OK] Features normalized")
        return scaled_features, numerical_cols
    
    def save_normalized_features(self, scaled_features):
        """Save normalized features"""
        output_path = DATA_DIR / 'customer_features_normalized.csv'
        scaled_features.to_csv(output_path, index=False)
        print(f"Normalized features saved to {output_path}")
    
    def save_scaler(self):
        """Save scaler for future use"""
        MODEL_DIR.mkdir(exist_ok=True)
        scaler_path = MODEL_DIR / f'scaler_{self.method}.pkl'
        joblib.dump(self.scaler, scaler_path)
        print(f"Scaler saved to {scaler_path}")
    
    def normalize_pipeline(self):
        """Run complete normalization pipeline"""
        print("=" * 60)
        print("SmartCLV Feature Normalization Pipeline")
        print("=" * 60)
        
        self.load_features()
        scaled_features, numerical_cols = self.normalize_features()
        self.save_normalized_features(scaled_features)
        self.save_scaler()
        
        print("\n[SUCCESS] Feature normalization complete!")
        return scaled_features

if __name__ == "__main__":
    normalizer = FeatureNormalizer(method='standard')
    normalized_features = normalizer.normalize_pipeline()
