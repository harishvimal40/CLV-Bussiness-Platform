# SmartCLV User Manual

## Getting Started

### Installation

**Prerequisites:**
- Python 3.8 or higher
- 8GB RAM minimum
- 2GB free disk space

**Step 1: Clone Repository**
```powershell
git clone <repository-url>
cd SmartCLV
```

**Step 2: Create Virtual Environment**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Step 3: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 4: Setup Database**
```powershell
python scripts/setup_database.py
python scripts/generate_synthetic_data.py
```

**Step 5: Run Data Pipeline**
```powershell
python src/main_pipeline.py
```

**Step 6: Launch Dashboard**
```powershell
streamlit run dashboard/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## Dashboard Guide

### Overview Tab 📊

**Key Metrics:**
- **Total Customers**: Number of customers in database
- **Avg CLV**: Average predicted customer lifetime value
- **Churn Rate**: Percentage of customers at risk
- **High Risk Customers**: Count of customers with >70% churn probability

**Segment Distribution Chart:**
- Pie chart showing customer distribution across segments
- Click segments to see details

### CLV Analysis Tab 💰

**CLV Distribution Histogram:**
- Shows how customer value is distributed
- Identify high-value customer concentration
- X-axis: Predicted CLV, Y-axis: Customer count

**CLV by Segment Box Plot:**
- Compare value across segments
- Identify outliers
- Median values shown as line in box

**How to Use:**
1. Review distribution to understand value spread
2. Identify which segments have highest CLV
3. Focus retention efforts on high-value segments

### Churn Risk Tab 📉

**Churn Probability Distribution:**
- Red histogram showing risk distribution
- Most customers should be in low-risk range

**Risk vs Value Scatter Plot:**
- X-axis: Churn probability (0-1)
- Y-axis: Predicted CLV
- Color: Customer segment
- **Critical Zone**: Top-right (High Value + High Risk)

**How to Use:**
1. Identify customers in "Can't Lose" zone (top-right)
2. Hover over points to see customer details
3. Prioritize retention for high-value, high-risk customers

### Decisions Tab 💡

**Recommended Actions Table:**
- Shows count of customers per action type
- Actions: "Immediate Retention", "Reward Loyalty", etc.

**Customer List:**
- Filterable table with all customers
- Columns: ID, Segment, Action, Offer, CLV, Churn Probability
- Use sidebar filters to narrow down

**Export Functionality:**
- Click "Download Recommendations CSV"
- Opens filtered data in Excel/CSV viewer
- Use for email campaigns or CRM import

**How to Use:**
1. Filter by segment (e.g., "Can't Lose")
2. Review recommended actions
3. Download list for marketing team
4. Execute campaigns based on offers

### Explainability Tab 🧠

**CLV Feature Importance:**
- SHAP summary plot
- Shows which features drive customer value
- Red = High feature value, Blue = Low feature value
- Features sorted by importance (top to bottom)

**Churn Feature Importance:**
- Similar plot for churn prediction
- Understand what causes customers to leave
- Use insights to improve retention strategies

**How to Interpret:**
- **Recency**: Days since last purchase (higher = more likely to churn)
- **Frequency**: Purchase count (higher = lower churn risk)
- **Engagement Score**: Marketing interaction level

---

## Filters & Controls

### Sidebar Filters

**Select Customer Segments:**
- Multi-select dropdown
- Choose one or more segments
- Dashboard updates automatically

**Available Segments:**
- Champions (High Value, Low Risk)
- Can't Lose (High Value, High Risk)
- At Risk (Medium Value, High Risk)
- Loyal Customers (Medium Value, Low Risk)
- Hibernating (Low Value, High Risk)
- And more...

---

## Interpreting Results

### What is CLV?
Customer Lifetime Value represents the total revenue expected from a customer over their entire relationship with your business.

**High CLV Customers:**
- Frequent purchasers
- High average transaction value
- Long tenure
- High engagement

**Low CLV Customers:**
- Infrequent purchases
- Low spending
- Recent registrations
- Low engagement

### What is Churn Risk?
Probability (0-100%) that a customer will stop doing business with you.

**High Risk Indicators:**
- No recent purchases (high recency)
- Declining purchase frequency
- Low email engagement
- Cart abandonments

**Low Risk Indicators:**
- Recent purchases
- Consistent buying pattern
- High engagement scores
- Positive reviews

### Recommended Actions

| Segment | Action | Why |
|---------|--------|-----|
| Champions | VIP Treatment | Reward loyalty, prevent competitors from poaching |
| Can't Lose | Immediate Retention | High value at risk, urgent intervention needed |
| At Risk | Re-engagement | Medium value, still salvageable |
| Hibernating | Win-back Campaign | Low value but low cost to try |

---

## Troubleshooting

### Dashboard Won't Load
**Error**: `ModuleNotFoundError`
- **Solution**: Ensure virtual environment is activated and dependencies installed
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### No Data Showing
**Error**: "Data not found"
- **Solution**: Run the data pipeline first
```powershell
python src/main_pipeline.py
```

### Slow Performance
**Issue**: Dashboard takes long to load
- **Solution**: Reduce dataset size or use data sampling
- Check system resources (RAM usage)

### Charts Not Displaying
**Issue**: Blank visualizations
- **Solution**: Clear Streamlit cache
```powershell
streamlit cache clear
```

---

## FAQ

**Q: Can I use my own data?**
A: Yes, replace synthetic data generation with your own data import. Ensure schema matches.

**Q: How often should I retrain models?**
A: Recommended monthly or when significant business changes occur.

**Q: Can I export individual customer reports?**
A: Use the CSV export feature and filter by customer ID.

**Q: What if a customer appears in wrong segment?**
A: Check their recent activity data. Model predictions are based on historical patterns.

**Q: How accurate are the predictions?**
A: CLV model: R² = 0.9995 (very high). Churn model: AUC = 0.90 (excellent).

---

## Best Practices

1. **Regular Updates**: Run pipeline weekly to keep predictions current
2. **Action Tracking**: Monitor which actions lead to retention
3. **Segment Analysis**: Review segment distribution monthly
4. **A/B Testing**: Test different offers on similar segments
5. **Feedback Loop**: Update model with actual outcomes

---

## Support

For technical issues or questions:
- Check documentation: `docs/technical_documentation.md`
- Review code comments in source files
- Run tests: `pytest tests/`

---

## Glossary

- **CLV**: Customer Lifetime Value
- **RFM**: Recency, Frequency, Monetary
- **SHAP**: SHapley Additive exPlanations
- **AUC**: Area Under Curve (model performance metric)
- **F1-Score**: Harmonic mean of precision and recall
- **Churn**: Customer attrition/leaving
