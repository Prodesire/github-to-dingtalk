from github_to_dingtalk.handlers.sub_issues import SubIssuesHandler

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


def test_sub_issue_added():
    payload = {
        **PAYLOAD_BASE,
        "action": "sub_issue_added",
        "sub_issue": {
            "number": 10,
            "title": "Child task",
            "html_url": "https://github.com/octocat/Hello-World/issues/10",
        },
        "parent_issue": {
            "number": 5,
            "title": "Parent epic",
            "html_url": "https://github.com/octocat/Hello-World/issues/5",
        },
    }
    handler = SubIssuesHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Sub Issues"
    assert "sub_issue_added" in msg.text
    assert "#10 Child task" in msg.text
    assert "#5 Parent epic" in msg.text
    assert "under" in msg.text
