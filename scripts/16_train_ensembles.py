import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib

print("🧠 Training ML Ensemble...")
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')

# Target: Next month's severe drought
df['next_month_severe'] = (df.groupby('county')['stress_category'].shift(-1) == 'severe_stress').astype(int)

# FIX: Use the core features that have complete data
features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight']
X = df[features].dropna()
y = df.loc[X.index, 'next_month_severe']

print(f"Training on {len(X)} valid samples.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the three models
clf1 = xgb.XGBClassifier(max_depth=4, n_estimators=100, learning_rate=0.1, eval_metric='auc')
clf2 = lgb.LGBMClassifier(max_depth=4, n_estimators=100, learning_rate=0.1, verbose=-1)
clf3 = RandomForestClassifier(max_depth=6, n_estimators=200, random_state=42)

# Create the Voting Ensemble
ensemble = VotingClassifier(
    estimators=[('xgb', clf1), ('lgb', clf2), ('rf', clf3)],
    voting='soft'
)

ensemble.fit(X_train, y_train)

y_pred = ensemble.predict(X_test)
y_prob = ensemble.predict_proba(X_test)[:, 1]
print(f"🎯 Ensemble Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"📈 Ensemble ROC-AUC:  {roc_auc_score(y_test, y_prob):.3f}")

# Save the ensemble
joblib.dump(ensemble, 'app/ensemble_model.pkl')
print("💾 Ensemble saved to app/ensemble_model.pkl")
