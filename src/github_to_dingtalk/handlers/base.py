from dataclasses import dataclass


@dataclass
class Message:
    title: str
    text: str


class BaseHandler:
    _TO_ACTIONS: set[str | None] = {"created", "opened", "submitted", None}

    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.action: str | None = payload.get("action")
        self.action_prep = "to" if self.action in self._TO_ACTIONS else "of"

        sender: dict = payload.get("sender") or {}
        self.sender_login: str | None = sender.get("login")
        self.sender_url: str | None = sender.get("html_url")
        self.md_sender = f"[{self.sender_login}]({self.sender_url})"

        repo: dict = payload.get("repository") or {}
        self.repo_full_name: str | None = repo.get("full_name")
        self.repo_url: str | None = repo.get("html_url")
        self.repo_star_count: int | None = repo.get("stargazers_count")
        self.repo_watchers_count: int | None = repo.get("watchers_count")
        self.md_repo = f"[{self.repo_full_name}]({self.repo_url})"

    def build_message(self) -> Message:
        raise NotImplementedError
