from github_to_dingtalk.handlers.commit_comment import CommitCommentHandler

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


def test_commit_comment():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "comment": {
            "html_url": "https://github.com/octocat/Hello-World/commit/abc1234#commitcomment-1",
            "body": "Great work!",
            "path": None,
            "line": None,
            "commit_id": "abc1234567890def",
        },
    }
    handler = CommitCommentHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Commit Comment"
    assert "abc1234" in msg.text
    assert "Great work!" in msg.text
    assert "View comment" in msg.text


def test_commit_comment_with_path_and_line():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "comment": {
            "html_url": "https://github.com/octocat/Hello-World/commit/abc1234#commitcomment-2",
            "body": "Fix this line",
            "path": "src/main.py",
            "line": 42,
            "commit_id": "def7890abcdef123",
        },
    }
    handler = CommitCommentHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Commit Comment"
    assert "def7890" in msg.text
    assert "Fix this line" in msg.text
