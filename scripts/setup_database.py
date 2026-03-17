"""
Database setup script for SmartCLV
Creates SQLite database with all required tables
"""

import sqlite3
import os
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / 'data' / 'smartclv.db'

def create_database():
    """Create database and all tables"""
    
    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            registration_date DATE NOT NULL,
            country TEXT,
            age INTEGER,
            gender TEXT CHECK(gender IN ('M', 'F', 'Other')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("[OK] Created customers table")
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            transaction_date DATE NOT NULL,
            amount REAL NOT NULL,
            product_category TEXT,
            payment_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    print("[OK] Created transactions table")
    
    # Create behavioral_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS behavioral_data (
            behavior_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            visit_date DATE NOT NULL,
            session_duration INTEGER,
            pages_viewed INTEGER,
            cart_abandonment BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    print("[OK] Created behavioral_data table")
    
    # Create engagement_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS engagement_data (
            engagement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            email_opened BOOLEAN DEFAULT 0,
            ad_clicked BOOLEAN DEFAULT 0,
            social_media_interaction INTEGER DEFAULT 0,
            engagement_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    print("[OK] Created engagement_data table")
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            rating INTEGER CHECK (rating BETWEEN 1 AND 5),
            review_text TEXT,
            sentiment_score REAL,
            feedback_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    print("[OK] Created feedback table")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"\n[SUCCESS] Database created successfully at: {DB_PATH}")
    print(f"Database size: {os.path.getsize(DB_PATH)} bytes")

if __name__ == "__main__":
    create_database()
