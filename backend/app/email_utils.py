import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .security import settings

def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using the SMTP settings from the .env file.
    """
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls() # Secure the connection
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"--- FAILED TO SEND EMAIL to {to_email}: {e} ---")
        # In a real app, you would log this error more robustly.
