import logging

from dingtalkchatbot.chatbot import DingtalkChatbot

from github_to_dingtalk.config import AppConfig
from github_to_dingtalk.handlers.base import BaseHandler, Message
from github_to_dingtalk.handlers.branch_protection_rule import (
    BranchProtectionRuleHandler,
)
from github_to_dingtalk.handlers.check_run import CheckRunHandler
from github_to_dingtalk.handlers.check_suite import CheckSuiteHandler
from github_to_dingtalk.handlers.code_scanning_alert import CodeScanningAlertHandler
from github_to_dingtalk.handlers.commit_comment import CommitCommentHandler
from github_to_dingtalk.handlers.create import CreateHandler
from github_to_dingtalk.handlers.delete import DeleteHandler
from github_to_dingtalk.handlers.dependabot_alert import DependabotAlertHandler
from github_to_dingtalk.handlers.deploy_key import DeployKeyHandler
from github_to_dingtalk.handlers.deployment import DeploymentHandler
from github_to_dingtalk.handlers.deployment_status import DeploymentStatusHandler
from github_to_dingtalk.handlers.discussion import DiscussionHandler
from github_to_dingtalk.handlers.fork import ForkHandler
from github_to_dingtalk.handlers.generic import GenericHandler
from github_to_dingtalk.handlers.gollum import GollumHandler
from github_to_dingtalk.handlers.installation import InstallationHandler
from github_to_dingtalk.handlers.issue import IssueHandler
from github_to_dingtalk.handlers.label import LabelHandler
from github_to_dingtalk.handlers.member import MemberHandler
from github_to_dingtalk.handlers.membership import MembershipHandler
from github_to_dingtalk.handlers.merge_group import MergeGroupHandler
from github_to_dingtalk.handlers.meta import MetaHandler
from github_to_dingtalk.handlers.milestone import MilestoneHandler
from github_to_dingtalk.handlers.org_block import OrgBlockHandler
from github_to_dingtalk.handlers.organization import OrganizationHandler
from github_to_dingtalk.handlers.package import PackageHandler
from github_to_dingtalk.handlers.page_build import PageBuildHandler
from github_to_dingtalk.handlers.ping import PingHandler
from github_to_dingtalk.handlers.projects_v2 import ProjectsV2Handler
from github_to_dingtalk.handlers.projects_v2_item import ProjectsV2ItemHandler
from github_to_dingtalk.handlers.public import PublicHandler
from github_to_dingtalk.handlers.pull_request import PullRequestHandler
from github_to_dingtalk.handlers.pull_request_review_thread import (
    PullRequestReviewThreadHandler,
)
from github_to_dingtalk.handlers.push import PushHandler
from github_to_dingtalk.handlers.registry_package import RegistryPackageHandler
from github_to_dingtalk.handlers.release import ReleaseHandler
from github_to_dingtalk.handlers.repository import RepositoryHandler
from github_to_dingtalk.handlers.repository_vulnerability_alert import (
    RepositoryVulnerabilityAlertHandler,
)
from github_to_dingtalk.handlers.secret_scanning_alert import (
    SecretScanningAlertHandler,
)
from github_to_dingtalk.handlers.security_advisory import SecurityAdvisoryHandler
from github_to_dingtalk.handlers.sponsorship import SponsorshipHandler
from github_to_dingtalk.handlers.star import StarHandler
from github_to_dingtalk.handlers.status import StatusHandler
from github_to_dingtalk.handlers.sub_issues import SubIssuesHandler
from github_to_dingtalk.handlers.team import TeamHandler
from github_to_dingtalk.handlers.team_add import TeamAddHandler
from github_to_dingtalk.handlers.watch import WatchHandler
from github_to_dingtalk.handlers.workflow_dispatch import WorkflowDispatchHandler
from github_to_dingtalk.handlers.workflow_job import WorkflowJobHandler
from github_to_dingtalk.handlers.workflow_run import WorkflowRunHandler
from github_to_dingtalk.router import Router

logger = logging.getLogger(__name__)

