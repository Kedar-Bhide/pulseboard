from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json

router = APIRouter()

@router.post("/interactions")
async def slack_interactions(request: Request):
    form_data = await request.form()
    payload = json.loads(form_data["payload"])

    user = payload["user"]["id"]
    action = payload["actions"][0]["value"] if "actions" in payload else None

    print(f"👉 Button clicked by: {user}, action: {action}")

    return JSONResponse({"text": f"Got it <@{user}>! We'll handle that shortly."})