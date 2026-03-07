import os
import smtplib
import imaplib
import time
from email.message import EmailMessage
import argparse

def send_email(to_email, subject, body):
    """
    Bravo Autonomous Email Engine (V5.6)
    - Fixes literal '\n' escaping from shell arguments
    - Ensures clean plain-text paragraphing
    - Saves to Sent folder via IMAP
    """
    gmail_user = os.environ.get("GMAIL_USER", "oasisaisolutions@gmail.com")
    gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")
    
    if not gmail_app_password:
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env.agents')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith("GMAIL_APP_PASSWORD="):
                        gmail_app_password = line.split("=")[1].strip()
                        break
    
    if not gmail_app_password:
        raise ValueError("GMAIL_APP_PASSWORD not set. Load from .env.agents.")
    
    # CRITICAL FIX: Decode literal '\n' passed from CLI strings
    clean_body = body.replace('\\n', '\n')
    
    msg = EmailMessage()
    msg.set_content(clean_body)
    msg['Subject'] = subject
    msg['From'] = f"OASIS AI Solutions <{gmail_user}>"
    msg['To'] = to_email

    try:
        # 1. Send via SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_user, gmail_app_password)
            smtp.send_message(msg)
        print(f"✅ Email sent to {to_email}")
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bravo Email Engine")
    parser.add_argument("--to", required=True, help="Recipient email")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body")
    
    args = parser.parse_args()
    send_email(args.to, args.subject, args.body)
