from github_to_dingtalk.handlers.dependabot_alert import DependabotAlertHandler

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


def test_alert_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "alert": {
            "summary": "Remote code execution in lodash",
            "severity": "critical",
            "html_url": "https://github.com/octocat/Hello-World/security/dependabot/1",
            "dependency": {"package": {"name": "lodash"}},
            "state": "open",
        },
    }
    handler = DependabotAlertHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Dependabot Alert"
    assert "created" in msg.text
    assert "lodash" in msg.text
    assert "critical" in msg.text


def test_alert_fixed():
    payload = {
        **PAYLOAD_BASE,
        "action": "fixed",
        "alert": {
            "summary": "Remote code execution in lodash",
            "severity": "critical",
            "html_url": "https://github.com/octocat/Hello-World/security/dependabot/1",
            "dependency": {"package": {"name": "lodash"}},
            "state": "fixed",
        },
    }
    handler = DependabotAlertHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Dependabot Alert"
    assert "fixed" in msg.text
