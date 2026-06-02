from github_to_dingtalk.handlers.base import BaseHandler, Message


class SecretScanningAlertHandler(BaseHandler):
    def build_message(self) -> Message:
        alert = self.payload["alert"]
        secret_type_display_name = alert["secret_type_display_name"]
        url = alert["html_url"]

        return Message(
            title="Secret Scanning Alert",
            text=(
                f"Secret scanning alert {self.action} in {self.md_repo}\n\n"
                f"Type: **{secret_type_display_name}**\n\n"
                f"[View alert]({url})"
            ),
        )
