from github_to_dingtalk.handlers.discussion import DiscussionHandler

PAYLOAD_BASE = {
    "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
    "repository": {
        "full_name": "octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "language": "Python",
        "stargazers_count": 42,
        "watchers_count": 42,
    },
    "action": "created",
}


def test_discussion():
    payload = {
        **PAYLOAD_BASE,
        "discussion": {
            "html_url": "https://github.com/octocat/Hello-World/discussions/1",
            "number": 1,
            "title": "How to contribute?",
            "body": "I want to help",
        },
    }
    handler = DiscussionHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Discussion"
    assert "#1 How to contribute?" in msg.text
    assert "I want to help" in msg.text


def test_discussion_comment():
    payload = {
        **PAYLOAD_BASE,
        "discussion": {
            "html_url": "https://github.com/octocat/Hello-World/discussions/1",
            "number": 1,
            "title": "How to contribute?",
            "body": "I want to help",
        },
        "comment": {
            "html_url": "https://github.com/octocat/Hello-World/discussions/1#discussioncomment-1",
            "body": "Check CONTRIBUTING.md",
        },
    }
    handler = DiscussionHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Discussion Comment"
    assert "Check CONTRIBUTING.md" in msg.text


def test_discussion_empty_body():
    payload = {
        **PAYLOAD_BASE,
        "discussion": {
            "html_url": "https://github.com/octocat/Hello-World/discussions/2",
            "number": 2,
            "title": "Empty",
            "body": None,
        },
    }
    handler = DiscussionHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Discussion"


def test_discussion_closed_no_body():
    payload = {
        **PAYLOAD_BASE,
        "action": "closed",
        "discussion": {
            "html_url": "https://github.com/octocat/Hello-World/discussions/1",
            "number": 1,
            "title": "How to contribute?",
            "body": "I want to help",
        },
    }
    handler = DiscussionHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Discussion"
    assert "#1 How to contribute?" in msg.text
    assert "I want to help" not in msg.text


def test_discussion_labeled():
    payload = {
        **PAYLOAD_BASE,
        "action": "labeled",
        "discussion": {
            "html_url": "https://github.com/octocat/Hello-World/discussions/1",
            "number": 1,
            "title": "How to contribute?",
            "body": "I want to help",
        },
        "label": {"name": "question"},
    }
    handler = DiscussionHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Discussion"
    assert "Label: **question**" in msg.text
    assert "I want to help" not in msg.text


def test_discussion_category_changed():
    payload = {
        **PAYLOAD_BASE,
        "action": "category_changed",
        "discussion": {
            "html_url": "https://github.com/octocat/Hello-World/discussions/1",
            "number": 1,
            "title": "How to contribute?",
            "body": "I want to help",
            "category": {"name": "Q&A"},
        },
        "changes": {
            "category": {"from": {"name": "General"}},
        },
    }
    handler = DiscussionHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Discussion"
    assert "Category: **General** -> **Q&A**" in msg.text
    assert "I want to help" not in msg.text
