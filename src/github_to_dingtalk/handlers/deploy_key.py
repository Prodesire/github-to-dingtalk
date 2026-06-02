from github_to_dingtalk.handlers.base import BaseHandler, Message


class DeployKeyHandler(BaseHandler):
    def build_message(self) -> Message:
        key = self.payload["key"]
        title = key["title"]
        read_only = key["read_only"]

        return Message(
            title="Deploy Key",
            text=(
                f"{self.md_sender} {self.action} deploy key"
                f" **{title}** in {self.md_repo}\n\n"
                f"Read-only: {read_only}"
            ),
        )
