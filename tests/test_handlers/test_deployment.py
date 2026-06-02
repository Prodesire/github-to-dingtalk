from github_to_dingtalk.handlers.deployment import DeploymentHandler

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


def test_deployment_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "deployment": {
            "environment": "production",
            "description": "Deploy request from CLI",
            "ref": "main",
            "sha": "abc123",
            "task": "deploy",
            "creator": {"login": "octocat"},
        },
    }
    handler = DeploymentHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Deployment"
    assert "production" in msg.text
    assert "main" in msg.text
    assert "Deploy request from CLI" in msg.text
    assert "octocat" in msg.text
