from github_to_dingtalk.handlers.check_suite import CheckSuiteHandler

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


def test_check_suite_completed():
    payload = {
        **PAYLOAD_BASE,
        "action": "completed",
        "check_suite": {
            "head_branch": "main",
            "status": "completed",
            "conclusion": "success",
            "url": "https://api.github.com/repos/octocat/Hello-World/check-suites/1",
            "head_sha": "abc123",
        },
    }
    handler = CheckSuiteHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Check Suite"
    assert "`main`" in msg.text
    assert "Status: completed" in msg.text
    assert "Conclusion: success" in msg.text


def test_check_suite_requested():
    payload = {
        **PAYLOAD_BASE,
        "action": "requested",
        "check_suite": {
            "head_branch": "feature-branch",
            "status": "queued",
            "conclusion": None,
            "url": "https://api.github.com/repos/octocat/Hello-World/check-suites/2",
            "head_sha": "def456",
        },
    }
    handler = CheckSuiteHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Check Suite"
    assert "`feature-branch`" in msg.text
    assert "Status: queued" in msg.text
