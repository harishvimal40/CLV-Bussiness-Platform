"""
Feature engineering module for SmartCLV
Extracts RFM, behavioral, and engagement features
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent.parent / 'data' / 'processed'

class FeatureEngineer:
    """Extract features for CLV prediction"""
    
    def __init__(self):
        self.reference_date = datetime(2024, 12, 31)  # End of data period
    
    def load_cleaned_data(self):
        """Load cleaned data"""
        print("Loading cleaned data...")
        
        self.customers = pd.read_csv(DATA_DIR / 'customers_clean.csv', parse_dates=['registration_date'])
        self.transactions = pd.read_csv(DATA_DIR / 'transactions_clean.csv', parse_dates=['transaction_date'])
        self.behavioral = pd.read_csv(DATA_DIR / 'behavioral_clean.csv', parse_dates=['visit_date'])
        self.engagement = pd.read_csv(DATA_DIR / 'engagement_clean.csv', parse_dates=['engagement_date'])
        self.feedback = pd.read_csv(DATA_DIR / 'feedback_clean.csv', parse_dates=['feedback_date'])
        
        print(f"Loaded {len(self.customers)} customers")
    
    def calculate_rfm_features(self):
        """Calculate Recency, Frequency, Monetary features"""
        print("\nCalculating RFM features...")
        
        rfm = self.transactions.groupby('customer_id').agg({
            'transaction_date': lambda x: (self.reference_date - x.max()).days,  # Recency
            'transaction_id': 'count',  # Frequency
            'amount': 'sum'  # Monetary
        }).reset_index()
        
        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        print(f"RFM features calculated for {len(rfm)} customers")
        return rfm
    
    def calculate_transaction_features(self):
        """Calculate advanced transaction features"""
        print("Calculating transaction features...")
        
        trans_features = self.transactions.groupby('customer_id').agg({
            'amount': ['mean', 'std', 'min', 'max'],
            'transaction_date': ['min', 'max', 'count'],
            'product_category': lambda x: x.nunique()
        }).reset_index()
        
        trans_features.columns = ['customer_id', 'avg_transaction_amount', 'std_transaction_amount',
                                   'min_transaction_amount', 'max_transaction_amount',
                                   'first_purchase_date', 'last_purchase_date', 'total_transactions',
                                   'product_diversity']
        
        # Calculate average days between purchases
        trans_features['purchase_span_days'] = (
            pd.to_datetime(trans_features['last_purchase_date']) - 
            pd.to_datetime(trans_features['first_purchase_date'])
        ).dt.days
        
        trans_features['avg_days_between_purchases'] = (
            trans_features['purchase_span_days'] / 
            (trans_features['total_transactions'] - 1)
        ).fillna(0)
        
        return trans_features
    
    def calculate_behavioral_features(self):
        """Calculate website behavioral features"""
        print("Calculating behavioral features...")
        
        behavior_features = self.behavioral.groupby('customer_id').agg({
            'session_duration': 'mean',
            'pages_viewed': 'mean',
            'cart_abandonment': 'sum',
            'visit_date': 'count'
        }).reset_index()
        
        behavior_features.columns = ['customer_id', 'avg_session_duration', 'avg_pages_viewed',
                                      'total_cart_abandonments', 'total_visits']
        
        behavior_features['cart_abandonment_rate'] = (
            behavior_features['total_cart_abandonments'] / 
            behavior_features['total_visits']
        )
        
        return behavior_features
    
    def calculate_engagement_features(self):
        """Calculate marketing engagement features"""
        print("Calculating engagement features...")
        
        engagement_features = self.engagement.groupby('customer_id').agg({
            'email_opened': 'sum',
            'ad_clicked': 'sum',
            'social_media_interaction': 'sum',
            'engagement_date': 'count'
        }).reset_index()
        
        engagement_features.columns = ['customer_id', 'total_emails_opened', 'total_ads_clicked',
                                        'total_social_interactions', 'total_engagement_events']
        
        engagement_features['email_open_rate'] = (
            engagement_features['total_emails_opened'] / 
            engagement_features['total_engagement_events']
        )
        
        engagement_features['ad_click_rate'] = (
            engagement_features['total_ads_clicked'] / 
            engagement_features['total_engagement_events']
        )
        
        # Calculate engagement score (0-100)
        engagement_features['engagement_score'] = (
            (engagement_features['email_open_rate'] * 0.4 +
             engagement_features['ad_click_rate'] * 0.3 +
             (engagement_features['total_social_interactions'] / 
              engagement_features['total_social_interactions'].max()) * 0.3) * 100
        )
        
        return engagement_features
    
    def calculate_sentiment_features(self):
        """Calculate sentiment features from feedback"""
        print("Calculating sentiment features...")
        
        sentiment_features = self.feedback.groupby('customer_id').agg({
            'rating': 'mean',
            'sentiment_score': 'mean',
            'feedback_id': 'count'
        }).reset_index()
        
        sentiment_features.columns = ['customer_id', 'avg_rating', 'avg_sentiment', 'total_reviews']
        
        # Positive review ratio
        positive_reviews = self.feedback[self.feedback['rating'] >= 4].groupby('customer_id').size()
        sentiment_features['positive_review_ratio'] = (
            sentiment_features['customer_id'].map(positive_reviews) / 
            sentiment_features['total_reviews']
        ).fillna(0)
        
        return sentiment_features
    
    def calculate_customer_features(self):
        """Calculate customer demographic features"""
        print("Calculating customer features...")
        
        customer_features = self.customers.copy()
        
        # Customer tenure (days since registration)
        customer_features['tenure_days'] = (
            self.reference_date - customer_features['registration_date']
        ).dt.days
        
        # Age groups
        customer_features['age_group'] = pd.cut(
            customer_features['age'], 
            bins=[0, 25, 35, 50, 100],
            labels=['18-25', '26-35', '36-50', '50+']
        ).astype(str).replace('nan', 'Unknown')
        
        return customer_features[['customer_id', 'age', 'gender', 'tenure_days', 'age_group']]
    
    def merge_all_features(self):
        """Merge all features into single dataframe"""
        print("\nMerging all features...")
        
        # Calculate all feature sets
        rfm = self.calculate_rfm_features()
        trans_features = self.calculate_transaction_features()
        behavior_features = self.calculate_behavioral_features()
        engagement_features = self.calculate_engagement_features()
        sentiment_features = self.calculate_sentiment_features()
        customer_features = self.calculate_customer_features()
        
        # Merge all features
        features = customer_features.merge(rfm, on='customer_id', how='left')
        features = features.merge(trans_features[['customer_id', 'avg_transaction_amount', 
                                                   'product_diversity', 'avg_days_between_purchases']], 
                                  on='customer_id', how='left')
        features = features.merge(behavior_features, on='customer_id', how='left')
        features = features.merge(engagement_features[['customer_id', 'engagement_score', 
                                                        'email_open_rate', 'ad_click_rate']], 
                                  on='customer_id', how='left')
        features = features.merge(sentiment_features, on='customer_id', how='left')
        
        # Fill missing values with 0
        features = features.fillna(0)
        
        print(f"\nTotal features created: {len(features.columns) - 1}")
        print(f"Feature names: {list(features.columns)}")
        
        return features
    
    def save_features(self, features):
        """Save features to CSV"""
        output_path = DATA_DIR / 'customer_features.csv'
        features.to_csv(output_path, index=False)
        print(f"\n[SUCCESS] Features saved to {output_path}")
    
    def engineer_features(self):
        """Run complete feature engineering pipeline"""
        print("=" * 60)
        print("SmartCLV Feature Engineering Pipeline")
        print("=" * 60)
        
        self.load_cleaned_data()
        features = self.merge_all_features()
        self.save_features(features)
        
        return features

if __name__ == "__main__":
    engineer = FeatureEngineer()
    features = engineer.engineer_features()
    print(f"\nFeature engineering complete! Created {len(features)} customer records.")
