from github_to_dingtalk.handlers.member import MemberHandler

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


def test_member_added():
    payload = {
        **PAYLOAD_BASE,
        "action": "added",
        "member": {
            "login": "hubot",
            "html_url": "https://github.com/hubot",
        },
    }
    handler = MemberHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Member"
    assert "added" in msg.text
    assert "hubot" in msg.text
    assert "collaborator" in msg.text


def test_member_removed():
    payload = {
        **PAYLOAD_BASE,
        "action": "removed",
        "member": {
            "login": "hubot",
            "html_url": "https://github.com/hubot",
        },
    }
    handler = MemberHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Member"
    assert "removed" in msg.text
    assert "hubot" in msg.text
