from github_to_dingtalk.handlers.base import BaseHandler, Message


def test_message_dataclass():
    msg = Message(title="Test", text="Hello")
    assert msg.title == "Test"
    assert msg.text == "Hello"


def test_base_handler_extracts_sender():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "repository": {
            "full_name": "octocat/Hello-World",
            "html_url": "https://github.com/octocat/Hello-World",
            "language": "Python",
            "stargazers_count": 42,
            "watchers_count": 42,
        },
        "action": "opened",
    }
    handler = BaseHandler(payload)
    assert handler.sender_login == "octocat"
    assert handler.sender_url == "https://github.com/octocat"
    assert handler.md_sender == "[octocat](https://github.com/octocat)"


def test_base_handler_extracts_repo():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "repository": {
            "full_name": "octocat/Hello-World",
            "html_url": "https://github.com/octocat/Hello-World",
            "language": "Python",
            "stargazers_count": 42,
            "watchers_count": 42,
        },
        "action": "created",
    }
    handler = BaseHandler(payload)
    assert handler.repo_full_name == "octocat/Hello-World"
    assert handler.repo_url == "https://github.com/octocat/Hello-World"
    assert (
        handler.md_repo
        == "[octocat/Hello-World](https://github.com/octocat/Hello-World)"
    )
    assert handler.repo_star_count == 42


def test_base_handler_action_preposition():
    payload_created = {
        "sender": {"login": "a", "html_url": ""},
        "repository": {
            "full_name": "a/b",
            "html_url": "",
            "language": None,
            "stargazers_count": 0,
            "watchers_count": 0,
        },
        "action": "created",
    }
    handler = BaseHandler(payload_created)
    assert handler.action_prep == "to"

    payload_edited = {**payload_created, "action": "edited"}
    handler2 = BaseHandler(payload_edited)
    assert handler2.action_prep == "of"


def test_base_handler_missing_sender_and_repo():
    payload: dict = {"action": "created"}
    handler = BaseHandler(payload)
    assert handler.sender_login is None
    assert handler.repo_full_name is None
    assert handler.md_sender == "[None](None)"
    assert handler.md_repo == "[None](None)"
