from github_to_dingtalk.handlers.generic import GenericHandler

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


def test_generic_with_action():
    payload = {**PAYLOAD_BASE, "action": "completed"}
    handler = GenericHandler(payload, "some_new_event")
    msg = handler.build_message()
    assert msg.title == "Some New Event"
    assert "completed" in msg.text
    assert "octocat" in msg.text


def test_generic_without_action():
    payload = {**PAYLOAD_BASE}
    handler = GenericHandler(payload, "unknown_event")
    msg = handler.build_message()
    assert msg.title == "Unknown Event"
    assert "octocat/Hello-World" in msg.text
