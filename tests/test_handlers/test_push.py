from github_to_dingtalk.handlers.push import PushHandler

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


def test_push_with_all_file_changes():
    payload = {
        **PAYLOAD_BASE,
        "head_commit": {
            "id": "abc123",
            "url": "https://github.com/octocat/Hello-World/commit/abc123",
            "message": "Fix typo",
            "added": ["new_file.py"],
            "removed": ["old_file.py"],
            "modified": ["readme.md"],
        },
    }
    handler = PushHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Push"
    assert "Fix typo" in msg.text
    assert "#abc123" in msg.text
    assert "Added: new_file.py" in msg.text
    assert "Removed: old_file.py" in msg.text
    assert "Modified: readme.md" in msg.text


def test_push_no_file_changes():
    payload = {
        **PAYLOAD_BASE,
        "head_commit": {
            "id": "def456",
            "url": "https://github.com/octocat/Hello-World/commit/def456",
            "message": "Empty commit",
            "added": [],
            "removed": [],
            "modified": [],
        },
    }
    handler = PushHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Push"
    assert "Empty commit" in msg.text
    assert "File Changes" not in msg.text
