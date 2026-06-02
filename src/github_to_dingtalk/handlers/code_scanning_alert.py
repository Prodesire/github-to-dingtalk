from github_to_dingtalk.handlers.base import BaseHandler, Message


class CodeScanningAlertHandler(BaseHandler):
    def build_message(self) -> Message:
        alert = self.payload["alert"]
        rule = alert["rule"]
        tool = alert["tool"]
        url = alert["html_url"]

        return Message(
            title="Code Scanning Alert",
            text=(
                f"Code scanning alert {self.action} in {self.md_repo}\n\n"
                f"Rule: **{rule['id']}** - {rule['description']}\n\n"
                f"Severity: {rule['severity']} | Tool: {tool['name']}\n\n"
                f"[View alert]({url})"
            ),
        )
