from github_to_dingtalk.handlers.status import StatusHandler

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


def test_status_success():
    payload = {
        **PAYLOAD_BASE,
        "state": "success",
        "description": "All checks passed",
        "target_url": "https://ci.example.com/builds/123",
        "context": "ci/circleci",
        "sha": "abc1234567890",
        "branches": [{"name": "main"}],
    }
    handler = StatusHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Status"
    assert "**success**" in msg.text
    assert "`abc1234`" in msg.text
    assert "ci/circleci" in msg.text
    assert "All checks passed" in msg.text
    assert "https://ci.example.com/builds/123" in msg.text


def test_status_failure():
    payload = {
        **PAYLOAD_BASE,
        "state": "failure",
        "description": "Tests failed",
        "target_url": "https://ci.example.com/builds/456",
        "context": "ci/github-actions",
        "sha": "def4567890abc",
        "branches": [{"name": "feature"}],
    }
    handler = StatusHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Status"
    assert "**failure**" in msg.text
    assert "`def4567`" in msg.text
    assert "ci/github-actions" in msg.text
    assert "Tests failed" in msg.text
