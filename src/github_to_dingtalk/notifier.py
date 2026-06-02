import logging

from dingtalkchatbot.chatbot import DingtalkChatbot

from github_to_dingtalk.config import AppConfig
from github_to_dingtalk.handlers.base import BaseHandler
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
        self._router = Router(config)

    def notify(self, payload: dict, event_type: str) -> None:
        logger.info("Preparing notification: %s", payload)
        handler = self._resolve_handler(payload, event_type)
        if handler is None:
            logger.warning("No handler found for event: %s", event_type)
            return

        repo: dict = payload.get("repository") or {}
        repo_name: str = repo.get("full_name", "")
        action: str | None = payload.get("action")
        groups = self._router.resolve(repo_name, event_type, action)
        if not groups:
            logger.info("No target groups for repo=%s event=%s", repo_name, event_type)
            return

        message = handler.build_message()
        for group in groups:
            bot = DingtalkChatbot(group.webhook, group.secret)
            bot.send_markdown(title=message.title, text=message.text)

    def _resolve_handler(self, payload: dict, event_type: str) -> BaseHandler | None:
        handler_cls = HANDLER_MAP.get(event_type)
        if handler_cls is not None:
            return handler_cls(payload)
        return GenericHandler(payload, event_type)
