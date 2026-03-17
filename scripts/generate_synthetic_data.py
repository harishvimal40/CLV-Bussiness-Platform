"""
Synthetic data generator for SmartCLV
Generates realistic customer data with patterns
"""

import sqlite3
import random
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from faker import Faker

# Initialize Faker
fake = Faker()

# Database path
DB_PATH = Path(__file__).parent.parent / 'data' / 'smartclv.db'

# Configuration
NUM_CUSTOMERS = 10000
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Product categories
CATEGORIES = [
    'Electronics', 'Clothing', 'Home & Garden', 'Books', 
    'Sports', 'Beauty', 'Toys', 'Food & Beverage'
]

# Payment methods
PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer']

# Review templates
POSITIVE_REVIEWS = [
    "Great product! Highly recommend.",
    "Excellent quality and fast shipping.",
    "Very satisfied with my purchase.",
    "Amazing! Will buy again.",
    "Perfect! Exceeded expectations."
]

NEGATIVE_REVIEWS = [
    "Not as described. Disappointed.",
    "Poor quality. Would not recommend.",
    "Took too long to arrive.",
    "Not worth the price.",
    "Had to return it."
]

def random_date(start, end):
    """Generate random date between start and end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def generate_customers(cursor, num_customers):
    """Generate customer data"""
    print(f"Generating {num_customers} customers...")
    
    customers = []
    # Generate unique emails first
    unique_emails = set()
    while len(unique_emails) < num_customers:
        unique_emails.add(fake.email())
    unique_emails_list = list(unique_emails)

    for i in range(num_customers):
        name = fake.name()
        email = unique_emails_list[i]
        registration_date = random_date(START_DATE, END_DATE - timedelta(days=30))
        country = fake.country()
        age = random.randint(18, 75)
        gender = random.choice(['M', 'F', 'Other'])
        
        customers.append((name, email, registration_date, country, age, gender))
    
    cursor.executemany('''
        INSERT INTO customers (name, email, registration_date, country, age, gender)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', customers)
    
    print(f"[OK] Generated {num_customers} customers")

def generate_transactions(cursor):
    """Generate transaction data with realistic patterns"""
    print("Generating transactions...")
    
    # Get all customer IDs
    cursor.execute("SELECT customer_id, registration_date FROM customers")
    customers = cursor.fetchall()
    
    transactions = []
    
    for customer_id, reg_date in customers:
        reg_date = datetime.strptime(reg_date, '%Y-%m-%d %H:%M:%S')
        
        # Customer segments (different purchase patterns)
        segment = random.choices(
            ['high_value', 'medium_value', 'low_value', 'churned'],
            weights=[0.15, 0.35, 0.35, 0.15]
        )[0]
        
        if segment == 'high_value':
            num_transactions = random.randint(10, 30)
            avg_amount = random.uniform(100, 500)
        elif segment == 'medium_value':
            num_transactions = random.randint(3, 10)
            avg_amount = random.uniform(50, 150)
        elif segment == 'low_value':
            num_transactions = random.randint(1, 3)
            avg_amount = random.uniform(20, 80)
        else:  # churned
            num_transactions = random.randint(1, 2)
            avg_amount = random.uniform(30, 100)
        
        for _ in range(num_transactions):
            # Transaction date after registration
            if segment == 'churned':
                # Churned customers: transactions only in first 3 months
                # Must be inactive for > 180 days, so max_date must be < END_DATE - 180
                churn_cutoff = END_DATE - timedelta(days=180)
                
                # If registered after churn cutoff, they can't be "churned" by this definition
                # So we interpret them as "early churn" (stopped immediately)
                if reg_date > churn_cutoff:
                    max_date = reg_date + timedelta(days=1) # Allow 1 day window
                else:
                    max_date = min(reg_date + timedelta(days=90), churn_cutoff)
            else:
                max_date = END_DATE
            
            trans_date = random_date(reg_date, max_date)
            amount = round(np.random.normal(avg_amount, avg_amount * 0.3), 2)
            amount = max(10, amount)  # Minimum $10
            category = random.choice(CATEGORIES)
            payment_method = random.choice(PAYMENT_METHODS)
            
            transactions.append((customer_id, trans_date, amount, category, payment_method))
    
    cursor.executemany('''
        INSERT INTO transactions (customer_id, transaction_date, amount, product_category, payment_method)
        VALUES (?, ?, ?, ?, ?)
    ''', transactions)
    
    print(f"[OK] Generated {len(transactions)} transactions")

def generate_behavioral_data(cursor):
    """Generate website behavioral data"""
    print("Generating behavioral data...")
    
    cursor.execute("SELECT customer_id, registration_date FROM customers")
    customers = cursor.fetchall()
    
    behaviors = []
    
    for customer_id, reg_date in customers:
        reg_date = datetime.strptime(reg_date, '%Y-%m-%d %H:%M:%S')
        
        # Number of visits
        num_visits = random.randint(5, 50)
        
        for _ in range(num_visits):
            visit_date = random_date(reg_date, END_DATE)
            session_duration = random.randint(30, 1800)  # 30 sec to 30 min
            pages_viewed = random.randint(1, 20)
            cart_abandonment = random.choice([0, 0, 0, 1])  # 25% abandonment
            
            behaviors.append((customer_id, visit_date, session_duration, pages_viewed, cart_abandonment))
    
    cursor.executemany('''
        INSERT INTO behavioral_data (customer_id, visit_date, session_duration, pages_viewed, cart_abandonment)
        VALUES (?, ?, ?, ?, ?)
    ''', behaviors)
    
    print(f"[OK] Generated {len(behaviors)} behavioral records")

def generate_engagement_data(cursor):
    """Generate marketing engagement data"""
    print("Generating engagement data...")
    
    cursor.execute("SELECT customer_id, registration_date FROM customers")
    customers = cursor.fetchall()
    
    engagements = []
    
    for customer_id, reg_date in customers:
        reg_date = datetime.strptime(reg_date, '%Y-%m-%d %H:%M:%S')
        
        # Number of engagement events
        num_events = random.randint(10, 100)
        
        for _ in range(num_events):
            engagement_date = random_date(reg_date, END_DATE)
            email_opened = random.choice([0, 0, 1])  # 33% open rate
            ad_clicked = random.choice([0, 0, 0, 1])  # 25% click rate
            social_interaction = random.randint(0, 5)
            
            engagements.append((customer_id, email_opened, ad_clicked, social_interaction, engagement_date))
    
    cursor.executemany('''
        INSERT INTO engagement_data (customer_id, email_opened, ad_clicked, social_media_interaction, engagement_date)
        VALUES (?, ?, ?, ?, ?)
    ''', engagements)
    
    print(f"[OK] Generated {len(engagements)} engagement records")

def generate_feedback(cursor):
    """Generate customer feedback and reviews"""
    print("Generating feedback...")
    
    cursor.execute("SELECT customer_id, registration_date FROM customers")
    customers = cursor.fetchall()
    
    feedbacks = []
    
    for customer_id, reg_date in customers:
        reg_date = datetime.strptime(reg_date, '%Y-%m-%d %H:%M:%S')
        
        # 30% of customers leave reviews
        if random.random() < 0.3:
            num_reviews = random.randint(1, 3)
            
            for _ in range(num_reviews):
                feedback_date = random_date(reg_date, END_DATE)
                rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.2, 0.35, 0.3])[0]
                
                # Sentiment based on rating
                if rating >= 4:
                    review_text = random.choice(POSITIVE_REVIEWS)
                    sentiment_score = round(random.uniform(0.5, 1.0), 2)
                elif rating == 3:
                    review_text = "It's okay. Average product."
                    sentiment_score = round(random.uniform(-0.2, 0.2), 2)
                else:
                    review_text = random.choice(NEGATIVE_REVIEWS)
                    sentiment_score = round(random.uniform(-1.0, -0.3), 2)
                
                feedbacks.append((customer_id, rating, review_text, sentiment_score, feedback_date))
    
    cursor.executemany('''
        INSERT INTO feedback (customer_id, rating, review_text, sentiment_score, feedback_date)
        VALUES (?, ?, ?, ?, ?)
    ''', feedbacks)
    
    print(f"[OK] Generated {len(feedbacks)} feedback records")

def generate_all_data():
    """Main function to generate all synthetic data"""
    
    if not DB_PATH.exists():
        print("[ERROR] Database not found. Please run setup_database.py first.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("SmartCLV Synthetic Data Generator")
    print("=" * 60)
    print()
    
    try:
        generate_customers(cursor, NUM_CUSTOMERS)
        conn.commit()
        
        generate_transactions(cursor)
        conn.commit()
        
        generate_behavioral_data(cursor)
        conn.commit()
        
        generate_engagement_data(cursor)
        conn.commit()
        
        generate_feedback(cursor)
        conn.commit()
        
        print()
        print("=" * 60)
        print("[SUCCESS] All synthetic data generated successfully!")
        print("=" * 60)
        
        # Print statistics
        cursor.execute("SELECT COUNT(*) FROM customers")
        print(f"Total customers: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM transactions")
        print(f"Total transactions: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM behavioral_data")
        print(f"Total behavioral records: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM engagement_data")
        print(f"Total engagement records: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM feedback")
        print(f"Total feedback records: {cursor.fetchone()[0]}")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    generate_all_data()
