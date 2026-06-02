from github_to_dingtalk.handlers.base import BaseHandler, Message


class BranchProtectionRuleHandler(BaseHandler):
    def build_message(self) -> Message:
        rule = self.payload["rule"]
        name = rule["name"]

        return Message(
            title="Branch Protection Rule",
            text=(
                f"{self.md_sender} {self.action} branch protection rule"
                f" for `{name}` in {self.md_repo}"
            ),
        )
