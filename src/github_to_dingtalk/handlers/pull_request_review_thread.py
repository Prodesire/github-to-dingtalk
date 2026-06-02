from github_to_dingtalk.handlers.base import BaseHandler, Message


class PullRequestReviewThreadHandler(BaseHandler):
    def build_message(self) -> Message:
        pr = self.payload["pull_request"]
        pr_number = pr["number"]
        pr_title = pr["title"]
        pr_url = pr["html_url"]

        return Message(
            title="PR Review Thread",
            text=(
                f"{self.md_sender} {self.action} a review thread"
                f" on {self.md_repo}\n\n"
                f"[#{pr_number} {pr_title}]({pr_url})"
            ),
        )
