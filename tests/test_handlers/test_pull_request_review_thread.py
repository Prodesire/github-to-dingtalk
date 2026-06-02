from github_to_dingtalk.handlers.pull_request_review_thread import (
    PullRequestReviewThreadHandler,
)

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


def test_thread_resolved():
    payload = {
        **PAYLOAD_BASE,
        "action": "resolved",
        "pull_request": {
            "number": 42,
            "title": "Fix bug",
            "html_url": "https://github.com/octocat/Hello-World/pull/42",
        },
        "thread": {
            "comments": [
                {
                    "body": "Needs changes",
                    "html_url": "https://github.com/octocat/Hello-World/pull/42#discussion_r1",
                }
            ]
        },
    }
    handler = PullRequestReviewThreadHandler(payload)
    msg = handler.build_message()
    assert msg.title == "PR Review Thread"
    assert "resolved" in msg.text
    assert "#42 Fix bug" in msg.text
