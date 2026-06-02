from github_to_dingtalk.handlers.workflow_job import WorkflowJobHandler

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


def test_workflow_job_completed():
    payload = {
        **PAYLOAD_BASE,
        "action": "completed",
        "workflow_job": {
            "name": "build",
            "status": "completed",
            "conclusion": "success",
            "html_url": "https://github.com/octocat/Hello-World/actions/runs/123/jobs/456",
            "workflow_name": "CI",
            "runner_name": "ubuntu-latest",
        },
    }
    handler = WorkflowJobHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Workflow Job"
    assert "build" in msg.text
    assert "CI" in msg.text
    assert "completed" in msg.text
    assert "success" in msg.text
    assert "octocat" in msg.text


def test_workflow_job_queued():
    payload = {
        **PAYLOAD_BASE,
        "action": "queued",
        "workflow_job": {
            "name": "test",
            "status": "queued",
            "conclusion": None,
            "html_url": "https://github.com/octocat/Hello-World/actions/runs/123/jobs/789",
            "workflow_name": "CI",
            "runner_name": None,
        },
    }
    handler = WorkflowJobHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Workflow Job"
    assert "test" in msg.text
    assert "queued" in msg.text
