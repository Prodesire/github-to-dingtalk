from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

REPO_FIELDS = {
    "full_name": "octocat/Hello-World",
    "html_url": "https://github.com/octocat/Hello-World",
    "language": "Python",
    "stargazers_count": 42,
    "watchers_count": 42,
}

SENDER_FIELDS = {"login": "octocat", "html_url": "https://github.com/octocat"}


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    content = """\
dingtalk_groups:
  test-group:
    webhook: "https://hook"
    secret: "SEC123"

routes:
  - repo: "octocat/Hello-World"
    events: ["pull_request"]
    groups: ["test-group"]
"""
    p = tmp_path / "config.yml"
    p.write_text(content)
    return p


def test_webhook_success(config_file: Path, caplog):
    with patch.dict("os.environ", {"CONFIG_PATH": str(config_file)}):
        from github_to_dingtalk.app import app

        client = TestClient(app)
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
        caplog.set_level("INFO", logger="github_to_dingtalk.app")
        response = client.post(
            "/",
            json=payload,
            headers={"X-GitHub-Event": "pull_request"},
        )
        assert response.status_code == 200
        assert response.json() == {"success": True}
        mock_notifier.notify.assert_called_once_with(payload, "pull_request")
        assert (
            "Received GitHub webhook: event=pull_request delivery= action=opened "
            "repo=octocat/Hello-World sender=octocat issue= pull_request=1"
        ) in caplog.text
        assert (
            "Handled GitHub webhook: event=pull_request delivery= action=opened "
            "repo=octocat/Hello-World"
        ) in caplog.text


def test_webhook_notify_error(config_file: Path, caplog):
    with patch.dict("os.environ", {"CONFIG_PATH": str(config_file)}):
        from github_to_dingtalk.app import app

        client = TestClient(app)
        mock_notifier = MagicMock()
        mock_notifier.notify.side_effect = Exception("DingTalk API error")
        app.state.notifier = mock_notifier

        payload = {
            "sender": SENDER_FIELDS,
            "repository": REPO_FIELDS,
            "action": "opened",
        }
        caplog.set_level("ERROR", logger="github_to_dingtalk.app")
        response = client.post(
            "/",
            json=payload,
            headers={"X-GitHub-Event": "issues"},
        )
        assert response.status_code == 500
        assert response.json()["success"] is False
        assert "DingTalk API error" in response.json()["message"]
        assert (
            "Failed to handle GitHub webhook: event=issues delivery= action=opened "
            "repo=octocat/Hello-World sender=octocat issue= pull_request="
        ) in caplog.text
        assert "DingTalk API error" in caplog.text


def test_webhook_missing_event_header(config_file: Path):
    with patch.dict("os.environ", {"CONFIG_PATH": str(config_file)}):
        from github_to_dingtalk.app import app

        client = TestClient(app)
        mock_notifier = MagicMock()
        app.state.notifier = mock_notifier

        payload = {"sender": SENDER_FIELDS, "repository": REPO_FIELDS}
        response = client.post("/", json=payload)
        assert response.status_code == 400
        assert response.json()["success"] is False
