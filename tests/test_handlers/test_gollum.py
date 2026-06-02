from github_to_dingtalk.handlers.gollum import GollumHandler

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


def test_gollum_single_page():
    payload = {
        **PAYLOAD_BASE,
        "pages": [
            {
                "page_name": "Home",
                "title": "Home",
                "action": "created",
                "html_url": "https://github.com/octocat/Hello-World/wiki/Home",
            },
        ],
    }
    handler = GollumHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Wiki"
    assert "updated wiki" in msg.text
    assert "Home" in msg.text
    assert "(created)" in msg.text


def test_gollum_multiple_pages():
    payload = {
        **PAYLOAD_BASE,
        "pages": [
            {
                "page_name": "Home",
                "title": "Home",
                "action": "edited",
                "html_url": "https://github.com/octocat/Hello-World/wiki/Home",
            },
            {
                "page_name": "Getting-Started",
                "title": "Getting Started",
                "action": "created",
                "html_url": "https://github.com/octocat/Hello-World/wiki/Getting-Started",
            },
        ],
    }
    handler = GollumHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Wiki"
    assert "Home" in msg.text
    assert "(edited)" in msg.text
    assert "Getting-Started" in msg.text
    assert "(created)" in msg.text
