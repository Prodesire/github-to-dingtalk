from github_to_dingtalk.handlers.workflow_dispatch import WorkflowDispatchHandler

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


def test_workflow_dispatch():
    payload = {
        **PAYLOAD_BASE,
        "workflow": ".github/workflows/main.yml",
        "ref": "refs/heads/main",
        "inputs": {"deploy_env": "staging"},
    }
    handler = WorkflowDispatchHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Workflow Dispatch"
    assert "`.github/workflows/main.yml`" in msg.text
    assert "`refs/heads/main`" in msg.text
    assert "octocat/Hello-World" in msg.text
