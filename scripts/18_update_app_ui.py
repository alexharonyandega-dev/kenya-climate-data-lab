from pathlib import Path

p = Path("app/app.py")
text = p.read_text()

# 1. Swap XGBoost for Joblib
if "import joblib" not in text:
    text = text.replace("import xgboost as xgb", "import joblib")

# 2. Update the model loading logic
old_model_load = """    model = xgb.XGBClassifier()
    model.load_model('app/drought_model.json')"""
new_model_load = """    model = joblib.load('app/ensemble_model.pkl')"""
text = text.replace(old_model_load, new_model_load)

# 3. Add the SHAP expander right below the KPI cards
shap_block = """
with st.expander("🧠 Why this prediction? (AI Explainability)"):
    try:
        with open('app/shap_values.json', 'r') as f:
            shaps = json.load(f)
        st.write("Feature contributions to the risk score:")
        shap_df = pd.DataFrame(list(shaps.items()), columns=['Feature', 'Impact']).set_index('Feature')
        st.bar_chart(shap_df)
    except Exception:
        st.write("SHAP values not generated yet.")
"""

if "Why this prediction?" not in text:
    text = text.replace("st.divider()\ncol_chart1, col_chart2 = st.columns(2)", shap_block + "\nst.divider()\ncol_chart1, col_chart2 = st.columns(2)")

p.write_text(text)
print("✅ Streamlit UI updated successfully.")
