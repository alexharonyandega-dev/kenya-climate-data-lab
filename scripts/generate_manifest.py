import json
import pandas as pd
from datetime import datetime
import subprocess
import os

def get_git_sha():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
    except Exception:
        return "unknown"

def main():
    print("📝 Generating run manifest...")
    df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')
    latest_month = df['month_start'].max()
    
    manifest = {
        "run_timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "target_month": latest_month,
        "total_rows": len(df),
        "counties_count": df['county'].nunique(),
        "git_sha": get_git_sha(),
        "source_latencies": {
            "chirps": "~3 seconds (simulated)",
            "era5": "~5 seconds (simulated)"
        },
        "data_quality": {
            "null_stress_avg": int(df['stress_avg'].isnull().sum()),
            "null_ndvi": int(df['ndvi_anomaly'].isnull().sum())
        }
    }
    
    filename = f"metrics/refresh_runs/{latest_month[:7]}.json"
    with open(filename, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    print(f"✅ Manifest saved to {filename}")

if __name__ == "__main__":
    main()
