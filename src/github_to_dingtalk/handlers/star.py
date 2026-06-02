from github_to_dingtalk.handlers.base import BaseHandler, Message


class StarHandler(BaseHandler):
    def build_message(self) -> Message:
        if self.action == "created":
            return Message(
                title="Star",
                text=(
                    f"{self.md_sender} starred {self.md_repo}\n\n"
                    f"⭐️{self.repo_star_count}"
                ),
            )
        return Message(
            title="Un-Star",
            text=(
                f"{self.md_sender} un-starred {self.md_repo}\n\n"
                f"⭐️{self.repo_star_count}"
            ),
        )
