import logging
import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse

from github_to_dingtalk.config import load_config
from github_to_dingtalk.notifier import DingTalkNotifier

logger = logging.getLogger(__name__)


def _configure_logging() -> None:
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    logging.getLogger("github_to_dingtalk").setLevel(level)


def _webhook_log_context(
    payload: dict[str, Any],
    event_type: str,
    delivery: str,
) -> dict[str, Any]:
    repo = payload.get("repository") or {}
    sender = payload.get("sender") or {}
    issue = payload.get("issue") or {}
    pull_request = payload.get("pull_request") or {}
    return {
        "event": event_type,
        "delivery": delivery,
        "action": payload.get("action") or "",
        "repo": repo.get("full_name") or "",
        "sender": sender.get("login") or "",
        "issue": issue.get("number") or "",
        "pull_request": pull_request.get("number") or "",
    }


_configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[missing-return-type]
    try:
        config = load_config()
    except Exception:
        logger.exception("Failed to load GitHub to DingTalk config")
        raise
    app.state.notifier = DingTalkNotifier(config)
    mentions = config.mentions
    logger.info(
        "Loaded GitHub to DingTalk config: group_count=%s route_count=%s "
        "default_group=%s issue_assignees=%s pull_request_assignees=%s "
        "pull_request_reviewers=%s issue_comment_authors=%s "
        "mapped_github_logins=%s",
        len(config.dingtalk_groups),
        len(config.routes),
        config.default_group or "",
        mentions.issue_assignees,
        mentions.pull_request_assignees,
        mentions.pull_request_reviewers,
        mentions.issue_comment_authors,
        sorted(mentions.github_to_dingtalk_ids),
    )
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
    delivery = request.headers.get("X-GitHub-Delivery", "")
    log_context = _webhook_log_context(payload, event_type, delivery)
    logger.info(
        "Received GitHub webhook: event=%s delivery=%s action=%s repo=%s "
        "sender=%s issue=%s pull_request=%s",
        log_context["event"],
        log_context["delivery"],
        log_context["action"],
        log_context["repo"],
        log_context["sender"],
        log_context["issue"],
        log_context["pull_request"],
    )
    try:
        request.app.state.notifier.notify(payload, event_type)
    except Exception as e:
        logger.exception(
            "Failed to handle GitHub webhook: event=%s delivery=%s action=%s "
            "repo=%s sender=%s issue=%s pull_request=%s",
            log_context["event"],
            log_context["delivery"],
            log_context["action"],
            log_context["repo"],
            log_context["sender"],
            log_context["issue"],
            log_context["pull_request"],
        )
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": str(e)},
        )
    logger.info(
        "Handled GitHub webhook: event=%s delivery=%s action=%s repo=%s",
        log_context["event"],
        log_context["delivery"],
        log_context["action"],
        log_context["repo"],
    )
    return {"success": True}
