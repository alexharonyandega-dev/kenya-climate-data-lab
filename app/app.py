import streamlit as st
import pandas as pd
import plotly.express as px
import xgboost as xgb

st.set_page_config(page_title="Kenya Drought Monitor", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/county_monthly_stress_v3.csv', parse_dates=['month_start'])
    yield_df = pd.read_csv('data/processed/mock_yield_data.csv')
    # Merge yield data on county and year
    df['year'] = df['month_start'].dt.year
    df = df.merge(yield_df, on=['county', 'year'], how='left')
    return df

@st.cache_resource
def load_model():
    model = xgb.XGBClassifier()
    model.load_model('app/drought_model.json')
    return model

df = load_data()
model = load_model()

st.sidebar.header("Select a County")
all_counties = sorted(df['county'].unique())
selected_county = st.sidebar.selectbox("County", all_counties)
county_df = df[df['county'] == selected_county].sort_values('month_start')

st.sidebar.header("Select a Month")
available_months = county_df['month_start'].dt.strftime('%Y-%m').unique()
selected_month_str = st.sidebar.selectbox("Month", sorted(available_months, reverse=True))
selected_month = pd.to_datetime(selected_month_str + '-01')
month_row = county_df[county_df['month_start'] == selected_month].iloc[0]

st.title('🌾 Kenya Drought Monitor')
st.markdown(f'**Currently viewing: {selected_county} County — {selected_month_str}**')

features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight']
if month_row[features].isnull().any():
    prob = 'N/A'
    pred_msg = 'Insufficient data'
else:
    input_data = month_row[features].values.reshape(1, -1)
    prob = model.predict_proba(input_data)[0][1] * 100
    pred_msg = 'High Risk 🔴' if prob > 50 else 'Low Risk 🟢'

st.subheader('Monthly Snapshot')
col1, col2, col3, col4 = st.columns(4)

cat_colors = {'severe_stress': '🔴', 'moderate_stress': '🟠', 'normal': '🟡', 'good': '🟢', 'very_good': '🟢'}
cat_icon = cat_colors.get(month_row['stress_category'], '⚪')

col1.metric(label=f'{cat_icon} Current Stress', value=f"{month_row['stress_avg']:+.2f}")
col2.metric(label='Crop-Weighted Stress', value=f"{month_row['stress_weighted']:+.2f}")
col3.metric(label='Maize Stage', value=str(month_row['crop_stage']).title())
if prob != 'N/A':
    col4.metric(label=f'Next Month Risk: {pred_msg}', value=f'{prob:.1f}%')
else:
    col4.metric(label='Next Month Risk', value=prob)

st.divider()

# --- DUAL VIEW SECTION ---
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
    # Scatter plot of all months for this county vs yield
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
