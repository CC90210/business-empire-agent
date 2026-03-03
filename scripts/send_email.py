import os
import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, body):
    """
    Bravo Autonomous Email Engine
    Uses App Password for oasisaisolutions@gmail.com
    """
    gmail_user = os.environ.get("GMAIL_USER", "oasisaisolutions@gmail.com")
    gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not gmail_app_password:
        raise ValueError("GMAIL_APP_PASSWORD not set. Load from .env.agents.")
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_user, gmail_app_password)
            smtp.send_message(msg)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    # Example usage:
    # send_email("recipient@example.com", "OASIS AI Automation Lead", "We found a gap in your workflow.")
    pass
