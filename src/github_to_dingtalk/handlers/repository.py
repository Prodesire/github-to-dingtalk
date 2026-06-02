from github_to_dingtalk.handlers.base import BaseHandler, Message


class RepositoryHandler(BaseHandler):
    def build_message(self) -> Message:
        return Message(
            title="Repository",
            text=(f"{self.md_sender} {self.action} repository {self.md_repo}"),
        )
