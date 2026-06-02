from github_to_dingtalk.handlers.projects_v2 import ProjectsV2Handler

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


def test_projects_v2_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "projects_v2": {
            "title": "Roadmap",
            "html_url": "https://github.com/orgs/octocat/projects/1",
            "short_description": "Track upcoming features",
            "number": 1,
        },
    }
    handler = ProjectsV2Handler(payload)
    msg = handler.build_message()
    assert msg.title == "Project"
    assert "created" in msg.text
    assert "**Roadmap**" in msg.text
    assert "Track upcoming features" in msg.text


def test_projects_v2_closed():
    payload = {
        **PAYLOAD_BASE,
        "action": "closed",
        "projects_v2": {
            "title": "Sprint 1",
            "html_url": "https://github.com/orgs/octocat/projects/2",
            "short_description": None,
            "number": 2,
        },
    }
    handler = ProjectsV2Handler(payload)
    msg = handler.build_message()
    assert msg.title == "Project"
    assert "closed" in msg.text
    assert "**Sprint 1**" in msg.text
