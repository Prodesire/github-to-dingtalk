from github_to_dingtalk.handlers.fork import ForkHandler


def test_fork():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "repository": {
            "full_name": "owner/repo",
            "html_url": "https://github.com/owner/repo",
            "language": "Python",
            "stargazers_count": 42,
            "watchers_count": 42,
        },
        "action": "created",
        "forkee": {
            "full_name": "octocat/repo",
            "html_url": "https://github.com/octocat/repo",
        },
    }
    handler = ForkHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Fork"
    assert "octocat/repo" in msg.text
    assert "owner/repo" in msg.text
    assert "42" in msg.text
