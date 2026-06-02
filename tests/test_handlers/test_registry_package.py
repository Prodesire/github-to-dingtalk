from github_to_dingtalk.handlers.registry_package import RegistryPackageHandler

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


def test_registry_package_published():
    payload = {
        **PAYLOAD_BASE,
        "action": "published",
        "registry_package": {
            "name": "my-package",
            "package_type": "container",
            "html_url": "https://github.com/octocat/Hello-World/packages/1",
            "package_version": {"version": "1.0.0"},
        },
    }
    handler = RegistryPackageHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Registry Package"
    assert "published" in msg.text
    assert "**my-package**" in msg.text
    assert "(container)" in msg.text
    assert "v1.0.0" in msg.text
    assert "[View]" in msg.text
