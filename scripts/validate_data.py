"""
Data validation script for SmartCLV
Validates data quality and completeness
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'data' / 'smartclv.db'

def validate_database():
    """Run validation checks on database"""
    
    if not DB_PATH.exists():
        print("[ERROR] Database not found!")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("SmartCLV Data Validation")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Check 1: All tables exist
    print("Check 1: Table existence")
    required_tables = ['customers', 'transactions', 'behavioral_data', 'engagement_data', 'feedback']
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    for table in required_tables:
        if table in existing_tables:
            print(f"  [OK] {table}")
        else:
            print(f"  [MISSING] {table}")
            all_passed = False
    
    # Check 2: Data counts
    print("\nCheck 2: Data counts")
    for table in required_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count:,} records")
        if count == 0:
            all_passed = False
    
    # Check 3: Data integrity
    print("\nCheck 3: Data integrity")
    
    # Check for NULL values in critical fields
    cursor.execute("SELECT COUNT(*) FROM customers WHERE email IS NULL")
    null_emails = cursor.fetchone()[0]
    if null_emails == 0:
        print(f"  [OK] No NULL emails")
    else:
        print(f"  [FAIL] Found {null_emails} NULL emails")
        all_passed = False
    
    # Check foreign key relationships
    cursor.execute("""
        SELECT COUNT(*) FROM transactions t
        LEFT JOIN customers c ON t.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """)
    orphan_transactions = cursor.fetchone()[0]
    if orphan_transactions == 0:
        print(f"  [OK] All transactions have valid customer references")
    else:
        print(f"  [FAIL] Found {orphan_transactions} orphan transactions")
        all_passed = False
    
    # Check 4: Data ranges
    print("\nCheck 4: Data ranges")
    
    cursor.execute("SELECT MIN(amount), MAX(amount), AVG(amount) FROM transactions")
    min_amt, max_amt, avg_amt = cursor.fetchone()
    print(f"  Transaction amounts: ${min_amt:.2f} - ${max_amt:.2f} (avg: ${avg_amt:.2f})")
    
    cursor.execute("SELECT MIN(rating), MAX(rating) FROM feedback")
    min_rating, max_rating = cursor.fetchone()
    if min_rating >= 1 and max_rating <= 5:
        print(f"  [OK] Ratings in valid range (1-5)")
    else:
        print(f"  [FAIL] Invalid rating range: {min_rating}-{max_rating}")
        all_passed = False
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("[SUCCESS] All validation checks passed!")
    else:
        print("[WARNING] Some validation checks failed")
    
    conn.close()
    return all_passed

if __name__ == "__main__":
    validate_database()
