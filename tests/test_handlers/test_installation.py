from github_to_dingtalk.handlers.installation import InstallationHandler


def test_installation_created():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "action": "created",
        "installation": {
            "id": 1,
            "app_id": 100,
            "app_slug": "my-app",
            "account": {
                "login": "my-org",
                "html_url": "https://github.com/my-org",
            },
            "target_type": "Organization",
        },
    }
    handler = InstallationHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Installation"
    assert "**my-app**" in msg.text
    assert "created" in msg.text
    assert "my-org" in msg.text


def test_installation_deleted():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "action": "deleted",
        "installation": {
            "id": 1,
            "app_id": 100,
            "app_slug": "my-app",
            "account": {
                "login": "my-org",
                "html_url": "https://github.com/my-org",
            },
            "target_type": "Organization",
        },
    }
    handler = InstallationHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Installation"
    assert "**my-app**" in msg.text
    assert "deleted" in msg.text
