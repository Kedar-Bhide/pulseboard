from app.core.celery_app import celery_app
from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="send_welcome_email")
def send_welcome_email(email: str, full_name: str):
    """Send welcome email to new users"""
    try:
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_USER
        msg["To"] = email
        msg["Subject"] = "Welcome to PulseBoard!"

        body = f"""
        Hi {full_name},

        Welcome to PulseBoard! We're excited to have you on board.

        Get started by:
        1. Completing your profile
        2. Joining your team
        3. Starting your first check-in

        Best regards,
        The PulseBoard Team
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Welcome email sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {email}: {str(e)}")
        raise

@celery_app.task(name="send_reminder_email")
def send_reminder_email(email: str, full_name: str, days_missed: int):
    """Send reminder email to users who haven't checked in"""
    try:
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_USER
        msg["To"] = email
        msg["Subject"] = f"Reminder: {days_missed} days since your last check-in"

        body = f"""
        Hi {full_name},

        We noticed you haven't checked in for {days_missed} days.
        Your team is waiting for your update!

        Click here to check in now: {settings.FRONTEND_URL}/check-in

        Best regards,
        The PulseBoard Team
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Reminder email sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send reminder email to {email}: {str(e)}")
        raise 