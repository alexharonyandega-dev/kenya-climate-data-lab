import pandas as pd
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from sqlalchemy import create_engine

# Configuration from GitHub Secrets
API_URL = 'https://api.kenyaclimatelab.me'
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASS = os.getenv('SENDER_PASS')
DB_URL = os.getenv('DATABASE_URL')

def send_email(to_email, county, stress_value):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = f"🚨 Severe Drought Alert: {county}"
    
    body = f"""
    <h2>Severe Drought Alert for {county}</h2>
    <p>Our AI model has detected severe drought stress in <strong>{county}</strong> with a stress score of <strong>{stress_value:.2f}</strong>.</p>
    <p>Please take necessary action to protect crops and livestock.</p>
    <p>View the live dashboard for more details.</p>
    """
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Alert sent to {to_email} for {county}")
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")

print("🚀 Checking for severe drought alerts...")
# 1. Get the latest month from the API
try:
    all_data = requests.get(f'{API_URL}/all_data', timeout=60).json()
    if not all_data:
        print("No data available.")
        exit()
except Exception as e:
    print(f"API Error: {e}")
    exit()

latest_month = max([row['month_start'] for row in all_data])
severe_counties = [row for row in all_data if row['month_start'] == latest_month and row['stress_category'] == 'severe_stress']

if not severe_counties:
    print(f"✅ No severe drought detected for {latest_month}. No alerts sent.")
    exit()

print(f"⚠️ Severe drought detected in {len(severe_counties)} counties for {latest_month}.")

# 2. Get subscribers from the DB
engine = create_engine(DB_URL)
subs = pd.read_sql("SELECT email, county FROM subscribers", con=engine)

# 3. Match subscribers with severe counties
for _, sub in subs.iterrows():
    match = next((c for c in severe_counties if c['county'].lower() == sub['county'].lower()), None)
    if match:
        send_email(sub['email'], sub['county'], match['stress_avg'])
