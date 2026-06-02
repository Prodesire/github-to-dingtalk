from github_to_dingtalk.handlers.base import BaseHandler, Message


class CheckRunHandler(BaseHandler):
    def build_message(self) -> Message:
        check_run = self.payload["check_run"]
        name = check_run["name"]
        status = check_run["status"]
        conclusion = check_run["conclusion"]
        url = check_run["html_url"]

        return Message(
            title="Check Run",
            text=(
                f"{self.md_sender} {self.action} check run **{name}**"
                f" {self.action_prep} {self.md_repo}\n\n"
                f"Status: {status}, Conclusion: {conclusion}\n\n"
                f"[Details]({url})"
            ),
        )
