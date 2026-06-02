from github_to_dingtalk.handlers.sponsorship import SponsorshipHandler


def test_sponsorship_created():
    payload = {
        "sender": {"login": "octocat", "html_url": "https://github.com/octocat"},
        "action": "created",
        "sponsorship": {
            "sponsor": {
                "login": "generous-dev",
                "html_url": "https://github.com/generous-dev",
            },
            "tier": {
                "name": "Gold",
                "monthly_price_in_dollars": 25,
            },
        },
    }
    handler = SponsorshipHandler(payload)
    msg = handler.build_message()
    assert msg.title == "Sponsorship"
    assert "created" in msg.text
    assert "generous-dev" in msg.text
    assert "Gold" in msg.text
    assert "$25/month" in msg.text
