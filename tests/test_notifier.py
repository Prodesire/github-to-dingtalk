import logging
from unittest.mock import MagicMock, patch

import pytest

from github_to_dingtalk.config import (
    AppConfig,
    DingTalkGroupConfig,
    MentionConfig,
    RouteConfig,
)
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
    mentions: MentionConfig | None = None,
) -> AppConfig:
    return AppConfig(
        dingtalk_groups={
            "g1": DingTalkGroupConfig(webhook="https://hook1", secret="SEC1"),
            "g2": DingTalkGroupConfig(webhook="https://hook2", secret="SEC2"),
        },
        routes=routes,
        default_group=default_group,
        mentions=mentions or MentionConfig(),
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
        "action": "released",
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
    assert call_kwargs["title"] == "First Release"


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_unrouted_event(mock_bot_cls: MagicMock):
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
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "created",
    }
    notifier.notify(payload, "star")
    mock_bot_cls.assert_not_called()


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_mentions_issue_assignee_when_enabled(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["issues.assigned"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            issue_assignees=True,
            github_to_dingtalk_ids={"dev1": "DINGTALK_USER_DEV1"},
        ),
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "assigned",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "body",
        },
        "assignee": {"login": "dev1"},
    }
    notifier.notify(payload, "issues")
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["at_dingtalk_ids"] == ["DINGTALK_USER_DEV1"]
    assert '<font color="#0089ff">@DINGTALK_USER_DEV1</font>' in call_kwargs["text"]
    assert "Assignee: **dev1**" not in call_kwargs["text"]
    assert "Please handle:" not in call_kwargs["text"]


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_mentions_pull_request_assignee_when_enabled(
    mock_bot_cls: MagicMock,
):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["pull_request.assigned"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            pull_request_assignees=True,
            github_to_dingtalk_ids={"dev1": "DINGTALK_USER_DEV1"},
        ),
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "assigned",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "body",
        },
        "assignee": {"login": "dev1"},
    }
    notifier.notify(payload, "pull_request")
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["at_dingtalk_ids"] == ["DINGTALK_USER_DEV1"]
    assert '<font color="#0089ff">@DINGTALK_USER_DEV1</font>' in call_kwargs["text"]
    assert "Assignee: **dev1**" not in call_kwargs["text"]
    assert "Please handle:" not in call_kwargs["text"]


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_mentions_pull_request_reviewer_when_enabled(
    mock_bot_cls: MagicMock,
):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["pull_request.review_requested"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            pull_request_reviewers=True,
            github_to_dingtalk_ids={"reviewer1": "DINGTALK_USER_REVIEWER1"},
        ),
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "review_requested",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "body",
        },
        "requested_reviewer": {"login": "reviewer1"},
    }
    notifier.notify(payload, "pull_request")
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["at_dingtalk_ids"] == ["DINGTALK_USER_REVIEWER1"]
    assert (
        '<font color="#0089ff">@DINGTALK_USER_REVIEWER1</font>' in call_kwargs["text"]
    )
    assert "Reviewer: **reviewer1**" not in call_kwargs["text"]
    assert "Please handle:" not in call_kwargs["text"]


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_mentions_issue_comment_author_when_enabled(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["issue_comment.created"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            issue_comment_authors=True,
            github_to_dingtalk_ids={"issue-author": "DINGTALK_USER_AUTHOR"},
        ),
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "created",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "body",
            "user": {"login": "issue-author"},
        },
        "comment": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1#issuecomment-1",
            "body": "I can reproduce this",
        },
    }
    notifier.notify(payload, "issue_comment")
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["at_dingtalk_ids"] == ["DINGTALK_USER_AUTHOR"]
    assert '<font color="#0089ff">@DINGTALK_USER_AUTHOR</font>' in call_kwargs["text"]
    assert "I can reproduce this" in call_kwargs["text"]


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_mentions_quoted_comment_author_when_enabled(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["issue_comment.created"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            issue_comment_authors=True,
            github_to_dingtalk_ids={
                "issue-author": "DINGTALK_USER_AUTHOR",
                "quoted-author": "DINGTALK_USER_QUOTED",
            },
        ),
    )
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "created",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "comments_url": "https://api.github.test/repos/octocat/Hello-World/issues/1/comments",
            "number": 1,
            "title": "Found a bug",
            "body": "body",
            "user": {"login": "issue-author"},
        },
        "comment": {
            "id": 20,
            "html_url": "https://github.com/octocat/Hello-World/issues/1#issuecomment-20",
            "body": (
                "> Directly putting policies into iac-code is inappropriate.\n"
                ">\n"
                "> - Add a new `pac-aliyun` skill.\n\n"
                "Let's do that."
            ),
        },
    }
    previous_comments = [
        {
            "id": 10,
            "body": (
                "Directly putting policies into iac-code is inappropriate.\n\n"
                "- Add a new `pac-aliyun` skill."
            ),
            "user": {"login": "quoted-author"},
        }
    ]
    notifier = DingTalkNotifier(
        config,
        issue_comments_fetcher=lambda url: previous_comments,
    )

    notifier.notify(payload, "issue_comment")

    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["at_dingtalk_ids"] == [
        "DINGTALK_USER_AUTHOR",
        "DINGTALK_USER_QUOTED",
    ]
    assert '<font color="#0089ff">@DINGTALK_USER_AUTHOR</font>' in call_kwargs["text"]
    assert '<font color="#0089ff">@DINGTALK_USER_QUOTED</font>' in call_kwargs["text"]


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_skips_ambiguous_quoted_comment_author(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["issue_comment.created"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            issue_comment_authors=True,
            github_to_dingtalk_ids={
                "issue-author": "DINGTALK_USER_AUTHOR",
                "first-author": "DINGTALK_USER_FIRST",
                "second-author": "DINGTALK_USER_SECOND",
            },
        ),
    )
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "created",
        "issue": {
            "comments_url": "https://api.github.test/repos/octocat/Hello-World/issues/1/comments",
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "body",
            "user": {"login": "issue-author"},
        },
        "comment": {
            "id": 20,
            "html_url": "https://github.com/octocat/Hello-World/issues/1#issuecomment-20",
            "body": "> Same quoted text.\n\nReplying.",
        },
    }
    previous_comments = [
        {"id": 10, "body": "Same quoted text.", "user": {"login": "first-author"}},
        {"id": 11, "body": "Same quoted text.", "user": {"login": "second-author"}},
    ]
    notifier = DingTalkNotifier(
        config,
        issue_comments_fetcher=lambda url: previous_comments,
    )

    notifier.notify(payload, "issue_comment")

    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["at_dingtalk_ids"] == ["DINGTALK_USER_AUTHOR"]
    assert "@DINGTALK_USER_FIRST" not in call_kwargs["text"]
    assert "@DINGTALK_USER_SECOND" not in call_kwargs["text"]


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_does_not_mention_when_disabled(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["issues.assigned"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            issue_assignees=False,
            github_to_dingtalk_ids={"dev1": "DINGTALK_USER_DEV1"},
        ),
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "assigned",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "body",
        },
        "assignee": {"login": "dev1"},
    }
    notifier.notify(payload, "issues")
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["at_dingtalk_ids"] == []
    assert 'font color="#0089ff"' not in call_kwargs["text"]
    assert "@DINGTALK_USER_DEV1" not in call_kwargs["text"]
    assert "Please handle:" not in call_kwargs["text"]
    assert "Assignee: **dev1**" in call_kwargs["text"]


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_does_not_mention_unmapped_user(mock_bot_cls: MagicMock):
    mock_bot = MagicMock()
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["pull_request.review_requested"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            pull_request_reviewers=True,
            github_to_dingtalk_ids={},
        ),
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "review_requested",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "body",
        },
        "requested_reviewer": {"login": "reviewer1"},
    }
    notifier.notify(payload, "pull_request")
    call_kwargs = mock_bot.send_markdown.call_args[1]
    assert call_kwargs["at_dingtalk_ids"] == []
    assert 'font color="#0089ff"' not in call_kwargs["text"]
    assert "@reviewer1" not in call_kwargs["text"]
    assert "Please handle:" not in call_kwargs["text"]
    assert "Reviewer: **reviewer1**" in call_kwargs["text"]


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_logs_mention_resolution_and_send_result(
    mock_bot_cls: MagicMock,
    caplog,
):
    mock_bot = MagicMock()
    mock_bot.send_markdown.return_value = {"errcode": 0, "errmsg": "ok"}
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["pull_request.review_requested"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            pull_request_reviewers=True,
            github_to_dingtalk_ids={"reviewer1": "$DINGTALK_REVIEWER1"},
        ),
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "review_requested",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "body",
        },
        "requested_reviewer": {"login": "reviewer1"},
    }

    caplog.set_level(logging.INFO, logger="github_to_dingtalk.notifier")
    notifier.notify(payload, "pull_request")

    log_text = caplog.text
    assert "Mention resolution:" in log_text
    assert "event=pull_request" in log_text
    assert "action=review_requested" in log_text
    assert "enabled=True" in log_text
    assert "mention_logins=['reviewer1']" in log_text
    assert "at_dingtalk_ids=['$DINGTALK_REVIEWER1']" in log_text
    assert "unmapped_logins=[]" in log_text
    assert "mapping_logins=['reviewer1']" in log_text
    assert "DingTalk send result:" in log_text
    assert "result={'errcode': 0, 'errmsg': 'ok'}" in log_text


