from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json
from app.core.slack import build_checkin_modal
from app.services.crud_question import get_today_question
from app.database import SessionLocal
from app.core.slack import client
from app.models.user import User
from app.models.answer import Answer
from app.models.question import Question
from app.services.crud_question import get_today_question
from app.database import SessionLocal
from datetime import datetime


router = APIRouter()

@router.post("/interactions")
async def slack_interactions(request: Request):
    form_data = await request.form()
    payload = json.loads(form_data["payload"])
    user_id = payload["user"]["id"]

    # Handle button click: open modal
    if payload["type"] == "block_actions":
        trigger_id = payload.get("trigger_id")
        db = SessionLocal()
        question = get_today_question(db)
        db.close()

        modal_view = build_checkin_modal(question.content if question else "No question found today.")
        client.views_open(trigger_id=trigger_id, view=modal_view)
        return JSONResponse(content={})

    # Handle modal submission
    if payload["type"] == "view_submission":
        db = SessionLocal()
        user = db.query(User).filter(User.slack_id == user_id).first()
        question = get_today_question(db)

        if user and question:
            answer_text = payload["view"]["state"]["values"]["answer_block"]["answer_input"]["value"]

            db_answer = Answer(
                user_id=user.id,
                question_id=question.id,
                answer=answer_text,
                timestamp=datetime.utcnow()
            )
            db.add(db_answer)
            db.commit()

        db.close()
        return JSONResponse(content={})