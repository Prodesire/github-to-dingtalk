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
                    f"{comment_body}"
                ),
            )

        discussion_url = discussion["html_url"]
        header = (
            f"{self.md_sender} has {self.action} a discussion"
            f" {self.action_prep} {self.md_repo}\n\n"
            f"[#{discussion_number} {discussion_title}]({discussion_url})"
        )

        if self.action == "created":
            detail = f"\n\n{discussion_body}" if discussion_body else ""
        elif self.action in ("labeled", "unlabeled"):
            label = self.payload.get("label", {})
            label_name = label.get("name", "")
            detail = f"\n\nLabel: **{label_name}**"
        elif self.action == "category_changed":
            from_category = (
                self.payload.get("changes", {}).get("category", {}).get("from", {})
            )
            from_name = from_category.get("name", "")
            to_category = self.payload.get("discussion", {}).get("category", {})
            to_name = to_category.get("name", "")
            detail = f"\n\nCategory: **{from_name}** -> **{to_name}**"
        else:
            detail = ""

        return Message(
            title="Discussion",
            text=header + detail,
        )
