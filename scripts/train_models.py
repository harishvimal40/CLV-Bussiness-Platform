import pandas as pd
import numpy as np
import joblib
import json
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score, 
    accuracy_score, confusion_matrix, roc_curve, auc
)
from sklearn.preprocessing import StandardScaler, LabelEncoder

warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent.parent
DATA_PATH    = BASE_DIR / "data" / "processed" / "customer_features_normalized.csv"
CLV_DIR      = BASE_DIR / "models" / "clv_models"
CHURN_DIR    = BASE_DIR / "models" / "churn_models"
PLOT_DIR     = BASE_DIR / "models" / "plots"
METRICS_PATH = BASE_DIR / "models" / "model_metrics.json"

CLV_DIR.mkdir(parents=True, exist_ok=True)
CHURN_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

def sep(title):
    print("\n" + "="*60)
    print("  " + title)
    print("="*60)

# ── STEP 1: Load Data ──────────────────────────────────────────────────────────
sep("STEP 1: Loading Customer Data")
DATA_RAW = BASE_DIR / "data" / "processed" / "customer_features.csv"
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Data file not found: {DATA_PATH}\nRun preprocessing first.")

df = pd.read_csv(DATA_PATH)
df_raw = pd.read_csv(DATA_RAW) if DATA_RAW.exists() else df

print(f"[OK] Loaded {len(df):,} customer records")

# ── STEP 2: CLV Calculation Logic (As per Project Plan) ──────────────────────
sep("STEP 2: CLV Calculation (Logic From Plan)")

# Avg Purchase Value = (Total Spend / Total Orders)
# Purchase Frequency = (Total Orders / Total Customers)
# Lifespan = 1 (Assumed)
# We use the raw 'monetary' and 'frequency' for calculation
df['purchase_value'] = df_raw.get('monetary', df['monetary'])
df['purchase_freq']  = df_raw.get('frequency', df['frequency'])
df['lifespan']       = 1.0

# Formula: CLV = Avg Value * Frequency * Lifespan
df['actual_clv'] = df['purchase_value'] * df['purchase_freq'] * df['lifespan']

# Use quantiles for classification to ensure classes exist in synthetic data
try:
    df['value_class'] = pd.qcut(df['actual_clv'], q=3, labels=['Low', 'Medium', 'High'])
except ValueError:
    df['value_class'] = 'Low'
    df.loc[df['actual_clv'] > df['actual_clv'].median(), 'value_class'] = 'High'

le = LabelEncoder()
df['value_label'] = le.fit_transform(df['value_class'])

print(f"Segment Breakdown:")
print(df['value_class'].value_counts())

print(f"[OK] CLV calculated using Plan Logic. Value Categories assigned.")

# ── STEP 3: Feature Engineering ───────────────────────────────────────────────
sep("STEP 3: Preparing Features")

DROP_COLS   = ["customer_id", "gender", "age_group", "monetary", "actual_clv", "value_class", "value_label", "purchase_value", "purchase_freq", "lifespan"]
feature_cols = [c for c in df.columns if c not in DROP_COLS]

X = df[feature_cols].fillna(0)
y_reg = df["actual_clv"]
y_clf = df["value_label"]

print(f"[OK] Features: {feature_cols}")

# ── STEP 4: Train-Test Split ──────────────────────────────────────────────────
# Regressor split
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X, y_reg, test_size=0.2, random_state=42)
# Classifier split
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_clf, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_c_sc = scaler.fit_transform(X_train_c)
X_test_c_sc  = scaler.transform(X_test_c)
joblib.dump(scaler, CLV_DIR / "scaler_clf.pkl")

# ── STEP 5: Regression Models (Predicting Value) ─────────────────────────────
sep("STEP 4: Training Regression Models (CLV value)")

# --- Model 1: Linear Regression ---
lr = LinearRegression()
lr.fit(X_train_r, y_train_r)
lr_preds = lr.predict(X_test_r)
lr_r2 = r2_score(y_test_r, lr_preds)

# --- Model 2: Random Forest Regressor (ADVANCED) ---
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_r, y_train_r)
rf_preds = rf.predict(X_test_r)
rf_r2 = r2_score(y_test_r, rf_preds)

print(f"LR R2: {lr_r2:.4f} | RF R2: {rf_r2:.4f}")
joblib.dump(rf, CLV_DIR / "best_model.pkl")

# ── STEP 6: Classification Models (Value Segment) ───────────────────────────
sep("STEP 5: Training Classification Models (Value Class)")

# --- Model 1: Logistic Regression (ADVANCED) ---
log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train_c_sc, y_train_c)
log_preds = log_reg.predict(X_test_c_sc)
log_acc = accuracy_score(y_test_c, log_preds)

print(f"Logistic Regression Accuracy: {log_acc*100:.2f}%")
joblib.dump(log_reg, CLV_DIR / "value_classifier.pkl")

# ── STEP 7: Performance Visuals (For Final Viva) ─────────────────────────────
sep("STEP 6: Generating Confusion Matrix & ROC plots")

# 1. Confusion Matrix
plt.figure(figsize=(8,6))
cm = confusion_matrix(y_test_c, log_preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', 
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.title('Value Classification: Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig(PLOT_DIR / "confusion_matrix.png")
plt.close()

# 2. ROC Curve (Simplifying for binary-style or using high-value indicator)
# For project report, we show binary ROC for 'High Value' vs Others
high_label_idx = int(le.transform(['High'])[0])
y_test_binary = np.where(y_test_c == high_label_idx, 1, 0)
log_probs = log_reg.predict_proba(X_test_c_sc)[:, high_label_idx]
fpr, tpr, _ = roc_curve(y_test_binary, log_probs)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8,6))
plt.plot(fpr, tpr, color='#cc0000', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='#333', lw=1, linestyle='--')
plt.title('Value Classification: ROC Curve (High Value)')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")
plt.savefig(PLOT_DIR / "roc_curve.png")
plt.close()

print(f"[OK] Plots saved to models/plots/")

# ── STEP 8: Save Metrics JSON ────────────────────────────────────────────────
sep("STEP 7: Saving Final Project Metrics")

metrics = {
    "R2_Score": round(rf_r2, 4),
    "Accuracy_MAPE": round(100 - (mean_absolute_error(y_test_r, rf_preds) / y_test_r.mean() * 100), 2),
    "Classification_Accuracy": round(log_acc * 100, 2),
    "ROC_AUC": round(roc_auc, 4),
    "best_model": "Random Forest Regressor",
    "trained_at": str(pd.Timestamp.now()),
    "segments": {
        "High": int(np.sum(df['value_class'] == 'High')),
        "Medium": int(np.sum(df['value_class'] == 'Medium')),
        "Low": int(np.sum(df['value_class'] == 'Low')),
    }
}

with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=4)

# ── STEP 9: Final Predictions ────────────────────────────────────────────────
sep("STEP 8: Generating Predictor Output")

df['clv_prediction'] = rf.predict(df[feature_cols])
df['value_class_predicted'] = le.inverse_transform(log_reg.predict(scaler.transform(df[feature_cols])))

pred_path = BASE_DIR / "data" / "processed" / "clv_predictions.csv"
df[['customer_id', 'actual_clv', 'clv_prediction', 'value_class', 'value_class_predicted']].to_csv(pred_path, index=False)
print(f"[OK] Full predictions saved to {pred_path.name}")

sep("EXECUTABLE PROJECT CODING COMPLETE")
