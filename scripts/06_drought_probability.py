import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import json

print("⏳ Loading data...")
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')

# 1. Shift the target variable by -1 to predict NEXT month's category
df['next_month_severe'] = (df.groupby('county')['stress_category'].shift(-1) == 'severe_stress').astype(int)

# 2. Select features (what we know TODAY to predict TOMORROW)
features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight']
X = df[features].dropna()
y = df.loc[X.index, 'next_month_severe']

# 3. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🧠 Training XGBoost Model...")
model = xgb.XGBClassifier(
    max_depth=3,
    n_estimators=100,
    learning_rate=0.1,
    objective='binary:logistic',
    eval_metric='auc'
)

model.fit(X_train, y_train)

# 4. Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]
acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print(f"✅ Model Trained!")
print(f"🎯 Accuracy: {acc:.2f}")
print(f"📈 ROC-AUC:  {auc:.2f}")

# 5. Save the model
model.save_model('app/drought_model.json')
print("💾 Model saved to app/drought_model.json")
