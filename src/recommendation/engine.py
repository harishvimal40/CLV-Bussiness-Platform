"""
Recommendation Engine
Generates personalized actions based on customer segments (CLV & Churn)
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
# Load inputs
CLV_PATH = BASE_DIR / 'data' / 'processed' / 'clv_predictions.csv'
CHURN_PATH = BASE_DIR / 'data' / 'processed' / 'churn_predictions.csv'
OUTPUT_PATH = BASE_DIR / 'data' / 'processed' / 'recommendations.csv'

def load_data():
    if not CLV_PATH.exists() or not CHURN_PATH.exists():
        raise FileNotFoundError("Input predictions not found. Run Phase 4 and 5 first.")
        
    clv_df = pd.read_csv(CLV_PATH)
    churn_df = pd.read_csv(CHURN_PATH)
    
    # Merge on customer_id
    print("Merging CLV and Churn data...")
    df = pd.merge(clv_df, churn_df, on='customer_id')
    return df

def generate_recommendations():
    df = load_data()
    
    # Calculate CLV thresholds for segmentation (High/Medium/Low Value)
    # Using 'monetary' or 'predicted_clv' - let's use predicted
    high_clv = df['predicted_clv'].quantile(0.80) # Top 20%
    med_clv = df['predicted_clv'].quantile(0.40)  # Next 40% (40-80)
    
    print(f"CLV Thresholds: High > {high_clv:.2f}, Medium > {med_clv:.2f}")
    
    # Define Segment Logic
    def get_segment(row):
        clv = row['predicted_clv']
        risk_prob = row['churn_probability']
        
        # Risk Categories
        is_high_risk = risk_prob > 0.7
        is_med_risk = risk_prob > 0.3
        
        # Value Categories
        is_high_val = clv > high_clv
        is_med_val = clv > med_clv
        
        # Matrix Logic
        if is_high_val:
            if is_high_risk: return "Can't Lose"     # High Value, High Risk
            elif is_med_risk: return "At Risk High"  # High Value, Med Risk
            else: return "Champions"                 # High Value, Low Risk
            
        elif is_med_val:
            if is_high_risk: return "At Risk"        # Med Value, High Risk
            elif is_med_risk: return "Need Attention" # Med Value, Med Risk
            else: return "Loyal Customers"           # Med Value, Low Risk
            
        else: # Low Value
            if is_high_risk: return "Hibernating"    # Low Value, High Risk
            elif is_med_risk: return "Drifting"      # Low Value, Med Risk
            else: return "Potential Loyalists"       # Low Value, Low Risk

    print("Assigning segments...")
    df['segment'] = df.apply(get_segment, axis=1)
    
    # Map Actions & Offers
    # (Segment) -> (Primary Action, Offer)
    strategies = {
        "Champions": ("Reward Loyalty", "Exclusive VIP Access"),
        "Can't Lose": ("Immediate Retention", "20% Off Next Purchase"),
        "At Risk High": ("Personal Outreach", "Free Shipping + 10% Off"),
        "At Risk": ("Re-engagement Campaign", "15% Discount"),
        "Loyal Customers": ("Upsell / Cross-sell", "Buy 1 Get 1 Free"),
        "Need Attention": ("Nurture", "Product Recommendations"),
        "Potential Loyalists": ("Onboarding", "Welcome Guide"),
        "Drifting": ("Reconnect", "Usage Tips"),
        "Hibernating": ("Win-back", "We Miss You Offer"),
    }
    
    # Apply strategies
    def apply_strategy(segment):
        return strategies.get(segment, ("General Marketing", "None"))

    df['action'], df['offer'] = zip(*df['segment'].map(apply_strategy))
    
    # Save Results
    output_cols = ['customer_id', 'predicted_clv', 'churn_probability', 'segment', 'action', 'offer']
    df[output_cols].to_csv(OUTPUT_PATH, index=False)
    
    print(f"Recommendations saved to {OUTPUT_PATH}")
    
    # Print Summary
    print("\nSegment Distribution:")
    print(df['segment'].value_counts(normalize=True))
    
    return df[output_cols].head()

if __name__ == "__main__":
    generate_recommendations()
