from github_to_dingtalk.handlers.projects_v2_item import ProjectsV2ItemHandler

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


def test_projects_v2_item_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "projects_v2_item": {
            "content_type": "Issue",
            "content_node_id": "I_abc123",
        },
    }
    handler = ProjectsV2ItemHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Project Item"
    assert "created" in msg.text
    assert "Issue" in msg.text
    assert "item in project" in msg.text
