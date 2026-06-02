from unittest.mock import MagicMock, patch

from github_to_dingtalk.config import AppConfig, DingTalkGroupConfig, RouteConfig
from github_to_dingtalk.notifier import DingTalkNotifier

REPO_FIELDS = {
    "full_name": "octocat/Hello-World",
    "html_url": "https://github.com/octocat/Hello-World",
    "language": "Python",
    "stargazers_count": 42,
    "watchers_count": 42,
}

SENDER_FIELDS = {"login": "octocat", "html_url": "https://github.com/octocat"}


def _make_config(
    routes: list[RouteConfig],
    default_group: str | None = None,
) -> AppConfig:
    return AppConfig(
        dingtalk_groups={
            "g1": DingTalkGroupConfig(webhook="https://hook1", secret="SEC1"),
            "g2": DingTalkGroupConfig(webhook="https://hook2", secret="SEC2"),
        },
        routes=routes,
        default_group=default_group,
    )


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_sends_to_matched_group(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["pull_request"],
                groups=["g1"],
            ),
        ]
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "opened",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "body",
        },
    }
    notifier.notify(payload, "pull_request")
    mock_bot.send_markdown.assert_called_once()
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["title"] == "Pull Request"


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_sends_to_multiple_groups(mock_bot_cls: MagicMock):
    bots: list[MagicMock] = [MagicMock(), MagicMock()]
    mock_bot_cls.side_effect = bots

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["push"],
                groups=["g1", "g2"],
            ),
        ]
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "head_commit": {
            "id": "abc123",
            "url": "https://github.com/octocat/Hello-World/commit/abc123",
            "message": "Fix",
            "added": [],
            "removed": [],
            "modified": [],
        },
    }
    notifier.notify(payload, "push")
    assert bots[0].send_markdown.call_count == 1
    assert bots[1].send_markdown.call_count == 1


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_no_match_no_send(mock_bot_cls: MagicMock):
    config = _make_config(routes=[])
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "created",
        "starred_at": "2026-01-01T00:00:00Z",
    }
    notifier.notify(payload, "star")
    mock_bot_cls.assert_not_called()


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_release(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["release"],
                groups=["g1"],
            ),
        ]
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "published",
        "release": {
            "tag_name": "v1.0.0",
            "name": "First Release",
            "html_url": "https://github.com/octocat/Hello-World/releases/tag/v1.0.0",
            "body": "Initial stable release",
        },
    }
    notifier.notify(payload, "release")
    mock_bot.send_markdown.assert_called_once()
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["title"] == "Release"


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_unknown_event(mock_bot_cls: MagicMock):
    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["push"],
                groups=["g1"],
            ),
        ]
    )
    notifier = DingTalkNotifier(config)
    payload = {"some_unknown_key": True, "repository": REPO_FIELDS}
    notifier.notify(payload, "push")
    mock_bot_cls.assert_not_called()
