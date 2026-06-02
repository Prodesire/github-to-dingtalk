from github_to_dingtalk.handlers.ping import PingHandler


def test_ping():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "repository": {
            "full_name": "owner/repo",
            "html_url": "https://github.com/owner/repo",
            "stargazers_count": 10,
            "watchers_count": 10,
        },
        "zen": "Keep it logically awesome.",
        "hook_id": 12345,
        "hook": {
            "events": ["push", "pull_request"],
        },
    }
    handler = PingHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Ping"
    assert "Keep it logically awesome." in msg.text
    assert "12345" in msg.text
