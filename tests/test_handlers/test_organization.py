from github_to_dingtalk.handlers.organization import OrganizationHandler


def test_member_added():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "action": "member_added",
        "organization": {
            "login": "my-org",
            "html_url": "https://github.com/my-org",
        },
        "membership": {
            "user": {"login": "newmember"},
        },
    }
    handler = OrganizationHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Organization"
    assert "member_added" in msg.text
    assert "my-org" in msg.text
    assert "newmember" in msg.text


def test_renamed():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "action": "renamed",
        "organization": {
            "login": "my-org",
            "html_url": "https://github.com/my-org",
        },
    }
    handler = OrganizationHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Organization"
    assert "renamed" in msg.text
    assert "my-org" in msg.text
