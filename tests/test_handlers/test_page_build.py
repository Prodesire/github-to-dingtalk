from github_to_dingtalk.handlers.page_build import PageBuildHandler

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


def test_page_build_success():
    payload = {
        **PAYLOAD_BASE,
        "build": {
            "status": "built",
            "error": {"message": None},
            "pusher": {"login": "octocat"},
            "duration": 12,
        },
    }
    handler = PageBuildHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Page Build"
    assert "**built**" in msg.text
    assert "Duration: 12s" in msg.text
    assert "Error" not in msg.text


def test_page_build_errored():
    payload = {
        **PAYLOAD_BASE,
        "build": {
            "status": "errored",
            "error": {"message": "Build timed out"},
            "pusher": {"login": "octocat"},
            "duration": 60,
        },
    }
    handler = PageBuildHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Page Build"
    assert "**errored**" in msg.text
    assert "Duration: 60s" in msg.text
    assert "Build timed out" in msg.text
