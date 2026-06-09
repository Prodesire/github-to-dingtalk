import os
from pathlib import Path
from unittest.mock import patch

import pytest

from github_to_dingtalk.config import load_config


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    content = """\
dingtalk_groups:
  dev-group:
    webhook: "https://oapi.dingtalk.com/robot/send?access_token=aaa"
    secret: "SECaaa"
  release-group:
    webhook: "https://oapi.dingtalk.com/robot/send?access_token=bbb"
    secret: "SECbbb"

routes:
  - repo: "myorg/iac-code"
    events: ["issues", "pull_request"]
    groups: ["dev-group"]
  - repo: "myorg/iac-code"
    events: ["release"]
    groups: ["release-group"]

default_group: "dev-group"
"""
    p = tmp_path / "config.yml"
    p.write_text(content)
    return p


def test_load_config(config_file: Path):
    config = load_config(str(config_file))
    assert "dev-group" in config.dingtalk_groups
    assert "release-group" in config.dingtalk_groups
    assert (
        config.dingtalk_groups["dev-group"].webhook
        == "https://oapi.dingtalk.com/robot/send?access_token=aaa"
    )
    assert config.dingtalk_groups["dev-group"].secret == "SECaaa"
    assert len(config.routes) == 2
    assert config.routes[0].repo == "myorg/iac-code"
    assert config.routes[0].events == ["issues", "pull_request"]
    assert config.routes[0].groups == ["dev-group"]
    assert config.default_group == "dev-group"
    assert config.mentions.issue_assignees is False
    assert config.mentions.pull_request_assignees is False
    assert config.mentions.pull_request_reviewers is False
    assert config.mentions.github_to_dingtalk_ids == {}


def test_load_config_mentions(tmp_path: Path):
    content = """\
dingtalk_groups:
  dev-group:
    webhook: "https://hook"
    secret: "SEC123"

routes: []

mentions:
  issue_assignees: true
  pull_request_assignees: true
  pull_request_reviewers: true
  github_to_dingtalk_ids:
    dev1: "$DINGTALK_DEV1"
    reviewer1: "$DINGTALK_REVIEWER1"
"""
    p = tmp_path / "config.yml"
    p.write_text(content)
    config = load_config(str(p))
    assert config.mentions.issue_assignees is True
    assert config.mentions.pull_request_assignees is True
    assert config.mentions.pull_request_reviewers is True
    assert config.mentions.github_to_dingtalk_ids == {
        "dev1": "$DINGTALK_DEV1",
        "reviewer1": "$DINGTALK_REVIEWER1",
    }


def test_load_config_no_default_group(tmp_path: Path):
    content = """\
dingtalk_groups:
  dev-group:
    webhook: "https://hook"
    secret: "SEC123"

routes:
  - repo: "myorg/repo"
    events: ["push"]
    groups: ["dev-group"]
"""
    p = tmp_path / "config.yml"
    p.write_text(content)
    config = load_config(str(p))
    assert config.default_group is None


def test_load_config_invalid_group_reference(tmp_path: Path):
    content = """\
dingtalk_groups:
  dev-group:
    webhook: "https://hook"
    secret: "SEC123"

routes:
  - repo: "myorg/repo"
    events: ["push"]
    groups: ["nonexistent-group"]
"""
    p = tmp_path / "config.yml"
    p.write_text(content)
    with pytest.raises(ValueError, match="nonexistent-group"):
        load_config(str(p))


def test_load_config_invalid_default_group(tmp_path: Path):
    content = """\
dingtalk_groups:
  dev-group:
    webhook: "https://hook"
    secret: "SEC123"

routes: []

default_group: "nonexistent"
"""
    p = tmp_path / "config.yml"
    p.write_text(content)
    with pytest.raises(ValueError, match="nonexistent"):
        load_config(str(p))


def test_load_config_env_override(tmp_path: Path):
    content = """\
dingtalk_groups:
  g1:
    webhook: "https://hook"
    secret: "SEC"

routes: []
"""
    p = tmp_path / "config.yml"
    p.write_text(content)
    with patch.dict(os.environ, {"CONFIG_PATH": str(p)}):
        config = load_config()
        assert "g1" in config.dingtalk_groups
