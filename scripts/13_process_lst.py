import pandas as pd

print("⏳ Processing MODIS LST data...")
# FIX: Added encoding='latin-1' for GEE exports
df = pd.read_csv('data/raw/modis_lst_raw.csv', encoding='latin-1')
df = df.rename(columns={'ADM1_NAME': 'county', 'mean': 'lst_celsius'})
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

monthly_lst = df.groupby(['county', 'year', 'month'])['lst_celsius'].mean().reset_index()
master = pd.read_csv('data/processed/county_monthly_stress_v3.csv', parse_dates=['month_start'])
master = master.merge(monthly_lst, on=['county', 'year', 'month'], how='left')

def calc_lst_anomaly(group):
    return (group['lst_celsius'] - group['lst_celsius'].mean()) / group['lst_celsius'].std()

master['lst_anomaly'] = master.groupby('county', group_keys=False).apply(calc_lst_anomaly)
master.to_csv('data/processed/county_monthly_stress_v3.csv', index=False)
print("✅ LST integrated and anomaly calculated!")
