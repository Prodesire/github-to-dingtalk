from github_to_dingtalk.handlers.base import BaseHandler, Message


class SecurityAdvisoryHandler(BaseHandler):
    def build_message(self) -> Message:
        advisory = self.payload["security_advisory"]
        ghsa_id = advisory["ghsa_id"]
        summary = advisory["summary"]
        severity = advisory["severity"]
        url = advisory["html_url"]

        return Message(
            title="Security Advisory",
            text=(
                f"Security advisory {self.action}: **{ghsa_id}**\n\n"
                f"{summary}\n\n"
                f"Severity: {severity}\n\n"
                f"[View advisory]({url})"
            ),
        )
