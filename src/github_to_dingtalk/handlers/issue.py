from github_to_dingtalk.handlers.base import BaseHandler, Message


class IssueHandler(BaseHandler):
    def build_message(self) -> Message:
        issue = self.payload["issue"]
        issue_number = issue["number"]
        issue_title = issue["title"]
        issue_body = issue["body"] or ""

        comment = self.payload.get("comment")
        if comment:
            comment_url = comment["html_url"]
            comment_body = comment["body"] or ""
            return Message(
                title="Issue Comment",
                text=(
                    f"{self.md_sender} has {self.action} an issue comment"
                    f" {self.action_prep} {self.md_repo}\n\n"
                    f"[#{issue_number} {issue_title}]({comment_url})\n\n"
                    f"> {comment_body}"
                ),
            )

        issue_url = issue["html_url"]
        return Message(
            title="Issue",
            text=(
                f"{self.md_sender} has {self.action} an issue"
                f" {self.action_prep} {self.md_repo}\n\n"
                f"[#{issue_number} {issue_title}]({issue_url})\n\n"
                f"> {issue_body}"
            ),
        )
