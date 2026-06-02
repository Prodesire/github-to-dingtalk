from github_to_dingtalk.handlers.membership import MembershipHandler

PAYLOAD_BASE = {
    "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
    "organization": {"login": "my-org"},
    "team": {
        "name": "Justice League",
        "html_url": "https://github.com/orgs/my-org/teams/justice-league",
    },
}


def test_member_added():
    payload = {
        **PAYLOAD_BASE,
        "action": "added",
        "member": {
            "login": "newmember",
            "html_url": "https://github.com/newmember",
        },
    }
    handler = MembershipHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Membership"
    assert "added" in msg.text
    assert "newmember" in msg.text
    assert "Justice League" in msg.text
    assert "octocat" in msg.text


def test_member_removed():
    payload = {
        **PAYLOAD_BASE,
        "action": "removed",
        "member": {
            "login": "oldmember",
            "html_url": "https://github.com/oldmember",
        },
    }
    handler = MembershipHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Membership"
    assert "removed" in msg.text
    assert "oldmember" in msg.text
    assert "Justice League" in msg.text
