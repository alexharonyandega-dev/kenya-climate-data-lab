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
    # Fetch from live API
    API_URL = 'https://api.kenyaclimatelab.me'
    try:
        res = requests.get(f'{API_URL}/all_data', timeout=60)
        df = pd.DataFrame(res.json())
        df['month_start'] = pd.to_datetime(df['month_start'])
    except Exception as e:
        st.error(f'API Error: {e}')
        df = pd.DataFrame()
    yield_df = pd.read_csv('data/processed/mock_yield_data.csv')
    df['year'] = df['month_start'].dt.year
    df = df.merge(yield_df, on=['county', 'year'], how='left')
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
features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight', 'spei_12']
if month_row[features].isnull().any():
    prob = None
    pred_msg = 'Insufficient data'
else:
    input_data = pd.DataFrame([month_row[features]], columns=features)
    prob = model.predict_proba(input_data)[0][1] * 100
    pred_msg = 'High Risk 🔴' if prob > 50 else 'Low Risk 🟢'

st.subheader('Monthly Snapshot')




# --- Elite Interactive Map ---
st.subheader("🗺️ Interactive Drought Map")
st.write("Hover over any county for instant data. Click to update the dashboard.")

import json
with open('data/external/kenya_counties.geojson', 'r') as f:
    geojson_data = json.load(f)

map_data = df[df['month_start'] == selected_month].copy()

# Inject rich data into the GeoJSON properties for the tooltip
props = map_data.set_index('county')[['stress_avg', 'vci', 'spei_12']].to_dict('index')
for feature in geojson_data['features']:
    c_name = feature['properties'].get('shapeName')
    if c_name in props:
        feature['properties']['stress_str'] = f"{props[c_name]['stress_avg']:.2f}" if pd.notna(props[c_name]['stress_avg']) else 'N/A'
        feature['properties']['vci_str'] = f"{props[c_name]['vci']:.1f}" if pd.notna(props[c_name]['vci']) else 'N/A'
        feature['properties']['spei_str'] = f"{props[c_name]['spei_12']:.2f}" if pd.notna(props[c_name]['spei_12']) else 'N/A'

# Center map on the currently selected county
# (Approximated by taking the mean latitude/longitude of the selected county's geometry)
center_lat, center_lon = -1.286389, 36.817223 # Default: Kenya center
for feature in geojson_data['features']:
    if feature['properties'].get('shapeName') == selected_county:
        try:
            # Very basic centroid approximation from the bounding box
            coords = feature['geometry']['coordinates'][0]
            lats = [c[1] for c in coords]
            lons = [c[0] for c in coords]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
        except Exception:
            pass
        break

m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles='Esri.WorldGrayCanvas')

# Layer 1: The Heatmap Colors
folium.Choropleth(
    geo_data=geojson_data,
    name='choropleth',
    data=map_data,
    columns=['county', 'stress_avg'],
    key_on='feature.properties.shapeName',
    fill_color='RdYlGn',
    fill_opacity=0.7,
    line_opacity=0.1,
    legend_name='Drought Stress (Negative = Severe)'
).add_to(m)

# Layer 2: The Interactive Layer (Hover Tooltips & Click Borders)
def style_fn(feature):
    if feature['properties'].get('shapeName') == selected_county:
        return {'fillColor': '#00000000', 'color': '#3b82f6', 'weight': 4} # Bold blue border for active
    return {'fillColor': '#00000000', 'color': '#000000', 'weight': 0.5}

folium.GeoJson(
    geojson_data,
    style_function=style_fn,
    tooltip=folium.GeoJsonTooltip(
        fields=['shapeName', 'stress_str', 'vci_str', 'spei_str'],
        aliases=['County:', 'Stress:', 'VCI:', 'SPEI-12:'],
        localize=True,
        sticky=False
    )
).add_to(m)

map_output = st_folium(m, width=1000, height=500, returned_objects=["last_active_drawing"])

if map_output["last_active_drawing"]:
    clicked_county = map_output["last_active_drawing"]["properties"]["shapeName"]
    if clicked_county != selected_county:
        st.session_state["selected_county"] = clicked_county
        st.rerun()

col1, col2, col3, col4, col5 = st.columns(5)

cat_colors = {'severe_stress': '🔴', 'moderate_stress': '🟠', 'normal': '🟡', 'good': '🟢', 'very_good': '🟢'}
cat_icon = cat_colors.get(month_row['stress_category'], '⚪')

col1.metric(label=f'{cat_icon} Current Stress', value=f"{month_row['stress_avg']:+.2f}")
col2.metric(label='Crop-Weighted Stress', value=f"{month_row['stress_weighted']:+.2f}")

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
st.dataframe(county_df[['month_start', 'stress_avg', 'stress_category', 'crop_stage', 'yield_tonnes_ha', 'vci', 'spei_12']], width='stretch')