HANDLER_MAP: dict[str, type[BaseHandler]] = {
    "branch_protection_rule": BranchProtectionRuleHandler,
    "check_run": CheckRunHandler,
    "check_suite": CheckSuiteHandler,
    "code_scanning_alert": CodeScanningAlertHandler,
    "commit_comment": CommitCommentHandler,
    "create": CreateHandler,
    "delete": DeleteHandler,
    "dependabot_alert": DependabotAlertHandler,
    "deploy_key": DeployKeyHandler,
    "deployment": DeploymentHandler,
    "deployment_status": DeploymentStatusHandler,
    "discussion": DiscussionHandler,
    "discussion_comment": DiscussionHandler,
    "fork": ForkHandler,
    "gollum": GollumHandler,
    "installation": InstallationHandler,
    "issue_comment": IssueHandler,
    "issues": IssueHandler,
    "label": LabelHandler,
    "member": MemberHandler,
    "membership": MembershipHandler,
    "merge_group": MergeGroupHandler,
    "meta": MetaHandler,
    "milestone": MilestoneHandler,
    "org_block": OrgBlockHandler,
    "organization": OrganizationHandler,
    "package": PackageHandler,
    "page_build": PageBuildHandler,
    "ping": PingHandler,
    "projects_v2": ProjectsV2Handler,
    "projects_v2_item": ProjectsV2ItemHandler,
    "public": PublicHandler,
    "pull_request": PullRequestHandler,
    "pull_request_review": PullRequestHandler,
    "pull_request_review_comment": PullRequestHandler,
    "pull_request_review_thread": PullRequestReviewThreadHandler,
    "push": PushHandler,
    "registry_package": RegistryPackageHandler,
    "release": ReleaseHandler,
    "repository": RepositoryHandler,
    "repository_vulnerability_alert": RepositoryVulnerabilityAlertHandler,
    "secret_scanning_alert": SecretScanningAlertHandler,
    "security_advisory": SecurityAdvisoryHandler,
    "sponsorship": SponsorshipHandler,
    "star": StarHandler,
    "status": StatusHandler,
    "sub_issues": SubIssuesHandler,
    "team": TeamHandler,
    "team_add": TeamAddHandler,
    "watch": WatchHandler,
    "workflow_dispatch": WorkflowDispatchHandler,
    "workflow_job": WorkflowJobHandler,
    "workflow_run": WorkflowRunHandler,
}


