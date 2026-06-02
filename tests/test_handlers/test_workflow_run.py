from github_to_dingtalk.handlers.workflow_run import WorkflowRunHandler

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


def test_workflow_run_completed_success():
    payload = {
        **PAYLOAD_BASE,
        "action": "completed",
        "workflow_run": {
            "name": "CI",
            "head_branch": "main",
            "status": "completed",
            "conclusion": "success",
            "html_url": "https://github.com/octocat/Hello-World/actions/runs/123",
            "event": "push",
        },
    }
    handler = WorkflowRunHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Workflow Run"
    assert "CI" in msg.text
    assert "main" in msg.text
    assert "completed" in msg.text
    assert "success" in msg.text
    assert "octocat" in msg.text


def test_workflow_run_in_progress():
    payload = {
        **PAYLOAD_BASE,
        "action": "in_progress",
        "workflow_run": {
            "name": "Deploy",
            "head_branch": "feature-branch",
            "status": "in_progress",
            "conclusion": None,
            "html_url": "https://github.com/octocat/Hello-World/actions/runs/456",
            "event": "pull_request",
        },
    }
    handler = WorkflowRunHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Workflow Run"
    assert "Deploy" in msg.text
    assert "feature-branch" in msg.text
    assert "in_progress" in msg.text
