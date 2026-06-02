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
                    f"> {review_body}"
                ),
            )

        if comment:
            comment_url = comment["html_url"]
            comment_body = comment["body"] or ""
            return Message(
                title="Pull Request Review Comment",
                text=(
                    f"{self.md_sender} has {self.action} a pull request review comment"
                    f" {self.action_prep} {self.md_repo}\n\n"
                    f"[#{pr_number} {pr_title}]({comment_url})\n\n"
                    f"> {comment_body}"
                ),
            )

        pr_url = pr["html_url"]
        return Message(
            title="Pull Request",
            text=(
                f"{self.md_sender} has {self.action} a pull request"
                f" {self.action_prep} {self.md_repo}\n\n"
                f"[#{pr_number} {pr_title}]({pr_url})\n\n"
                f"> {pr_body}"
            ),
        )
