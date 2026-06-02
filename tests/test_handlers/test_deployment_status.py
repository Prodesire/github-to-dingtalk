from github_to_dingtalk.handlers.deployment_status import DeploymentStatusHandler

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


def test_deployment_status_success():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "deployment_status": {
            "state": "success",
            "description": "Deployment finished successfully",
            "target_url": "https://example.com/deployments/123",
            "environment": "production",
        },
        "deployment": {
            "ref": "main",
            "environment": "production",
        },
    }
    handler = DeploymentStatusHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Deployment Status"
    assert "production" in msg.text
    assert "success" in msg.text
    assert "Deployment finished successfully" in msg.text
    assert "https://example.com/deployments/123" in msg.text


def test_deployment_status_failure():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "deployment_status": {
            "state": "failure",
            "description": "Deployment failed due to timeout",
            "target_url": "https://example.com/deployments/456",
            "environment": "staging",
        },
        "deployment": {
            "ref": "feature-branch",
            "environment": "staging",
        },
    }
    handler = DeploymentStatusHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Deployment Status"
    assert "staging" in msg.text
    assert "failure" in msg.text
    assert "Deployment failed due to timeout" in msg.text
