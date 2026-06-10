from github_to_dingtalk.handlers.pull_request import PullRequestHandler

PAYLOAD_BASE = {
    "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
    "repository": {
        "full_name": "octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "language": "Python",
        "stargazers_count": 42,
        "watchers_count": 42,
    },
    "action": "opened",
}


def test_pull_request():
    payload = {
        **PAYLOAD_BASE,
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "This fixes the bug",
        },
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request"
    assert "[octocat]" in msg.text
    assert "#1 Fix bug" in msg.text
    assert "This fixes the bug" in msg.text


def test_pull_request_review():
    payload = {
        **PAYLOAD_BASE,
        "action": "submitted",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "This fixes the bug",
        },
        "review": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1#pullrequestreview-1",
            "body": "Looks good!",
        },
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request Review"
    assert "Looks good!" in msg.text


def test_pull_request_review_comment():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "body",
        },
        "comment": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1#discussion_r1",
            "body": "Nit: rename this",
        },
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request Review Comment"
    assert "Nit: rename this" in msg.text


def test_pull_request_review_comment_does_not_mention_sender_when_sender_is_author():
    payload = {
        **PAYLOAD_BASE,
        "sender": {
            "login": "pr-author",
            "html_url": "https://github.com/pr-author",
        },
        "action": "created",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "body",
            "user": {"login": "pr-author"},
        },
        "comment": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1#discussion_r1",
            "body": "Nit: rename this",
        },
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request Review Comment"
    assert msg.mention_logins == []


def test_pull_request_review_comment_mentions_users_from_comment_body():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "body",
            "user": {"login": "pr-author"},
        },
        "comment": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1#discussion_r1",
            "body": "@Prodesire and @pr-author please take a look",
        },
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request Review Comment"
    assert msg.mention_logins == ["pr-author", "Prodesire"]


def test_pull_request_empty_body():
    payload = {
        **PAYLOAD_BASE,
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/2",
            "number": 2,
            "title": "Empty PR",
            "body": None,
        },
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request"
    assert "Empty PR" in msg.text


def test_pull_request_closed_no_body():
    payload = {
        **PAYLOAD_BASE,
        "action": "closed",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "This fixes the bug",
        },
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request"
    assert "#1 Fix bug" in msg.text
    assert "This fixes the bug" not in msg.text


def test_pull_request_labeled():
    payload = {
        **PAYLOAD_BASE,
        "action": "labeled",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "This fixes the bug",
        },
        "label": {"name": "enhancement"},
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request"
    assert "Label: **enhancement**" in msg.text
    assert "This fixes the bug" not in msg.text


def test_pull_request_assigned():
    payload = {
        **PAYLOAD_BASE,
        "action": "assigned",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "This fixes the bug",
        },
        "assignee": {"login": "dev1"},
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request"
    assert "Assignee: **dev1**" in msg.text
    assert msg.mention_logins == ["dev1"]
    assert "This fixes the bug" not in msg.text


def test_pull_request_review_requested():
    payload = {
        **PAYLOAD_BASE,
        "action": "review_requested",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix bug",
            "body": "This fixes the bug",
        },
        "requested_reviewer": {"login": "reviewer1"},
    }
    handler = PullRequestHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Pull Request"
    assert "Reviewer: **reviewer1**" in msg.text
    assert msg.mention_logins == ["reviewer1"]
    assert "This fixes the bug" not in msg.text
