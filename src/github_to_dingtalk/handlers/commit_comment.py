from github_to_dingtalk.handlers.base import BaseHandler, Message


class CommitCommentHandler(BaseHandler):
    def build_message(self) -> Message:
        comment = self.payload["comment"]
        comment_url = comment["html_url"]
        comment_body = comment["body"] or ""
        commit_id = comment["commit_id"]

        return Message(
            title="Commit Comment",
            text=(
                f"{self.md_sender} commented on commit"
                f" `{commit_id[:7]}` in {self.md_repo}\n\n"
                f"[View comment]({comment_url})\n\n"
                f"> {comment_body}"
            ),
        )
