import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.config import settings

client = WebClient(token=settings.SLACK_BOT_TOKEN)

def send_slack_dm(user_id: str, message: str, include_button: bool = False):
    try:
        blocks = [
            {"type": "section", "text": {"type": "mrkdwn", "text": message}},
        ]
        if include_button:
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Check In Now"},
                        "url": "https://yourfrontend.com/checkin",  # replace with real link
                        "style": "primary"
                    }
                ]
            })

        response = client.chat_postMessage(
            channel=user_id,
            text=message,
            blocks=blocks if include_button else None
        )
        return response
    except SlackApiError as e:
        print(f"Slack error: {e.response['error']}")
        return None