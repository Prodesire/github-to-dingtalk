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
            "user": {"login": "issue-author"},
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
    assert msg.mention_logins == ["issue-author"]


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


def test_issue_closed_no_body():
    payload = {
        **PAYLOAD_BASE,
        "action": "closed",
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
    assert "Steps to reproduce" not in msg.text


def test_issue_labeled():
    payload = {
        **PAYLOAD_BASE,
        "action": "labeled",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "Steps to reproduce...",
        },
        "label": {"name": "bug"},
    }
    handler = IssueHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Issue"
    assert "Label: **bug**" in msg.text
    assert "Steps to reproduce" not in msg.text


def test_issue_assigned_mentions_assignee():
    payload = {
        **PAYLOAD_BASE,
        "action": "assigned",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "Steps to reproduce...",
        },
        "assignee": {"login": "dev1"},
    }
    handler = IssueHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Issue"
    assert "Assignee: **dev1**" in msg.text
    assert msg.mention_logins == ["dev1"]
    assert "Steps to reproduce" not in msg.text


def test_issue_typed():
    payload = {
        **PAYLOAD_BASE,
        "action": "typed",
        "issue": {
            "html_url": "https://github.com/octocat/Hello-World/issues/1",
            "number": 1,
            "title": "Found a bug",
            "body": "Steps to reproduce...",
        },
        "type": {"name": "Bug"},
    }
    handler = IssueHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Issue"
    assert "Type: **Bug**" in msg.text
    assert "Steps to reproduce" not in msg.text
