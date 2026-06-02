from github_to_dingtalk.handlers.base import BaseHandler, Message


class DeleteHandler(BaseHandler):
    def build_message(self) -> Message:
        ref = self.payload["ref"]
        ref_type = self.payload["ref_type"]

        return Message(
            title="Delete",
            text=f"{self.md_sender} deleted {ref_type} `{ref}` from {self.md_repo}",
        )
