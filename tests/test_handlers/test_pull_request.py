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
