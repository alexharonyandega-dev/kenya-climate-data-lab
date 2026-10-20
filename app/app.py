import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import joblib
import shap
import json

st.set_page_config(page_title="Kenya Drought Monitor", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
@st.cache_data(ttl=3600)
def load_data():
    import requests
    import time
    import os
    API_URL = 'https://api.kenyaclimatelab.me'

    # 1. Try fetching from API with retries
    api_success = False
    for attempt in range(3):
        try:
            with st.spinner(f'Waking up the cloud database (Attempt {attempt+1}/3)...'):
                res = requests.get(f'{API_URL}/all_data', timeout=90)
                if res.status_code == 200:
                    data = res.json()
                    df = pd.DataFrame(data)
                    if not df.empty and 'month_start' in df.columns:
                        df['month_start'] = pd.to_datetime(df['month_start'])
                        api_success = True
                        break
        except Exception:
            pass
        time.sleep(3)

    # 2. Fallback to local CSV if API fails
    if not api_success:
        st.warning('⚠️ Live API is unreachable. Falling back to local CSV data.')
        df = pd.read_csv('data/processed/county_monthly_stress_v3.csv', parse_dates=['month_start'])

    # 3. Bulletproof Merge with Mock Yield Data
    yield_path = 'data/processed/mock_yield_data.csv'
    if os.path.exists(yield_path):
        try:
            yield_df = pd.read_csv(yield_path)
            
            # Standardize date column in mock data
            if 'month_start' not in yield_df.columns:
                if 'date' in yield_df.columns:
                    yield_df['month_start'] = pd.to_datetime(yield_df['date'])
                elif 'year' in yield_df.columns and 'month' in yield_df.columns:
                    yield_df['month_start'] = pd.to_datetime(yield_df['year'].astype(str) + '-' + yield_df['month'].astype(str) + '-01')
            
            # Remove timezones and force to year-month-day for exact matching
            yield_df['month_start'] = pd.to_datetime(yield_df['month_start']).dt.tz_localize(None).dt.floor('D')
            df['month_start'] = pd.to_datetime(df['month_start']).dt.tz_localize(None).dt.floor('D')
            
            # Force county names to match exactly (Title Case, stripped of spaces)
            yield_df['county'] = yield_df['county'].astype(str).str.strip().str.title()
            df['county'] = df['county'].astype(str).str.strip().str.title()
            
            # Merge
            df = df.merge(yield_df, on=['county', 'month_start'], how='left')
            
        except Exception as e:
            st.error(f"Merge Error Details: {e}")
            
    # 4. Add year and month columns for filtering
    df['year'] = df['month_start'].dt.year
    df['month'] = df['month_start'].dt.month
    return df

@st.cache_resource
def load_model():
    return joblib.load('app/ensemble_model.pkl')

@st.cache_data
def load_shap():
    try:
        with open('app/shap_values.json', 'r') as f:
            return json.load(f)
    except:
        return None

@st.cache_data
def load_projections():
    with open('data/projection_coefs.json', 'r') as f:
        return json.load(f)

df = load_data()
model = load_model()
coefs = load_projections()
shaps = load_shap()

# --- FRESHNESS BADGE ---
latest_date = df['month_start'].max()
# FIXED: Deprecation warning resolved
age_days = (pd.Timestamp.now(tz='UTC').tz_localize(None) - latest_date).days

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
default_index = list(available_months).index(latest_date.strftime('%Y-%m')) if latest_date.strftime('%Y-%m') in available_months else 0
selected_month_str = st.sidebar.selectbox("Month", sorted(available_months, reverse=True), index=default_index)

selected_month = pd.to_datetime(selected_month_str + '-01')
month_row = county_df[county_df['month_start'] == selected_month].iloc[0]

st.title('🌾 Kenya Drought Monitor')
st.markdown(f'**Currently viewing: {selected_county} County — {selected_month_str}**')

# --- ML PREDICTION & PROJECTION ---
features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight', 'spei_12', 'lst_anomaly']
if month_row[features].isnull().any():
    prob = None
    pred_msg = 'Insufficient data'
else:
    input_data = pd.DataFrame([month_row[features]], columns=features)
    prob = model.predict_proba(input_data)[0][1] * 100
    pred_msg = 'High Risk 🔴' if prob > 50 else 'Low Risk 🟢'

st.subheader('Monthly Snapshot')




@st.cache_data(ttl=86400)
def load_geojson():
    import requests
    url = 'https://raw.githubusercontent.com/wmgeolab/geoBoundaries/main/releaseData/gbOpen/KEN/ADM1/geoBoundaries-KEN-ADM1_simplified.geojson'
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

# --- Interactive Map with Time Slider ---
st.subheader("🗺️ Interactive Drought Map")
st.write("Drag the slider to watch drought stress evolve over time. Click a county to update the dashboard.")

import json

@st.cache_data(ttl=86400)
def load_base_geojson():
    import requests
    res = requests.get('https://api.kenyaclimatelab.me/base_map', timeout=60)
    res.raise_for_status()
    return res.json()

geojson_data = load_base_geojson()

# Create the time slider
all_months = sorted(df['month_start'].dt.strftime('%Y-%m').unique())
if len(all_months) > 0:
    selected_month_str = st.slider(
        "Select Month for Map",
        min_value=all_months[0],
        max_value=all_months[-1],
        value=all_months[-1],
        step=1
    )
    
    # Filter the cached dataframe for the selected month
    map_month_dt = pd.to_datetime(selected_month_str)
    map_data = df[df['month_start'] == map_month_dt].copy()
    
    # Create Folium Map
    m = folium.Map(location=[-1.286389, 36.817223], zoom_start=6, tiles='Esri.WorldGrayCanvas')
    
    # Inject the data into the geojson properties for this specific month
    for feature in geojson_data['features']:
        c_name = feature['properties'].get('shapeName')
        row = map_data[map_data['county'].str.title() == c_name.title()] if c_name else pd.DataFrame()
        
        if not row.empty:
            r = row.iloc[0]
            feature['properties']['stress_val'] = r['stress_avg']
            feature['properties']['cat'] = r['stress_category']
            feature['properties']['vci'] = r.get('vci', 'N/A')
            feature['properties']['spei'] = r.get('spei_12', 'N/A')
        else:
            feature['properties']['stress_val'] = None
            feature['properties']['cat'] = 'no_data'
            feature['properties']['vci'] = 'N/A'
            feature['properties']['spei'] = 'N/A'

    def style_fn(feature):
        stress = feature['properties'].get('stress_val')
        if stress is None:
            fill = '#cccccc'
        elif stress <= -1.25:
            fill = '#dc2626' # Severe
        elif stress <= -0.5:
            fill = '#f59e0b' # Moderate
        elif stress <= 0.5:
            fill = '#eab308' # Normal
        else:
            fill = '#22c55e' # Good
            
        if feature['properties'].get('shapeName') == selected_county:
            return {'fillColor': fill, 'color': '#3b82f6', 'weight': 4, 'fillOpacity': 0.7}
        return {'fillColor': fill, 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}

    folium.GeoJson(
        geojson_data,
        style_function=style_fn,
        tooltip=folium.GeoJsonTooltip(
            fields=['shapeName', 'stress_val', 'cat', 'vci', 'spei'],
            aliases=['County:', 'Stress:', 'Category:', 'VCI:', 'SPEI-12:'],
            localize=True
        )
    ).add_to(m)

    # Render map and handle clicks
    map_output = st_folium(m, width=1000, height=500, returned_objects=["last_active_drawing"], key=f"map_{selected_month_str}")
    
    if map_output["last_active_drawing"]:
        clicked_county = map_output["last_active_drawing"]["properties"]["shapeName"]
        if clicked_county != selected_county:
            st.session_state["selected_county"] = clicked_county
            st.rerun()
else:
    st.warning("No map data available.")
col1, col2, col3, col4, col5 = st.columns(5)

cat_colors = {'severe_stress': '🔴', 'moderate_stress': '🟠', 'normal': '🟡', 'good': '🟢', 'very_good': '🟢'}
cat_icon = cat_colors.get(month_row['stress_category'], '⚪')

col1.metric(label=f'{cat_icon} Current Stress', value=f"{month_row['stress_avg']:+.2f}")
stress_w = month_row.get('stress_weighted', None)
col2.metric(label='Crop-Weighted Stress', value=f'{stress_w:+.2f}' if pd.notna(stress_w) else 'N/A')

vci_val = month_row.get('vci', None)
col3.metric(label='VCI (0-100)', value=f'{vci_val:.1f}' if pd.notna(vci_val) else 'N/A', help='Vegetation Condition Index. Below 35 indicates drought.')

if prob is not None:
    col4.metric(label=f'Next Month Risk: {pred_msg}', value=f'{prob:.1f}%')
else:
    col4.metric(label='Next Month Risk', value='N/A')

spei_val = month_row.get('spei_12', None)
spei_str = f'{spei_val:+.2f}' if pd.notna(spei_val) else 'N/A'
col5.metric(label='12-Mo SPEI', value=spei_str, help='Standardized Precipitation-Evapotranspiration Index. Below -1.0 indicates drought.')

# Experimental Projection
c = coefs.get(selected_county)
if c and c['r'] >= 0.3 and pd.notna(month_row['swvl1_mean_anomaly']):
    proj = c['a'] * month_row['swvl1_mean_anomaly'] + c['b']
    st.info(f"**Experimental Projection:** Next month's vegetation stress is projected to be **{proj:+.2f}σ** based on current soil moisture (r={c['r']}, n={c['n']}). *Signal only, not a validated forecast.*")

# SHAP Explanations
try:
    xgb_model = model.estimators_[0]
    explainer = shap.TreeExplainer(xgb_model)
except Exception:
    explainer = None

if explainer is not None and not month_row[features].isna().any():
    with st.expander("🧠 Why this prediction? (AI Explainability)"):
        st.write("Feature contributions (positive = pushes toward drought):")
        row_df = pd.DataFrame([month_row[features].values], columns=features)
        sv = explainer.shap_values(row_df)
        if isinstance(sv, list):
            sv = sv[1][0]
        elif sv.ndim > 1:
            sv = sv[0]
        shap_df = pd.DataFrame({'Feature': features, 'Impact': sv.flatten()}).set_index('Feature')
        st.bar_chart(shap_df)

st.divider()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader('12-Month Stress Trend')
    recent_12 = county_df[county_df['month_start'] <= selected_month].tail(12)
    # FIXED: Using string dates to prevent the axis bug
    recent_12['month_str'] = recent_12['month_start'].dt.strftime('%b %Y')
    fig1 = px.bar(
        recent_12, x='month_str', y='stress_avg', color='stress_category',
        color_discrete_map={'severe_stress': '#dc2626', 'moderate_stress': '#f59e0b', 'normal': '#eab308', 'good': '#22c55e', 'very_good': '#16a34a'},
        labels={'month_str': 'Month', 'stress_avg': 'Stress Score'}
    )
    fig1.add_hline(y=-1.25, line_dash='dot', line_color='red', annotation_text='Severe Threshold')
    st.plotly_chart(fig1, width='stretch')

with col_chart2:
    st.subheader('Historical Yield vs Stress')
    
    if 'yield_tonnes_ha' in county_df.columns and not county_df['yield_tonnes_ha'].isna().all():
        scatter_data = county_df.dropna(subset=['yield_tonnes_ha', 'stress_avg'])
        
        if not scatter_data.empty:
            fig2 = px.scatter(
                scatter_data, x='stress_avg', y='yield_tonnes_ha',
                color='stress_category',
                color_discrete_map={'severe_stress': '#dc2626', 'moderate_stress': '#f59e0b', 'normal': '#eab308', 'good': '#22c55e', 'very_good': '#16a34a'},
                labels={'stress_avg': 'Stress Score (Anomaly)', 'yield_tonnes_ha': 'Yield (t/ha)'}
            )
            fig2.add_vline(x=-1.25, line_dash='dot', line_color='red')
            st.plotly_chart(fig2, width='stretch')
        else:
            st.info('No overlapping yield and stress data for this county.')
    else:
        st.info('Yield data is currently unavailable for this dataset.')

st.divider()
st.subheader(f"Full Historical Data for {selected_county}")
display_cols = ['month_start', 'stress_avg', 'stress_category', 'crop_stage', 'vci', 'spei_12']
if 'yield_tonnes_ha' in county_df.columns:
    display_cols.insert(4, 'yield_tonnes_ha')
st.dataframe(county_df[display_cols], width='stretch')

st.divider()
st.subheader("📬 Subscribe to Drought Alerts")
st.write("Get an automated email if your selected county enters a severe drought.")
with st.form("subscription_form"):
    sub_email = st.text_input("Email Address")
    sub_county = st.selectbox("County", df['county'].unique())
    submit_btn = st.form_submit_button("Subscribe")
    
    if submit_btn:
        if sub_email:
            import requests
            try:
                res = requests.post('https://api.kenyaclimatelab.me/subscribe', json={"email": sub_email, "county": sub_county})
                if res.status_code == 200:
                    st.success(f"✅ Successfully subscribed {sub_email} to {sub_county} alerts!")
                else:
                    st.error(f"API Error ({res.status_code}): {res.text}")
            except Exception as e:
                st.error(f"API Error: {e}")
        else:
            st.warning("Please enter a valid email.")
