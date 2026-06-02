from github_to_dingtalk.handlers.check_run import CheckRunHandler

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


def test_check_run_completed_success():
    payload = {
        **PAYLOAD_BASE,
        "action": "completed",
        "check_run": {
            "name": "build",
            "status": "completed",
            "conclusion": "success",
            "html_url": "https://github.com/octocat/Hello-World/runs/1",
            "output": {"title": "Build", "summary": "All checks passed"},
        },
    }
    handler = CheckRunHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Check Run"
    assert "**build**" in msg.text
    assert "Status: completed" in msg.text
    assert "Conclusion: success" in msg.text
    assert "[Details]" in msg.text


def test_check_run_created_no_conclusion():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "check_run": {
            "name": "lint",
            "status": "queued",
            "conclusion": None,
            "html_url": "https://github.com/octocat/Hello-World/runs/2",
            "output": {"title": "Lint", "summary": ""},
        },
    }
    handler = CheckRunHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Check Run"
    assert "**lint**" in msg.text
    assert "Status: queued" in msg.text
    assert "Conclusion: None" in msg.text
