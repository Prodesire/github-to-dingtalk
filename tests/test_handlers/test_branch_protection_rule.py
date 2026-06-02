from github_to_dingtalk.handlers.branch_protection_rule import (
    BranchProtectionRuleHandler,
)

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


def test_rule_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "rule": {"name": "main", "admin_enforced": True},
    }
    handler = BranchProtectionRuleHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Branch Protection Rule"
    assert "created" in msg.text
    assert "`main`" in msg.text
    assert "octocat" in msg.text


def test_rule_deleted():
    payload = {
        **PAYLOAD_BASE,
        "action": "deleted",
        "rule": {"name": "release/*", "admin_enforced": False},
    }
    handler = BranchProtectionRuleHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Branch Protection Rule"
    assert "deleted" in msg.text
    assert "`release/*`" in msg.text
