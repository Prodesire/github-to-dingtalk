from github_to_dingtalk.handlers.secret_scanning_alert import SecretScanningAlertHandler

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
            "secret_type": "github_personal_access_token",
            "secret_type_display_name": "GitHub Personal Access Token",
            "html_url": "https://github.com/octocat/Hello-World/security/secret-scanning/1",
            "resolution": None,
        },
    }
    handler = SecretScanningAlertHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Secret Scanning Alert"
    assert "created" in msg.text
    assert "GitHub Personal Access Token" in msg.text


def test_alert_resolved():
    payload = {
        **PAYLOAD_BASE,
        "action": "resolved",
        "alert": {
            "secret_type": "github_personal_access_token",
            "secret_type_display_name": "GitHub Personal Access Token",
            "html_url": "https://github.com/octocat/Hello-World/security/secret-scanning/1",
            "resolution": "revoked",
        },
    }
    handler = SecretScanningAlertHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Secret Scanning Alert"
    assert "resolved" in msg.text
