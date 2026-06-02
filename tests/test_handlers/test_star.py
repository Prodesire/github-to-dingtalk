from github_to_dingtalk.handlers.star import StarHandler

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


def test_star_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "starred_at": "2026-01-01T00:00:00Z",
    }
    handler = StarHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Star"
    assert "starred" in msg.text
    assert "42" in msg.text


def test_star_deleted():
    payload = {**PAYLOAD_BASE, "action": "deleted", "starred_at": None}
    handler = StarHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Un-Star"
    assert "un-starred" in msg.text
