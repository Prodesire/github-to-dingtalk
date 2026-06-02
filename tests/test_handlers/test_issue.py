from github_to_dingtalk.handlers.issue import IssueHandler

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


def test_issue_opened():
    payload = {
        **PAYLOAD_BASE,
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "Steps to reproduce...",
        },
    }
    handler = IssueHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Issue"
    assert "#1 Found a bug" in msg.text
    assert "Steps to reproduce" in msg.text


def test_issue_comment():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "Steps to reproduce...",
        },
        "comment": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1#issuecomment-1",
            "body": "I can reproduce this",
        },
    }
    handler = IssueHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Issue Comment"
    assert "I can reproduce this" in msg.text


def test_issue_empty_body():
    payload = {
        **PAYLOAD_BASE,
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/2",
            "number": 2,
            "title": "No body",
            "body": None,
        },
    }
    handler = IssueHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Issue"
    assert "No body" in msg.text
