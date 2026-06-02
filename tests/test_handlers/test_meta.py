from github_to_dingtalk.handlers.meta import MetaHandler

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


def test_meta_deleted():
    payload = {
        **PAYLOAD_BASE,
        "action": "deleted",
        "hook_id": 123456,
        "hook": {
            "type": "Repository",
            "events": ["push", "pull_request"],
            "active": True,
        },
    }
    handler = MetaHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Meta"
    assert "123456" in msg.text
    assert "deleted" in msg.text
    assert "push" in msg.text
    assert "pull_request" in msg.text
