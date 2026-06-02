from github_to_dingtalk.config import AppConfig, DingTalkGroupConfig


class Router:
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def _match_event(self, pattern: str, event_type: str, action: str | None) -> bool:
        if "." in pattern:
            pat_event, pat_action = pattern.split(".", 1)
            return pat_event == event_type and pat_action == action
        return pattern == event_type

    def resolve(
        self, repo: str, event_type: str, action: str | None = None
    ) -> list[DingTalkGroupConfig]:
        matched_ids: list[str] = []
        seen: set[str] = set()
        for route in self._config.routes:
            if route.repo == repo and any(
                self._match_event(e, event_type, action) for e in route.events
            ):
                for g in route.groups:
                    if g not in seen:
                        seen.add(g)
                        matched_ids.append(g)
        if not matched_ids and self._config.default_group is not None:
            matched_ids.append(self._config.default_group)
        return [self._config.dingtalk_groups[g] for g in matched_ids]
