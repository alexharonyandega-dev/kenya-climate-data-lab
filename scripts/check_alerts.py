import pandas as pd
import json
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

THRESHOLD = -1.25
DATA_PATH = 'data/processed/county_monthly_stress_v3.csv'
STATE_PATH = 'data/alert_state.json'

def send_email(to_email, subject, body):
    # In production, this uses SMTP credentials from GitHub Secrets.
    # For now, it prints to the console so the script runs anywhere.
    smtp_user = os.environ.get('SMTP_USER', 'dummy@gmail.com')
    smtp_pass = os.environ.get('SMTP_PASS', 'dummy_password')
    
    if smtp_user == 'dummy@gmail.com':
        print(f"📧 [SIMULATED EMAIL] To: {to_email} | Subject: {subject}")
        print(f"Body:\n{body}\n{'-'*40}")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"✅ Sent email to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    print("🔍 Checking for threshold alerts...")
    df = pd.read_csv(DATA_PATH)
    latest_month = df['month_start'].max()
    
    # Filter for severe drought this month
    flagged = df[(df['month_start'] == latest_month) & (df['stress_avg'] < THRESHOLD)]
    
    # Load state
    with open(STATE_PATH, 'r') as f:
        state = json.load(f)
        
    # Load recipients
    recipients = pd.read_csv('data/alert_recipients.csv')
    default_email = recipients[recipients['county'] == 'ALL']['email'].iloc[0]
    
    new_alerts = []
    
    for row in flagged.itertuples():
        county = row.county
        # Check if we already alerted this county for this month
        if state.get(county) != latest_month:
            new_alerts.append(row)
            state[county] = latest_month
            
            # Find specific recipient or send to default
            county_recipients = recipients[recipients['county'] == county]
            to_email = county_recipients['email'].iloc[0] if not county_recipients.empty else default_email
            
            subject = f"🚨 SEVERE DROUGHT ALERT: {county} ({latest_month})"
            body = f"Warning: {county} County has crossed the severe drought threshold.\n\nStress Score: {row.stress_avg:.2f}\nCategory: {row.stress_category}\nMonth: {latest_month}\n\nPlease log in to the dashboard for details."
            send_email(to_email, subject, body)

    # Always send a monthly digest (so you know the job ran)
    digest_subject = f"📊 Monthly Drought Digest ({latest_month})"
    if new_alerts:
        digest_body = f"The monthly check is complete. {len(new_alerts)} NEW counties crossed the severe threshold this month."
    else:
        digest_body = f"The monthly check is complete. No new counties crossed the severe threshold this month."
    
    send_email(default_email, digest_subject, digest_body)

    # Save updated state
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, indent=4)
        
    print("✅ Alert check complete.")

if __name__ == "__main__":
    main()
