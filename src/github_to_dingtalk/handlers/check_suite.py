from github_to_dingtalk.handlers.base import BaseHandler, Message


class CheckSuiteHandler(BaseHandler):
    def build_message(self) -> Message:
        check_suite = self.payload["check_suite"]
        head_branch = check_suite["head_branch"]
        status = check_suite["status"]
        conclusion = check_suite["conclusion"]

        return Message(
            title="Check Suite",
            text=(
                f"{self.md_sender} check suite on branch `{head_branch}`"
                f" {self.action_prep} {self.md_repo}\n\n"
                f"Status: {status}, Conclusion: {conclusion}"
            ),
        )
