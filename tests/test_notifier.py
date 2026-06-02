from unittest.mock import MagicMock, patch

from github_to_dingtalk.notifier import DingTalkNotifier

REPO_FIELDS = {
    "full_name": "octocat/Hello-World",
    "html_url": "https://github.com/octocat/Hello-World",
    "language": "Python",
    "stargazers_count": 42,
    "watchers_count": 42,
}

SENDER_FIELDS = {"login": "octocat", "html_url": "https://github.com/octocat"}


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_pull_request(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    notifier = DingTalkNotifier(webhook="https://hook", secret="SEC123")
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
    notifier.notify(payload)
    mock_bot.send_markdown.assert_called_once()
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["title"] == "Pull Request"


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_push(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    notifier = DingTalkNotifier(webhook="https://hook", secret="SEC123")
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
    notifier.notify(payload)
    mock_bot.send_markdown.assert_called_once()
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["title"] == "Push"


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_star(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    notifier = DingTalkNotifier(webhook="https://hook", secret="SEC123")
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "created",
        "starred_at": "2026-01-01T00:00:00Z",
    }
    notifier.notify(payload)
    mock_bot.send_markdown.assert_called_once()
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["title"] == "Star"


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_unknown_event(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    notifier = DingTalkNotifier(webhook="https://hook", secret="SEC123")
    payload = {"some_unknown_key": True}
    notifier.notify(payload)
    mock_bot.send_markdown.assert_not_called()
