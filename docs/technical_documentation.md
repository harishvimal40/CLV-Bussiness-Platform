# SmartCLV Technical Documentation

## System Architecture

### Overview
SmartCLV is an AI-powered Customer Lifetime Value prediction system that combines machine learning, behavioral analytics, and explainable AI to provide actionable business insights.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   SQLite    │────▶│ Data Prep &  │────▶│  ML Models  │────▶│  Dashboard   │
│  Database   │     │   Features   │     │   (XGB/RF)  │     │  (Streamlit) │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                            │                     │
                            ▼                     ▼
                    ┌──────────────┐     ┌──────────────┐
                    │ Normalization│     │ Explainability│
                    │  (Scaler)    │     │    (SHAP)     │
                    └──────────────┘     └──────────────┘
```

---

## Database Schema

### Tables

**1. customers**
- `customer_id` (PK): Unique identifier
- `name`: Customer name
- `email`: Email address (UNIQUE)
- `registration_date`: Account creation date
- `age`: Customer age
- `gender`: M/F

**2. transactions**
- `transaction_id` (PK)
- `customer_id` (FK)
- `transaction_date`: Purchase date
- `amount`: Transaction value
- `product_category`: Product type

**3. behavioral_data**
- `behavior_id` (PK)
- `customer_id` (FK)
- `visit_date`: Website visit date
- `session_duration`: Time on site (seconds)
- `pages_viewed`: Page count
- `cart_abandonment`: Boolean flag

**4. engagement_data**
- `engagement_id` (PK)
- `customer_id` (FK)
- `email_opened`: Boolean
- `ad_clicked`: Boolean
- `social_media_interaction`: Boolean
- `engagement_date`: Event date

**5. feedback**
- `feedback_id` (PK)
- `customer_id` (FK)
- `rating`: 1-5 stars
- `review_text`: Customer review
- `sentiment_score`: -1 to 1
- `feedback_date`: Review date

---

## Module Structure

### 1. Data Preprocessing (`src/data_preprocessing/`)
- **`cleaner.py`**: Handles missing values, duplicates, outliers
- **`normalizer.py`**: Scales features using StandardScaler

### 2. Feature Engineering (`src/feature_engineering/`)
- **`features.py`**: Extracts 22 features per customer
  - RFM (Recency, Frequency, Monetary)
  - Behavioral (session duration, cart abandonment)
  - Engagement (email open rate, ad clicks)
  - Sentiment (review ratings, sentiment scores)

### 3. Model Training (`src/model_training/`)
- **`trainer.py`**: CLV prediction models
  - Linear Regression (baseline)
  - Random Forest
  - **XGBoost** (selected, R² = 0.9995)
  
- **`churn_trainer.py`**: Churn prediction models
  - Logistic Regression
  - **Random Forest** (selected, F1 = 0.80, AUC = 0.90)

### 4. Prediction (`src/prediction/`)
- **`predictor.py`**: Generates CLV predictions
- **`churn_predictor.py`**: Generates churn probabilities

### 5. Recommendation (`src/recommendation/`)
- **`engine.py`**: Segments customers and assigns actions
  - 9-box matrix (Value × Risk)
  - Personalized offers

### 6. Explainability (`src/explainability/`)
- **`shap_explainer.py`**: SHAP value calculations
  - Global feature importance
  - Model interpretability

### 7. Dashboard (`dashboard/`)
- **`app.py`**: Streamlit web application
  - 5 tabs: Overview, CLV, Churn, Decisions, Explainability

---

## Model Performance

### CLV Prediction Model (XGBoost)
| Metric | Value |
|--------|-------|
| RMSE   | 0.02  |
| MAE    | 0.01  |
| R²     | 0.9995|

**Top Features:**
1. Monetary (historical spend)
2. Frequency (purchase count)
3. Engagement score
4. Tenure days

### Churn Prediction Model (Random Forest)
| Metric | Value |
|--------|-------|
| Accuracy | 0.85 |
| Precision | 0.82 |
| Recall | 0.79 |
| F1-Score | 0.80 |
| AUC-ROC | 0.90 |

**Top Features:**
1. Recency (days since last purchase)
2. Frequency
3. Email open rate
4. Cart abandonment rate

---

## API Reference

### FeatureEngineer Class
```python
from src.feature_engineering.features import FeatureEngineer

engineer = FeatureEngineer()
features = engineer.engineer_features()
```

**Methods:**
- `load_cleaned_data()`: Load preprocessed data
- `calculate_rfm_features()`: Compute RFM metrics
- `merge_all_features()`: Combine all feature sets
- `save_features(features)`: Export to CSV

### CLVTrainer Class
```python
from src.model_training.trainer import CLVTrainer

trainer = CLVTrainer()
trainer.run_pipeline()
```

**Methods:**
- `load_data()`: Load normalized features
- `train_xgboost()`: Train XGBoost model
- `evaluate_models()`: Calculate metrics
- `plot_feature_importance()`: Visualize importance

---

## Configuration

### Environment Variables (`.env`)
```
DB_PATH=data/smartclv.db
MODEL_DIR=models/
DATA_DIR=data/processed/
```

### Dependencies
- Python 3.8+
- pandas, numpy
- scikit-learn, xgboost
- streamlit, plotly
- shap
- faker (for synthetic data)

---

## Testing

### Unit Tests (`tests/test_core.py`)
```powershell
pytest tests/
```

**Test Coverage:**
- Data structure validation
- Churn probability ranges
- Recommendation logic
- Model loading

### Integration Pipeline
```powershell
python src/main_pipeline.py
```

Runs full workflow: Data → Features → Models → Predictions → Dashboard

---

## Performance Optimization

### Data Processing
- Batch processing for large datasets
- Efficient pandas operations
- Cached feature calculations

### Model Inference
- Pre-trained models loaded once
- Vectorized predictions
- Streamlit caching (`@st.cache_data`)

---

## Security Considerations

1. **Data Privacy**: No real customer data used (synthetic only)
2. **Database**: SQLite with local storage
3. **Authentication**: Not implemented (add for production)
4. **Input Validation**: Implemented in data cleaning

---

## Troubleshooting

### Common Issues

**Issue**: `UnicodeEncodeError` on Windows
- **Solution**: Use ASCII characters in print statements

**Issue**: `TypeError: Cannot setitem on Categorical`
- **Solution**: Convert categorical columns to string before fillna

**Issue**: Model file not found
- **Solution**: Run training scripts before prediction

---

## Future Enhancements

1. Real-time data streaming (Apache Kafka)
2. Deep learning models (LSTM for time-series)
3. A/B testing framework
4. Multi-currency support
5. Advanced segmentation (K-means clustering)
