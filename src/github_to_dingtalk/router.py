from github_to_dingtalk.config import AppConfig, DingTalkGroupConfig


class Router:
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def resolve(self, repo: str, event_type: str) -> list[DingTalkGroupConfig]:
        matched_ids: list[str] = []
        seen: set[str] = set()
        for route in self._config.routes:
            if route.repo == repo and event_type in route.events:
                for g in route.groups:
                    if g not in seen:
                        seen.add(g)
                        matched_ids.append(g)
        if not matched_ids and self._config.default_group is not None:
            matched_ids.append(self._config.default_group)
        return [self._config.dingtalk_groups[g] for g in matched_ids]
