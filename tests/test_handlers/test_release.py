from github_to_dingtalk.handlers.release import ReleaseHandler

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


def test_release_published():
    payload = {
        **PAYLOAD_BASE,
        "action": "published",
        "release": {
            "tag_name": "v1.0.0",
            "name": "First Release",
            "html_url": "https://github.com/octocat/Hello-World/releases/tag/v1.0.0",
            "body": "Initial stable release",
        },
    }
    handler = ReleaseHandler(payload)
    msg = handler.build_message()
    assert msg.title == "First Release"
    assert "First Release" in msg.text
    assert "Initial stable release" in msg.text


def test_release_published_no_body():
    payload = {
        **PAYLOAD_BASE,
        "action": "published",
        "release": {
            "tag_name": "v0.1.0",
            "name": "Beta",
            "html_url": "https://github.com/octocat/Hello-World/releases/tag/v0.1.0",
            "body": "",
        },
    }
    handler = ReleaseHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Beta"
    assert "Beta" in msg.text


def test_release_deleted():
    payload = {
        **PAYLOAD_BASE,
        "action": "deleted",
        "release": {
            "tag_name": "v0.0.1",
            "name": "",
            "html_url": "https://github.com/octocat/Hello-World/releases/tag/v0.0.1",
            "body": None,
        },
    }
    handler = ReleaseHandler(payload)
    msg = handler.build_message()
    assert msg.title == "v0.0.1"
    assert "v0.0.1" in msg.text
