from github_to_dingtalk.handlers.base import BaseHandler, Message


class DiscussionHandler(BaseHandler):
    def build_message(self) -> Message:
        discussion = self.payload["discussion"]
        discussion_number = discussion["number"]
        discussion_title = discussion["title"]
        discussion_body = discussion["body"] or ""

        comment = self.payload.get("comment")
        if comment:
            comment_url = comment["html_url"]
            comment_body = comment["body"] or ""
            return Message(
                title="Discussion Comment",
                text=(
                    f"{self.md_sender} has {self.action} a discussion comment"
                    f" {self.action_prep} {self.md_repo}\n\n"
                    f"[#{discussion_number} {discussion_title}]({comment_url})\n\n"
                    f"> {comment_body}"
                ),
            )

        discussion_url = discussion["html_url"]
        return Message(
            title="Discussion",
            text=(
                f"{self.md_sender} has {self.action} a discussion"
                f" {self.action_prep} {self.md_repo}\n\n"
                f"[#{discussion_number} {discussion_title}]({discussion_url})\n\n"
                f"> {discussion_body}"
            ),
        )
