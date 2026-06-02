from github_to_dingtalk.handlers.base import BaseHandler, Message


class PublicHandler(BaseHandler):
    def build_message(self) -> Message:
        return Message(
            title="Public",
            text=f"{self.md_sender} made {self.md_repo} public",
        )
