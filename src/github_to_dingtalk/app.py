import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse

from github_to_dingtalk.config import Settings
from github_to_dingtalk.notifier import DingTalkNotifier

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[missing-return-type]
    settings = Settings()  # ty: ignore[missing-argument]
    app.state.notifier = DingTalkNotifier(
        webhook=settings.dingtalk_webhook, secret=settings.dingtalk_secret
    )
    yield


app = FastAPI(title="GitHub to DingTalk", lifespan=lifespan)


@app.post("/", response_model=None)
async def handle_webhook(
    request: Request,
    payload: dict[str, Any] = Body(...),
) -> dict[str, Any] | JSONResponse:
    try:
        request.app.state.notifier.notify(payload)
    except Exception as e:
        logger.exception("Failed to send notification")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": str(e)},
        )
    return {"success": True}
