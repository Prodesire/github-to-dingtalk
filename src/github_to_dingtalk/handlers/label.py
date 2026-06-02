from github_to_dingtalk.handlers.base import BaseHandler, Message


class LabelHandler(BaseHandler):
    def build_message(self) -> Message:
        label = self.payload["label"]
        name = label["name"]

        return Message(
            title="Label",
            text=(f"{self.md_sender} {self.action} label **{name}** in {self.md_repo}"),
        )
