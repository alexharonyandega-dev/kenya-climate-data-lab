import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Set page config
st.set_page_config(
    page_title="Kenya Drought Monitor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/county_monthly_stress_v3.csv', parse_dates=['month_start'])
    return df

df = load_data()

# 3. Sidebar - County Selector
st.sidebar.header("Select a County")
all_counties = sorted(df['county'].unique())
selected_county = st.sidebar.selectbox("County", all_counties)

# Filter dataframe for the selected county
county_df = df[df['county'] == selected_county].sort_values('month_start')

# 4. Sidebar - Month Selector (Tuesday's Task)
st.sidebar.header("Select a Month")
available_months = county_df['month_start'].dt.strftime('%Y-%m').unique()
selected_month_str = st.sidebar.selectbox("Month", sorted(available_months, reverse=True))

# Convert selected month string back to datetime to match the dataframe
selected_month = pd.to_datetime(selected_month_str + '-01')
month_row = county_df[county_df['month_start'] == selected_month].iloc[0]

# 5. Main Header
st.title("🌾 Kenya Drought Monitor")
st.markdown(f"**Currently viewing: {selected_county} County — {selected_month_str}**")

# 6. KPI Metrics & Crop-Stage Context (Wednesday's Task)
st.subheader("Monthly Snapshot")
col1, col2, col3 = st.columns(3)

# Color mapping for the metric
cat_colors = {
    'severe_stress': '🔴',
    'moderate_stress': '🟠',
    'normal': '🟡',
    'good': '🟢',
    'very_good': '🟢'
}
cat_icon = cat_colors.get(month_row['stress_category'], '⚪')

col1.metric(
    label=f"{cat_icon} Composite Stress", 
    value=f"{month_row['stress_avg']:+.2f}",
    help="Standard deviations from normal. Below -1.25 is severe."
)
col2.metric(
    label="Crop-Weighted Stress", 
    value=f"{month_row['stress_weighted']:+.2f}",
    help="Adjusted for the maize crop stage. Weight of 0 means fallow."
)
col3.metric(
    label="Maize Stage", 
    value=str(month_row['crop_stage']).title(),
    help=f"Weight applied: {month_row['crop_stage_weight']:.1f}"
)

st.divider()

# 7. Display the Plotly Chart (Last 12 months leading up to selected month)
st.subheader("12-Month Stress Trend")
recent_12 = county_df[county_df['month_start'] <= selected_month].tail(12)

fig = px.bar(
    recent_12, 
    x='month_start', 
    y='stress_avg',
    color='stress_category',
    color_discrete_map={
        'severe_stress': '#dc2626',
        'moderate_stress': '#f59e0b',
        'normal': '#eab308',
        'good': '#22c55e',
        'very_good': '#16a34a'
    },
    labels={'month_start': 'Month', 'stress_avg': 'Stress Score'}
)
fig.add_hline(y=-1.25, line_dash='dot', line_color='red', annotation_text='Severe Threshold')

# FIXED: Replaced use_container_width with width='stretch'
st.plotly_chart(fig, width='stretch')

st.divider()

# 8. Display the FULL Data Table
st.subheader(f"Full Historical Data for {selected_county}")
st.dataframe(county_df[['month_start', 'stress_avg', 'stress_category', 'crop_stage']], width='stretch')