class DingTalkNotifier:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._router = Router(config)

    def notify(self, payload: dict, event_type: str) -> None:
        repo: dict = payload.get("repository") or {}
        sender: dict = payload.get("sender") or {}
        issue: dict = payload.get("issue") or {}
        pull_request: dict = payload.get("pull_request") or {}
        assignee: dict = payload.get("assignee") or {}
        requested_reviewer: dict = payload.get("requested_reviewer") or {}
        repo_name: str = repo.get("full_name", "")
        action: str | None = payload.get("action")
        logger.info(
            "Preparing notification: repo=%s event=%s action=%s sender=%s "
            "issue=%s pull_request=%s assignee=%s requested_reviewer=%s",
            repo_name,
            event_type,
            action,
            sender.get("login", ""),
            issue.get("number", ""),
            pull_request.get("number", ""),
            assignee.get("login", ""),
            requested_reviewer.get("login", ""),
        )
        logger.debug("GitHub webhook payload: %s", payload)
        handler = self._resolve_handler(payload, event_type)
        if handler is None:
            logger.warning("No handler found for event: %s", event_type)
            return

        groups = self._router.resolve(repo_name, event_type, action)
        if not groups:
            logger.info("No target groups for repo=%s event=%s", repo_name, event_type)
            return

        try:
            message = handler.build_message()
        except Exception:
            logger.exception(
                "Failed to build DingTalk message: repo=%s event=%s action=%s "
                "handler=%s",
                repo_name,
                event_type,
                action,
                type(handler).__name__,
            )
            raise
        logger.info(
            "Built DingTalk message: repo=%s event=%s action=%s title=%s "
            "mention_logins=%s text_length=%s",
            repo_name,
            event_type,
            action,
            message.title,
            message.mention_logins,
            len(message.text),
        )
        at_dingtalk_ids = self._resolve_mention_ids(message, event_type, action)
        text = self._format_text(message.text, at_dingtalk_ids)
        for index, group in enumerate(groups, start=1):
            logger.info(
                "Sending DingTalk markdown: repo=%s event=%s action=%s title=%s "
                "group_index=%s group_count=%s at_dingtalk_ids=%s "
                "at_placeholder_count=%s",
                repo_name,
                event_type,
                action,
                message.title,
                index,
                len(groups),
                at_dingtalk_ids,
                len(at_dingtalk_ids),
            )
            try:
                bot = DingtalkChatbot(group.webhook, group.secret)
                result = bot.send_markdown(
                    title=message.title,
                    text=text,
                    at_dingtalk_ids=at_dingtalk_ids,
                )
            except Exception:
                logger.exception(
                    "DingTalk send failed: repo=%s event=%s action=%s title=%s "
                    "group_index=%s group_count=%s at_dingtalk_ids=%s "
                    "at_placeholder_count=%s",
                    repo_name,
                    event_type,
                    action,
                    message.title,
                    index,
                    len(groups),
                    at_dingtalk_ids,
                    len(at_dingtalk_ids),
                )
                raise
            logger.info(
                "DingTalk send result: repo=%s event=%s action=%s title=%s "
                "at_dingtalk_ids=%s result=%s",
                repo_name,
                event_type,
                action,
                message.title,
                at_dingtalk_ids,
                result,
            )

    def _resolve_handler(self, payload: dict, event_type: str) -> BaseHandler | None:
        handler_cls = HANDLER_MAP.get(event_type)
        if handler_cls is not None:
            return handler_cls(payload)
        return GenericHandler(payload, event_type)

    def _resolve_mention_ids(
        self, message: Message, event_type: str, action: str | None
    ) -> list[str]:
        enabled = self._mentions_enabled(event_type, action)
        mapping = self._config.mentions.github_to_dingtalk_ids
        mention_ids: list[str] = []
        unmapped_logins: list[str] = []
        seen: set[str] = set()
        if enabled:
            for login in message.mention_logins:
                dingtalk_id = mapping.get(login)
                if dingtalk_id:
                    if dingtalk_id not in seen:
                        seen.add(dingtalk_id)
                        mention_ids.append(dingtalk_id)
                else:
                    unmapped_logins.append(login)
        logger.info(
            "Mention resolution: event=%s action=%s enabled=%s "
            "mention_logins=%s at_dingtalk_ids=%s unmapped_logins=%s "
            "mapping_size=%s mapping_logins=%s",
            event_type,
            action,
            enabled,
            message.mention_logins,
            mention_ids,
            unmapped_logins,
            len(mapping),
            sorted(mapping),
        )
        return mention_ids

    def _mentions_enabled(self, event_type: str, action: str | None) -> bool:
        mentions = self._config.mentions
        if event_type == "issues" and action == "assigned":
            return mentions.issue_assignees
        if event_type == "pull_request" and action == "assigned":
            return mentions.pull_request_assignees
        if event_type == "pull_request" and action == "review_requested":
            return mentions.pull_request_reviewers
        return False

    def _format_text(self, text: str, at_dingtalk_ids: list[str]) -> str:
        if not at_dingtalk_ids:
            return text
        text = self._remove_mention_detail(text)
        placeholders = " ".join(
            f'<font color="#0089ff">@{dingtalk_id}</font>'
            for dingtalk_id in at_dingtalk_ids
        )
        return f"{text}\n\n{placeholders}"

    def _remove_mention_detail(self, text: str) -> str:
        lines = text.splitlines()
        removable_prefixes = ("Assignee: **", "Reviewer: **")
        kept_lines = [line for line in lines if not line.startswith(removable_prefixes)]
        return "\n".join(kept_lines).rstrip()
