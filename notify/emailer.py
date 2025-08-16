# notify/emailer.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Load environment variables (from .env file if using python-dotenv)
from dotenv import load_dotenv
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_drop_alert(product_name, product_url, old_price, new_price, recipient_email):
    """
    Send an email alert when a price drop is detected.
    """
    try:
        subject = f"Price Drop Alert: {product_name}"
        body = f"""
        Good news! 🎉

        The product **{product_name}** has dropped in price.

        Old Price: ₹{old_price}
        New Price: ₹{new_price}

        Buy now: {product_url}
        """

        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, recipient_email, msg.as_string())

        print(f"✅ Email sent successfully to {recipient_email} for {product_name}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
