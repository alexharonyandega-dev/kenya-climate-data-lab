import streamlit as st
import pandas as pd
import plotly.express as px
import xgboost as xgb
import json

st.set_page_config(page_title="Kenya Drought Monitor", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/county_monthly_stress_v3.csv', parse_dates=['month_start'])
    yield_df = pd.read_csv('data/processed/mock_yield_data.csv')
    df['year'] = df['month_start'].dt.year
    df = df.merge(yield_df, on=['county', 'year'], how='left')
    return df

@st.cache_resource
def load_model():
    model = xgb.XGBClassifier()
    model.load_model('app/drought_model.json')
    return model

@st.cache_data
def load_projections():
    with open('data/projection_coefs.json', 'r') as f:
        return json.load(f)

df = load_data()
model = load_model()
coefs = load_projections()

# --- FRESHNESS BADGE (Feedback Point #2) ---
latest_date = df['month_start'].max()
age_days = (pd.Timestamp.utcnow().tz_localize(None) - latest_date).days

if age_days > 45:
    st.error(f"⚠️ Data is {age_days} days old (through {latest_date:%b %Y}). The monthly refresh may have failed — treat readings as historical.")
else:
    st.caption(f"🟢 Data through **{latest_date:%B %Y}** · refreshed monthly")

st.sidebar.header("Select a County")
all_counties = sorted(df['county'].unique())
selected_county = st.sidebar.selectbox("County", all_counties)
county_df = df[df['county'] == selected_county].sort_values('month_start')

st.sidebar.header("Select a Month")
available_months = county_df['month_start'].dt.strftime('%Y-%m').unique()
# Auto-default to the latest month
default_index = list(available_months).index(latest_date.strftime('%Y-%m')) if latest_date.strftime('%Y-%m') in available_months else 0
selected_month_str = st.sidebar.selectbox("Month", sorted(available_months, reverse=True), index=default_index)

selected_month = pd.to_datetime(selected_month_str + '-01')
month_row = county_df[county_df['month_start'] == selected_month].iloc[0]

st.title('🌾 Kenya Drought Monitor')
st.markdown(f'**Currently viewing: {selected_county} County — {selected_month_str}**')

# --- ML PREDICTION & PROJECTION (Feedback Point #4) ---
features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight']
if month_row[features].isnull().any():
    prob = None
    pred_msg = 'Insufficient data'
else:
    input_data = month_row[features].values.reshape(1, -1)
    prob = model.predict_proba(input_data)[0][1] * 100
    pred_msg = 'High Risk 🔴' if prob > 50 else 'Low Risk 🟢'

st.subheader('Monthly Snapshot')
col1, col2, col3, col4, col5 = st.columns(5)

cat_colors = {'severe_stress': '🔴', 'moderate_stress': '🟠', 'normal': '🟡', 'good': '🟢', 'very_good': '🟢'}
cat_icon = cat_colors.get(month_row['stress_category'], '⚪')

col1.metric(label=f'{cat_icon} Current Stress', value=f"{month_row['stress_avg']:+.2f}")
col2.metric(label='Crop-Weighted Stress', value=f"{month_row['stress_weighted']:+.2f}")
col3.metric(label='Maize Stage', value=str(month_row['crop_stage']).title())

if prob is not None:
    col4.metric(label=f'Next Month Risk: {pred_msg}', value=f'{prob:.1f}%')
else:
    col4.metric(label='Next Month Risk', value='N/A')

spei_val = month_row.get('spei_12', None)
if pd.notna(spei_val):
    spei_str = f'{spei_val:+.2f}'
else:
    spei_str = 'N/A'
col5.metric(label='12-Mo SPEI', value=spei_str, help='Standardized Precipitation-Evapotranspiration Index. Below -1.0 indicates drought.')

# Experimental Projection
c = coefs.get(selected_county)
if c and c['r'] >= 0.3 and pd.notna(month_row['swvl1_mean_anomaly']):
    proj = c['a'] * month_row['swvl1_mean_anomaly'] + c['b']
    st.info(f"**Experimental Projection:** Next month's vegetation stress is projected to be **{proj:+.2f}σ** based on current soil moisture (r={c['r']}, n={c['n']}). *Signal only, not a validated forecast.*")

st.divider()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader('12-Month Stress Trend')
    recent_12 = county_df[county_df['month_start'] <= selected_month].tail(12)
    fig1 = px.bar(
        recent_12, x='month_start', y='stress_avg', color='stress_category',
        color_discrete_map={'severe_stress': '#dc2626', 'moderate_stress': '#f59e0b', 'normal': '#eab308', 'good': '#22c55e', 'very_good': '#16a34a'},
        labels={'month_start': 'Month', 'stress_avg': 'Stress Score'}
    )
    fig1.add_hline(y=-1.25, line_dash='dot', line_color='red', annotation_text='Severe Threshold')
    st.plotly_chart(fig1, width='stretch')

with col_chart2:
    st.subheader('Historical Yield vs Stress')
    scatter_data = county_df.dropna(subset=['yield_tonnes_ha', 'stress_avg'])
    fig2 = px.scatter(
        scatter_data, x='stress_avg', y='yield_tonnes_ha', 
        color='stress_category',
        color_discrete_map={'severe_stress': '#dc2626', 'moderate_stress': '#f59e0b', 'normal': '#eab308', 'good': '#22c55e', 'very_good': '#16a34a'},
        labels={'stress_avg': 'Stress Score (Anomaly)', 'yield_tonnes_ha': 'Yield (t/ha)'}
    )
    fig2.add_vline(x=-1.25, line_dash='dot', line_color='red')
    st.plotly_chart(fig2, width='stretch')

st.divider()

st.subheader(f"Full Historical Data for {selected_county}")
st.dataframe(county_df[['month_start', 'stress_avg', 'stress_category', 'crop_stage', 'yield_tonnes_ha']], width='stretch')
