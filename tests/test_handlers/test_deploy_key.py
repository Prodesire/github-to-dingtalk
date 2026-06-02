from github_to_dingtalk.handlers.deploy_key import DeployKeyHandler

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


def test_deploy_key_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "key": {
            "title": "my-deploy-key",
            "read_only": True,
            "verified": True,
        },
    }
    handler = DeployKeyHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Deploy Key"
    assert "created" in msg.text
    assert "**my-deploy-key**" in msg.text
    assert "Read-only: True" in msg.text
