from github_to_dingtalk.handlers.watch import WatchHandler


def test_watch():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "repository": {
            "full_name": "octocat/Hello-World",
            "html_url": "https://github.com/octocat/Hello-World",
            "language": "Python",
            "stargazers_count": 42,
            "watchers_count": 100,
        },
        "action": "started",
    }
    handler = WatchHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Watch"
    assert "watched" in msg.text
    assert "100" in msg.text
