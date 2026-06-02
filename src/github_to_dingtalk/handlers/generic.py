from github_to_dingtalk.handlers.base import BaseHandler, Message


class GenericHandler(BaseHandler):
    def __init__(self, payload: dict, event_type: str) -> None:
        super().__init__(payload)
        self.event_type = event_type

    def build_message(self) -> Message:
        title = self.event_type.replace("_", " ").title()
        parts = [f"**{title}** event"]
        if self.action:
            parts.append(f"({self.action})")
        if self.repo_full_name:
            parts.append(f"in {self.md_repo}")
        if self.sender_login:
            parts[0:0] = [self.md_sender]
        return Message(title=title, text=" ".join(parts))
