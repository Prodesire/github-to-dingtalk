from github_to_dingtalk.handlers.label import LabelHandler

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


def test_label_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "label": {
            "name": "bug",
            "color": "d73a4a",
            "description": "Something isn't working",
        },
    }
    handler = LabelHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Label"
    assert "created" in msg.text
    assert "**bug**" in msg.text


def test_label_deleted():
    payload = {
        **PAYLOAD_BASE,
        "action": "deleted",
        "label": {
            "name": "wontfix",
            "color": "ffffff",
            "description": None,
        },
    }
    handler = LabelHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Label"
    assert "deleted" in msg.text
    assert "**wontfix**" in msg.text
