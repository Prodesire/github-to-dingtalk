from github_to_dingtalk.handlers.delete import DeleteHandler


def test_delete_branch():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "repository": {
            "full_name": "owner/repo",
            "html_url": "https://github.com/owner/repo",
            "stargazers_count": 10,
            "watchers_count": 10,
        },
        "ref": "feature-branch",
        "ref_type": "branch",
    }
    handler = DeleteHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Delete"
    assert "branch" in msg.text
    assert "feature-branch" in msg.text
    assert "owner/repo" in msg.text


def test_delete_tag():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "repository": {
            "full_name": "owner/repo",
            "html_url": "https://github.com/owner/repo",
            "stargazers_count": 10,
            "watchers_count": 10,
        },
        "ref": "v1.0.0",
        "ref_type": "tag",
    }
    handler = DeleteHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Delete"
    assert "tag" in msg.text
    assert "v1.0.0" in msg.text
