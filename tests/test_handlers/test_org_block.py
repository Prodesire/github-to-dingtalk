from github_to_dingtalk.handlers.org_block import OrgBlockHandler


def test_user_blocked():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "action": "blocked",
        "blocked_user": {
            "login": "badactor",
            "html_url": "https://github.com/badactor",
        },
        "organization": {
            "login": "my-org",
            "html_url": "https://github.com/my-org",
        },
    }
    handler = OrgBlockHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Org Block"
    assert "blocked" in msg.text
    assert "badactor" in msg.text
    assert "my-org" in msg.text
    assert "octocat" in msg.text
