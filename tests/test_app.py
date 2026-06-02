import os

os.environ.setdefault("DINGTALK_WEBHOOK", "https://test")
os.environ.setdefault("DINGTALK_SECRET", "test")

from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from github_to_dingtalk.app import app

REPO_FIELDS = {
    "full_name": "octocat/Hello-World",
    "html_url": "https://github.com/octocat/Hello-World",
    "language": "Python",
    "stargazers_count": 42,
    "watchers_count": 42,
}

SENDER_FIELDS = {"login": "octocat", "html_url": "https://github.com/octocat"}

client = TestClient(app)


def test_webhook_success():
    mock_notifier = MagicMock()
    app.state.notifier = mock_notifier

    payload = {
        "sender": SENDER_FIELDS,
        "repository": REPO_FIELDS,
        "action": "opened",
        "pull_request": {
            "html_url": "https://github.com/octocat/Hello-World/pull/1",
            "number": 1,
            "title": "Fix",
            "body": "body",
        },
    }
    response = client.post("/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"success": True}
    mock_notifier.notify.assert_called_once_with(payload)


def test_webhook_notify_error():
    mock_notifier = MagicMock()
    mock_notifier.notify.side_effect = Exception("DingTalk API error")
    app.state.notifier = mock_notifier

    payload = {"sender": SENDER_FIELDS, "repository": REPO_FIELDS, "action": "opened"}
    response = client.post("/", json=payload)
    assert response.status_code == 500
    assert response.json()["success"] is False
    assert "DingTalk API error" in response.json()["message"]
