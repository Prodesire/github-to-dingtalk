from github_to_dingtalk.handlers.base import BaseHandler, Message


class WatchHandler(BaseHandler):
    def build_message(self) -> Message:
        return Message(
            title="Watch",
            text=(
                f"{self.md_sender} watched {self.md_repo}\n\n"
                f"Watchers: {self.repo_watchers_count}"
            ),
        )
