from github_to_dingtalk.handlers.base import BaseHandler, Message


class PullRequestHandler(BaseHandler):
    def build_message(self) -> Message:
        pr = self.payload["pull_request"]
        pr_number = pr["number"]
        pr_title = pr["title"]
        pr_body = pr["body"] or ""

        review = self.payload.get("review")
        comment = self.payload.get("comment")

        if review:
            review_url = review["html_url"]
            review_body = review["body"] or ""
            return Message(
                title="Pull Request Review",
                text=(
                    f"{self.md_sender} has {self.action} a pull request review"
                    f" {self.action_prep} {self.md_repo}\n\n"
                    f"[#{pr_number} {pr_title}]({review_url})\n\n"
                    f"{review_body}"
                ),
            )

        if comment:
            comment_url = comment["html_url"]
            comment_body = comment["body"] or ""
            pr_author = pr.get("user", {})
            return Message(
                title="Pull Request Review Comment",
                text=(
                    f"{self.md_sender} has {self.action} a pull request review comment"
                    f" {self.action_prep} {self.md_repo}\n\n"
                    f"[#{pr_number} {pr_title}]({comment_url})\n\n"
                    f"{comment_body}"
                ),
                mention_logins=self._comment_mention_logins(
                    comment_body,
                    pr_author,
                ),
            )

        pr_url = pr["html_url"]
        header = (
            f"{self.md_sender} has {self.action} a pull request"
            f" {self.action_prep} {self.md_repo}\n\n"
            f"[#{pr_number} {pr_title}]({pr_url})"
        )

        if self.action == "opened":
            detail = f"\n\n{pr_body}" if pr_body else ""
            mention_logins = []
        elif self.action in ("labeled", "unlabeled"):
            label = self.payload.get("label", {})
            label_name = label.get("name", "")
            detail = f"\n\nLabel: **{label_name}**"
            mention_logins = []
        elif self.action in ("assigned", "unassigned"):
            assignee = self.payload.get("assignee", {})
            assignee_login = assignee.get("login", "")
            detail = f"\n\nAssignee: **{assignee_login}**"
            mention_logins = (
                self._login_list(assignee) if self.action == "assigned" else []
            )
        elif self.action == "review_requested":
            reviewer = self.payload.get("requested_reviewer", {})
            reviewer_login = reviewer.get("login", "")
            detail = f"\n\nReviewer: **{reviewer_login}**"
            mention_logins = self._login_list(reviewer)
        else:
            detail = ""
            mention_logins = []

        return Message(
            title="Pull Request",
            text=header + detail,
            mention_logins=mention_logins,
        )
