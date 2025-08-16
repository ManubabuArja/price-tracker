# notify/emailer.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_drop_alert(email: str, product_name: str, url: str, current_price: float):
    """
    Send price drop alert email
    """
    if not email:
        print(f"⚠️ No email configured for {product_name}")
        return False
    
    try:
        # Email configuration
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        if not all([sender_email, sender_password]):
            print("⚠️ Email configuration incomplete. Set SENDER_EMAIL and SENDER_PASSWORD in .env file")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = f"💰 Price Drop Alert: {product_name}"
        
        # Email body
        body = f"""
        <html>
        <body>
            <h2>🎉 Price Drop Alert!</h2>
            <p><strong>Product:</strong> {product_name}</p>
            <p><strong>Current Price:</strong> ₹{current_price:.2f}</p>
            <p><strong>Product URL:</strong> <a href="{url}">{url}</a></p>
            <br>
            <p>Hurry up! The price has dropped to your target price or below.</p>
            <hr>
            <p><small>This alert was sent by your Price Tracker application.</small></p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        
        print(f"✅ Price drop alert email sent to {email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email alert: {e}")
        return False
