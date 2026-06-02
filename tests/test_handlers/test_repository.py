from github_to_dingtalk.handlers.repository import RepositoryHandler

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


def test_repository_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
    }
    handler = RepositoryHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Repository"
    assert "created" in msg.text
    assert "octocat" in msg.text
    assert "octocat/Hello-World" in msg.text


def test_repository_archived():
    payload = {
        **PAYLOAD_BASE,
        "action": "archived",
    }
    handler = RepositoryHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Repository"
    assert "archived" in msg.text
    assert "octocat" in msg.text
    assert "octocat/Hello-World" in msg.text
