import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.core.config import settings

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
    
def build_checkin_modal(question_text: str):
    return {
        "type": "modal",
        "callback_id": "submit_checkin_modal",
        "title": {"type": "plain_text", "text": "Daily Check-In"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Today's Question:*\n{question_text}"}
            },
            {
                "type": "input",
                "block_id": "answer_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "answer_input",
                    "multiline": True
                },
                "label": {"type": "plain_text", "text": "Your Answer"}
            }
        ]
    }