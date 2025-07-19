import hmac
import hashlib
import time
from fastapi import Request, HTTPException
from app.core.config import settings

def verify_slack_request(request: Request, body: bytes):
    slack_signature = request.headers.get("X-Slack-Signature", "")
    slack_timestamp = request.headers.get("X-Slack-Request-Timestamp", "")

    if abs(time.time() - int(slack_timestamp)) > 60 * 5:
        raise HTTPException(status_code=403, detail="Slack request too old")

    basestring = f"v0:{slack_timestamp}:{body.decode('utf-8')}"
    computed_signature = "v0=" + hmac.new(
        settings.SLACK_SIGNING_SECRET.encode(),
        basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_signature, slack_signature):
        raise HTTPException(status_code=403, detail="Invalid Slack signature")