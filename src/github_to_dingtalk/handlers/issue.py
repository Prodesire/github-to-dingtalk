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
            issue_author = issue.get("user", {})
            return Message(
                title="Issue Comment",
                text=(
                    f"{self.md_sender} has {self.action} an issue comment"
                    f" {self.action_prep} {self.md_repo}\n\n"
                    f"[#{issue_number} {issue_title}]({comment_url})\n\n"
                    f"{comment_body}"
                ),
                mention_logins=self._comment_mention_logins(
                    comment_body,
                    issue_author,
                ),
            )

        issue_url = issue["html_url"]
        header = (
            f"{self.md_sender} has {self.action} an issue"
            f" {self.action_prep} {self.md_repo}\n\n"
            f"[#{issue_number} {issue_title}]({issue_url})"
        )

        if self.action == "opened":
            detail = f"\n\n{issue_body}" if issue_body else ""
        elif self.action in ("labeled", "unlabeled"):
            label = self.payload.get("label", {})
            label_name = label.get("name", "")
            detail = f"\n\nLabel: **{label_name}**"
        elif self.action in ("typed", "untyped"):
            issue_type = self.payload.get("type", {})
            type_name = issue_type.get("name", "")
            detail = f"\n\nType: **{type_name}**"
        elif self.action in ("assigned", "unassigned"):
            assignee = self.payload.get("assignee", {})
            assignee_login = assignee.get("login", "")
            detail = f"\n\nAssignee: **{assignee_login}**"
        else:
            detail = ""

        mention_logins = []
        if self.action == "assigned":
            mention_logins = self._login_list(self.payload.get("assignee", {}))

        return Message(
            title="Issue",
            text=header + detail,
            mention_logins=mention_logins,
        )
