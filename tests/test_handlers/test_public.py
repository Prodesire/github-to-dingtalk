from github_to_dingtalk.handlers.public import PublicHandler


def test_public():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "repository": {
            "full_name": "owner/repo",
            "html_url": "https://github.com/owner/repo",
            "stargazers_count": 10,
            "watchers_count": 10,
        },
    }
    handler = PublicHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Public"
    assert "octocat" in msg.text
    assert "owner/repo" in msg.text
    assert "public" in msg.text
