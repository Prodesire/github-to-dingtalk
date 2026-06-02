from github_to_dingtalk.handlers.security_advisory import SecurityAdvisoryHandler

PAYLOAD_BASE = {
    "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
}


def test_advisory_published():
    payload = {
        **PAYLOAD_BASE,
        "action": "published",
        "security_advisory": {
            "ghsa_id": "GHSA-abcd-1234-efgh",
            "summary": "Critical vulnerability in example-package",
            "description": "A detailed description of the vulnerability.",
            "severity": "critical",
            "html_url": "https://github.com/advisories/GHSA-abcd-1234-efgh",
        },
    }
    handler = SecurityAdvisoryHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Security Advisory"
    assert "published" in msg.text
    assert "GHSA-abcd-1234-efgh" in msg.text
    assert "Critical vulnerability in example-package" in msg.text
    assert "critical" in msg.text