@patch("github_to_dingtalk.notifier.DingtalkChatbot")
def test_notify_logs_send_exception_with_context(mock_bot_cls: MagicMock, caplog):
    mock_bot = MagicMock()
    mock_bot.send_markdown.side_effect = RuntimeError("DingTalk API error")
    mock_bot_cls.return_value = mock_bot

    config = _make_config(
        routes=[
            RouteConfig(
                repo="octocat/Hello-World",
                events=["issues.assigned"],
                groups=["g1"],
            ),
        ],
        mentions=MentionConfig(
            issue_assignees=True,
            github_to_dingtalk_ids={"dev1": "$DINGTALK_DEV1"},
        ),
    )
    notifier = DingTalkNotifier(config)
    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "assigned",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "body",
        },
        "assignee": {"login": "dev1"},
    }

    caplog.set_level(logging.ERROR, logger="github_to_dingtalk.notifier")
    with pytest.raises(RuntimeError, match="DingTalk API error"):
        notifier.notify(payload, "issues")

    log_text = caplog.text
    assert "DingTalk send failed:" in log_text
    assert "repo=octocat/Hello-World" in log_text
    assert "event=issues" in log_text
    assert "action=assigned" in log_text
    assert "title=Issue" in log_text
    assert "group_index=1" in log_text
    assert "group_count=1" in log_text
    assert "at_dingtalk_ids=['$DINGTALK_DEV1']" in log_text
    assert "DingTalk API error" in log_text
