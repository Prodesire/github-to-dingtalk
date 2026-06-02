from github_to_dingtalk.handlers.code_scanning_alert import CodeScanningAlertHandler

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
            "rule": {
                "id": "js/zipslip",
                "description": "Arbitrary file write during zip extraction",
                "severity": "high",
            },
            "tool": {"name": "CodeQL"},
            "html_url": "https://github.com/octocat/Hello-World/code-scanning/1",
            "state": "open",
        },
    }
    handler = CodeScanningAlertHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Code Scanning Alert"
    assert "created" in msg.text
    assert "js/zipslip" in msg.text
    assert "high" in msg.text
    assert "CodeQL" in msg.text


def test_alert_fixed():
    payload = {
        **PAYLOAD_BASE,
        "action": "fixed",
        "alert": {
            "rule": {
                "id": "js/zipslip",
                "description": "Arbitrary file write during zip extraction",
                "severity": "high",
            },
            "tool": {"name": "CodeQL"},
            "html_url": "https://github.com/octocat/Hello-World/code-scanning/1",
            "state": "fixed",
        },
    }
    handler = CodeScanningAlertHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Code Scanning Alert"
    assert "fixed" in msg.text
