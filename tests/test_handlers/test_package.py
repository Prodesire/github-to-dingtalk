from github_to_dingtalk.handlers.package import PackageHandler

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


def test_package_published():
    payload = {
        **PAYLOAD_BASE,
        "action": "published",
        "package": {
            "name": "my-package",
            "package_type": "npm",
            "html_url": "https://github.com/octocat/Hello-World/packages/123",
            "package_version": {
                "version": "1.0.0",
                "name": "my-package",
            },
        },
    }
    handler = PackageHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Package"
    assert "published" in msg.text
    assert "**my-package**" in msg.text
    assert "(npm)" in msg.text
    assert "v1.0.0" in msg.text
    assert "View package" in msg.text
    assert "https://github.com/octocat/Hello-World/packages/123" in msg.text
