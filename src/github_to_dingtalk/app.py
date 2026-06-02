import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse

from github_to_dingtalk.config import load_config
from github_to_dingtalk.notifier import DingTalkNotifier

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[missing-return-type]
    config = load_config()
    app.state.notifier = DingTalkNotifier(config)
    yield


app = FastAPI(title="GitHub to DingTalk", lifespan=lifespan)


@app.post("/", response_model=None)
async def handle_webhook(
    request: Request,
    payload: dict[str, Any] = Body(...),
) -> dict[str, Any] | JSONResponse:
    event_type = request.headers.get("X-GitHub-Event")
    if not event_type:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Missing X-GitHub-Event header"},
        )
    try:
        request.app.state.notifier.notify(payload, event_type)
    except Exception as e:
        logger.exception("Failed to send notification")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": str(e)},
        )
    return {"success": True}
