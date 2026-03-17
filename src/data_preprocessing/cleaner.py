"""
Data cleaning module for SmartCLV
Handles missing values, duplicates, and outliers
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent.parent.parent / 'data' / 'smartclv.db'

class DataCleaner:
    """Clean and validate customer data"""
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
    
    def load_data(self):
        """Load all tables from database"""
        print("Loading data from database...")
        
        self.customers = pd.read_sql_query("SELECT * FROM customers", self.conn)
        self.transactions = pd.read_sql_query("SELECT * FROM transactions", self.conn)
        self.behavioral = pd.read_sql_query("SELECT * FROM behavioral_data", self.conn)
        self.engagement = pd.read_sql_query("SELECT * FROM engagement_data", self.conn)
        self.feedback = pd.read_sql_query("SELECT * FROM feedback", self.conn)
        
        print(f"Loaded {len(self.customers)} customers")
        print(f"Loaded {len(self.transactions)} transactions")
        print(f"Loaded {len(self.behavioral)} behavioral records")
        print(f"Loaded {len(self.engagement)} engagement records")
        print(f"Loaded {len(self.feedback)} feedback records")
    
    def check_missing_values(self):
        """Check for missing values in critical fields"""
        print("\nChecking missing values...")
        
        tables = {
            'customers': self.customers,
            'transactions': self.transactions,
            'behavioral': self.behavioral,
            'engagement': self.engagement,
            'feedback': self.feedback
        }
        
        for name, df in tables.items():
            missing = df.isnull().sum()
            if missing.sum() > 0:
                print(f"\n{name}:")
                print(missing[missing > 0])
            else:
                print(f"{name}: No missing values")
    
    def remove_duplicates(self):
        """Remove duplicate records"""
        print("\nRemoving duplicates...")
        
        before = len(self.customers)
        self.customers = self.customers.drop_duplicates(subset=['email'])
        after = len(self.customers)
        print(f"Customers: Removed {before - after} duplicates")
        
        before = len(self.transactions)
        self.transactions = self.transactions.drop_duplicates()
        after = len(self.transactions)
        print(f"Transactions: Removed {before - after} duplicates")
    
    def detect_outliers(self, column, df, method='iqr'):
        """Detect outliers using IQR method"""
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            return outliers
        return pd.DataFrame()
    
    def handle_outliers(self):
        """Handle outliers in transaction amounts"""
        print("\nHandling outliers...")
        
        outliers = self.detect_outliers('amount', self.transactions)
        print(f"Found {len(outliers)} transaction amount outliers")
        
        # Cap outliers instead of removing
        Q1 = self.transactions['amount'].quantile(0.25)
        Q3 = self.transactions['amount'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        
        self.transactions.loc[self.transactions['amount'] > upper_bound, 'amount'] = upper_bound
        print(f"Capped outliers at ${upper_bound:.2f}")
    
    def convert_dates(self):
        """Convert date columns to datetime"""
        print("\nConverting dates...")
        
        self.customers['registration_date'] = pd.to_datetime(self.customers['registration_date'])
        self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        self.behavioral['visit_date'] = pd.to_datetime(self.behavioral['visit_date'])
        self.engagement['engagement_date'] = pd.to_datetime(self.engagement['engagement_date'])
        self.feedback['feedback_date'] = pd.to_datetime(self.feedback['feedback_date'])
        
        print("All dates converted to datetime format")
    
    def save_cleaned_data(self):
        """Save cleaned data to CSV"""
        output_dir = Path(__file__).parent.parent.parent / 'data' / 'processed'
        output_dir.mkdir(exist_ok=True)
        
        self.customers.to_csv(output_dir / 'customers_clean.csv', index=False)
        self.transactions.to_csv(output_dir / 'transactions_clean.csv', index=False)
        self.behavioral.to_csv(output_dir / 'behavioral_clean.csv', index=False)
        self.engagement.to_csv(output_dir / 'engagement_clean.csv', index=False)
        self.feedback.to_csv(output_dir / 'feedback_clean.csv', index=False)
        
        print(f"\nCleaned data saved to {output_dir}")
    
    def clean_all(self):
        """Run complete cleaning pipeline"""
        print("=" * 60)
        print("SmartCLV Data Cleaning Pipeline")
        print("=" * 60)
        
        self.load_data()
        self.check_missing_values()
        self.remove_duplicates()
        self.convert_dates()
        self.handle_outliers()
        self.save_cleaned_data()
        
        print("\n[SUCCESS] Data cleaning complete!")
        self.conn.close()

if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.clean_all()
