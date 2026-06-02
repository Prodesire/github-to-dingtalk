from github_to_dingtalk.handlers.base import BaseHandler, Message


class MilestoneHandler(BaseHandler):
    def build_message(self) -> Message:
        milestone = self.payload["milestone"]
        title = milestone["title"]
        description = milestone["description"] or ""
        url = milestone["html_url"]
        open_issues = milestone["open_issues"]
        closed_issues = milestone["closed_issues"]

        return Message(
            title="Milestone",
            text=(
                f"{self.md_sender} {self.action} milestone"
                f" [{title}]({url}) in {self.md_repo}\n\n"
                f"> {description}\n\n"
                f"Open: {open_issues} / Closed: {closed_issues}"
            ),
        )
