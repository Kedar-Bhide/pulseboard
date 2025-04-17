import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.config import settings

client = WebClient(token=settings.SLACK_BOT_TOKEN)

def send_slack_dm(user_id: str, message: str):
    try:
        response = client.chat_postMessage(
            channel=user_id,
            text=message
        )
        return response
    except SlackApiError as e:
        print(f"Slack error: {e.response['error']}")
        return None