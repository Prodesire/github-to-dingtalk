import os
from unittest.mock import patch

from github_to_dingtalk.config import Settings


def test_settings_from_env():
    env = {
        "DINGTALK_WEBHOOK": "https://oapi.dingtalk.com/robot/send?access_token=test",
        "DINGTALK_SECRET": "SECtest123",
    }
    with patch.dict(os.environ, env):
        settings = Settings()
        assert settings.dingtalk_webhook == env["DINGTALK_WEBHOOK"]
        assert settings.dingtalk_secret == env["DINGTALK_SECRET"]
