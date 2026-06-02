from github_to_dingtalk.handlers.merge_group import MergeGroupHandler

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


def test_checks_requested():
    payload = {
        **PAYLOAD_BASE,
        "action": "checks_requested",
        "merge_group": {
            "head_sha": "abc123",
            "head_ref": "refs/heads/gh-readonly-queue/main/pr-1",
            "base_sha": "def456",
            "base_ref": "main",
        },
    }
    handler = MergeGroupHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Merge Group"
    assert "checks_requested" in msg.text
    assert "main" in msg.text
    assert "octocat/Hello-World" in msg.text
    assert "gh-readonly-queue" in msg.text
