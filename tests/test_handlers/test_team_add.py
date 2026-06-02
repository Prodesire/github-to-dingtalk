from github_to_dingtalk.handlers.team_add import TeamAddHandler

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


def test_team_added_to_repo():
    payload = {
        **PAYLOAD_BASE,
        "team": {
            "name": "Justice League",
            "slug": "justice-league",
            "html_url": "https://github.com/orgs/my-org/teams/justice-league",
        },
    }
    handler = TeamAddHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Team Add"
    assert "Justice League" in msg.text
    assert "octocat/Hello-World" in msg.text
