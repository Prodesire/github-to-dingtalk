import logging

from dingtalkchatbot.chatbot import DingtalkChatbot

from github_to_dingtalk.config import AppConfig
from github_to_dingtalk.handlers.base import BaseHandler
from github_to_dingtalk.handlers.discussion import DiscussionHandler
from github_to_dingtalk.handlers.fork import ForkHandler
from github_to_dingtalk.handlers.issue import IssueHandler
from github_to_dingtalk.handlers.pull_request import PullRequestHandler
from github_to_dingtalk.handlers.push import PushHandler
from github_to_dingtalk.handlers.release import ReleaseHandler
from github_to_dingtalk.handlers.star import StarHandler
from github_to_dingtalk.handlers.watch import WatchHandler
from github_to_dingtalk.router import Router

logger = logging.getLogger(__name__)


class DingTalkNotifier:
    def __init__(self, config: AppConfig) -> None:
        self._router = Router(config)

    def notify(self, payload: dict, event_type: str) -> None:
        logger.info("Preparing notification: %s", payload)
        handler = self._resolve_handler(payload)
        if handler is None:
            logger.warning("No handler found for payload")
            return

        repo: dict = payload.get("repository") or {}
        repo_name: str = repo.get("full_name", "")
        groups = self._router.resolve(repo_name, event_type)
        if not groups:
            logger.info("No target groups for repo=%s event=%s", repo_name, event_type)
            return

        message = handler.build_message()
        for group in groups:
            bot = DingtalkChatbot(group.webhook, group.secret)
            bot.send_markdown(title=message.title, text=message.text)

    def _resolve_handler(self, payload: dict) -> BaseHandler | None:
        if "pull_request" in payload:
            return PullRequestHandler(payload)
        if "head_commit" in payload:
            return PushHandler(payload)
        if "issue" in payload:
            return IssueHandler(payload)
        if "starred_at" in payload:
            return StarHandler(payload)
        if "forkee" in payload:
            return ForkHandler(payload)
        if "discussion" in payload:
            return DiscussionHandler(payload)
        if "release" in payload:
            return ReleaseHandler(payload)
        if payload.get("action") == "started":
            return WatchHandler(payload)
        return None
