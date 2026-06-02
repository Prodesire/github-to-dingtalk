from github_to_dingtalk.handlers.create import CreateHandler


def test_create_branch():
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
        "master_branch": "main",
        "description": "",
    }
    handler = CreateHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Create"
    assert "branch" in msg.text
    assert "feature-branch" in msg.text
    assert "owner/repo" in msg.text


def test_create_tag():
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
        "master_branch": "main",
        "description": "",
    }
    handler = CreateHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Create"
    assert "tag" in msg.text
    assert "v1.0.0" in msg.text
