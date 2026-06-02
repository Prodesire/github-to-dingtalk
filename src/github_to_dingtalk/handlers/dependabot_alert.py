from github_to_dingtalk.handlers.base import BaseHandler, Message


class DependabotAlertHandler(BaseHandler):
    def build_message(self) -> Message:
        alert = self.payload["alert"]
        dependency = alert["dependency"]
        package_name = dependency["package"]["name"]
        summary = alert["summary"]
        severity = alert["severity"]
        url = alert["html_url"]

        return Message(
            title="Dependabot Alert",
            text=(
                f"Dependabot alert {self.action} in {self.md_repo}\n\n"
                f"**{package_name}**: {summary}\n\n"
                f"Severity: {severity}\n\n"
                f"[View alert]({url})"
            ),
        )
