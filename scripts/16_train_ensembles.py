import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib

print("🧠 Training ML Ensemble (5-feature model)...")
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')

# Target: next month's severe drought
df['next_month_severe'] = (df.groupby('county')['stress_category'].shift(-1) == 'severe_stress').astype(int)

# 5 core features — SPEI re-added (4,277 valid rows), LST still excluded (only 96)
features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight', 'spei_12', 'lst_anomaly']
X = df[features].dropna()
y = df.loc[X.index, 'next_month_severe']

print(f"Training on {len(X)} valid samples with {len(features)} features.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf1 = xgb.XGBClassifier(max_depth=4, n_estimators=100, learning_rate=0.1, eval_metric='auc')
clf2 = lgb.LGBMClassifier(max_depth=4, n_estimators=100, learning_rate=0.1, verbose=-1)
clf3 = RandomForestClassifier(max_depth=6, n_estimators=200, random_state=42)

ensemble = VotingClassifier(
    estimators=[('xgb', clf1), ('lgb', clf2), ('rf', clf3)],
    voting='soft'
)

ensemble.fit(X_train, y_train)
y_pred = ensemble.predict(X_test)
y_prob = ensemble.predict_proba(X_test)[:, 1]

print(f"🎯 Accuracy : {accuracy_score(y_test, y_pred):.3f}")
print(f"📈 ROC-AUC  : {roc_auc_score(y_test, y_prob):.3f}")
joblib.dump(ensemble, 'app/ensemble_model.pkl')
print("💾 Saved to app/ensemble_model.pkl")
