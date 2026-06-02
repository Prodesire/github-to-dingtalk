from github_to_dingtalk.handlers.base import BaseHandler, Message


class SubIssuesHandler(BaseHandler):
    def build_message(self) -> Message:
        sub = self.payload["sub_issue"]
        sub_number = sub["number"]
        sub_title = sub["title"]
        sub_url = sub["html_url"]

        parent = self.payload["parent_issue"]
        parent_number = parent["number"]
        parent_title = parent["title"]
        parent_url = parent["html_url"]

        return Message(
            title="Sub Issues",
            text=(
                f"{self.md_sender} {self.action}:"
                f" [#{sub_number} {sub_title}]({sub_url})"
                f" under [#{parent_number} {parent_title}]({parent_url})"
                f" in {self.md_repo}"
            ),
        )
