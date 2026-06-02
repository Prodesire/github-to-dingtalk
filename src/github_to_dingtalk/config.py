import os
from pathlib import Path

import yaml
from pydantic import BaseModel


class DingTalkGroupConfig(BaseModel):
    webhook: str
    secret: str


class RouteConfig(BaseModel):
    repo: str
    events: list[str]
    groups: list[str]


class AppConfig(BaseModel):
    dingtalk_groups: dict[str, DingTalkGroupConfig]
    routes: list[RouteConfig]
    default_group: str | None = None


def load_config(path: str | None = None) -> AppConfig:
    if path is None:
        path = os.environ.get("CONFIG_PATH", "config.yml")
    raw = yaml.safe_load(Path(path).read_text())
    config = AppConfig(**raw)
    group_ids = set(config.dingtalk_groups.keys())
    for route in config.routes:
        for g in route.groups:
            if g not in group_ids:
                raise ValueError(
                    f"Route for '{route.repo}' references unknown group '{g}'"
                )
    if config.default_group is not None and config.default_group not in group_ids:
        raise ValueError(
            f"default_group references unknown group '{config.default_group}'"
        )
    return config
