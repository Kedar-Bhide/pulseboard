from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json
from app.core.slack import build_checkin_modal
from app.services.crud_question import get_today_question
from app.database import SessionLocal
from app.core.slack import client


router = APIRouter()

@router.post("/interactions")
async def slack_interactions(request: Request):
    form_data = await request.form()
    payload = json.loads(form_data["payload"])
    user_id = payload["user"]["id"]
    trigger_id = payload.get("trigger_id")

    # Handle button click → open modal
    if payload["type"] == "block_actions":
        db = SessionLocal()
        question = get_today_question(db)
        db.close()

        modal_view = build_checkin_modal(question.content if question else "No question found today.")
        client.views_open(trigger_id=trigger_id, view=modal_view)
        return JSONResponse(content={})

    return JSONResponse(content={"text": "Unhandled Slack interaction"})