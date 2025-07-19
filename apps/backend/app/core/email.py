import resend
from app.core.config import settings

resend.api_key = settings.OPENAI_API_KEY

def send_email(to_email: str, subject: str, body: str):
    try:
        resend.Emails.send({
            "from": "Pulseboard <noreply@pulseboard.dev>",  # You can configure domain later
            "to": to_email,
            "subject": subject,
            "html": f"<p>{body}</p>"
        })
    except Exception as e:
        print(f"Email send failed: {e}")