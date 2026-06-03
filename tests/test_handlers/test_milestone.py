from github_to_dingtalk.handlers.milestone import MilestoneHandler

PAYLOAD_BASE = {
    "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
    "repository": {
        "full_name": "octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "language": "Python",
        "stargazers_count": 42,
        "watchers_count": 42,
    },
}


def test_milestone_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "milestone": {
            "title": "v1.0",
            "description": "First stable release",
            "html_url": "https://github.com/octocat/Hello-World/milestone/1",
            "state": "open",
            "open_issues": 5,
            "closed_issues": 0,
        },
    }
    handler = MilestoneHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Milestone"
    assert "created" in msg.text
    assert "v1.0" in msg.text
    assert "First stable release" in msg.text
    assert "Open: 5" in msg.text
    assert "Closed: 0" in msg.text


def test_milestone_closed():
    payload = {
        **PAYLOAD_BASE,
        "action": "closed",
        "milestone": {
            "title": "v1.0",
            "description": "First stable release",
            "html_url": "https://github.com/octocat/Hello-World/milestone/1",
            "state": "closed",
            "open_issues": 0,
            "closed_issues": 10,
        },
    }
    handler = MilestoneHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Milestone"
    assert "closed" in msg.text
    assert "v1.0" in msg.text
    assert "Open: 0" in msg.text
    assert "Closed: 10" in msg.text
    assert "First stable release" not in msg.text
