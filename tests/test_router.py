from github_to_dingtalk.config import AppConfig, DingTalkGroupConfig, RouteConfig
from github_to_dingtalk.router import Router


def _make_config(
    routes: list[RouteConfig],
    default_group: str | None = None,
) -> AppConfig:
    return AppConfig(
        dingtalk_groups={
            "g1": DingTalkGroupConfig(webhook="https://hook1", secret="SEC1"),
            "g2": DingTalkGroupConfig(webhook="https://hook2", secret="SEC2"),
        },
        routes=routes,
        default_group=default_group,
    )


def test_exact_match():
    config = _make_config(
        routes=[
            RouteConfig(repo="org/repo", events=["issues"], groups=["g1"]),
        ]
    )
    router = Router(config)
    result = router.resolve("org/repo", "issues")
    assert len(result) == 1
    assert result[0].webhook == "https://hook1"


def test_no_match_no_default():
    config = _make_config(routes=[])
    router = Router(config)
    result = router.resolve("org/repo", "push")
    assert result == []


def test_no_match_with_default():
    config = _make_config(routes=[], default_group="g2")
    router = Router(config)
    result = router.resolve("org/repo", "push")
    assert len(result) == 1
    assert result[0].webhook == "https://hook2"


def test_multi_rule_dedup():
    config = _make_config(
        routes=[
            RouteConfig(repo="org/repo", events=["push"], groups=["g1"]),
            RouteConfig(
                repo="org/repo",
                events=["push", "issues"],
                groups=["g1", "g2"],
            ),
        ]
    )
    router = Router(config)
    result = router.resolve("org/repo", "push")
    assert len(result) == 2
    webhooks = {r.webhook for r in result}
    assert webhooks == {"https://hook1", "https://hook2"}


def test_event_mismatch():
    config = _make_config(
        routes=[
            RouteConfig(repo="org/repo", events=["issues"], groups=["g1"]),
        ]
    )
    router = Router(config)
    result = router.resolve("org/repo", "push")
    assert result == []


def test_repo_mismatch():
    config = _make_config(
        routes=[
            RouteConfig(repo="org/other", events=["push"], groups=["g1"]),
        ]
    )
    router = Router(config)
    result = router.resolve("org/repo", "push")
    assert result == []
