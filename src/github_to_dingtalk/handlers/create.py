from github_to_dingtalk.handlers.base import BaseHandler, Message


class CreateHandler(BaseHandler):
    def build_message(self) -> Message:
        ref = self.payload["ref"]
        ref_type = self.payload["ref_type"]

        return Message(
            title="Create",
            text=f"{self.md_sender} created {ref_type} `{ref}` in {self.md_repo}",
        )
