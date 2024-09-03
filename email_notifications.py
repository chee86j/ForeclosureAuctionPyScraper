import os
from dotenv import load_dotenv
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from the .env file
load_dotenv()

# Get email credentials from .env file
sender_email = os.getenv('SENDER_EMAIL')
recipient_email = os.getenv('RECIPIENT_EMAIL')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')

# Common SMTP server settings
    # smtp_server = "smtp.gmail.com"
    # smtp_server = "smtp.office365.com"
    # smtp_server = "smtp.mail.yahoo.com"
    # smtp_server = "You can obtain this from your domain or email service provider."
    
# Common SMTP port numbers
    # smtp_port = 587  # For TLS (Transport Layer Security)
    # smtp_port = 465  # For SSL (Secure Sockets Layer)
    # smtp_port = 25  # For non-secure connections

def send_email_notification(subject, body, to_email):
    """Send an email notification with the given subject and body to the specified email address."""
    
    # Prepare the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        print(f"Failed to send email: {e}")

# Example usage
if __name__ == "__main__":
    new_listings = "Property at 123 Main St.\nProperty at 456 Oak St."
    send_email_notification(
        subject='New Foreclosure Auction Listings',
        body=f"New auction listings found:\n{new_listings}",
        to_email=recipient_email
    )