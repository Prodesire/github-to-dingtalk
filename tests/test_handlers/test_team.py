from github_to_dingtalk.handlers.team import TeamHandler

PAYLOAD_BASE = {
    "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
    "organization": {
        "login": "my-org",
        "html_url": "https://github.com/my-org",
    },
}


def test_team_created():
    payload = {
        **PAYLOAD_BASE,
        "action": "created",
        "team": {
            "name": "Justice League",
            "slug": "justice-league",
            "html_url": "https://github.com/orgs/my-org/teams/justice-league",
            "description": "A great team",
        },
    }
    handler = TeamHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Team"
    assert "created" in msg.text
    assert "Justice League" in msg.text
    assert "my-org" in msg.text
    assert "octocat" in msg.text


def test_team_added_to_repository():
    payload = {
        **PAYLOAD_BASE,
        "action": "added_to_repository",
        "team": {
            "name": "Justice League",
            "slug": "justice-league",
            "html_url": "https://github.com/orgs/my-org/teams/justice-league",
            "description": "A great team",
        },
    }
    handler = TeamHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Team"
    assert "added_to_repository" in msg.text
    assert "Justice League" in msg.text
