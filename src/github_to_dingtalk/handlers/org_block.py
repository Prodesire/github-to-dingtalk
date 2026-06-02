from github_to_dingtalk.handlers.base import BaseHandler, Message


class OrgBlockHandler(BaseHandler):
    def build_message(self) -> Message:
        blocked_user = self.payload["blocked_user"]
        blocked_login = blocked_user["login"]
        blocked_url = blocked_user["html_url"]
        md_blocked = f"[{blocked_login}]({blocked_url})"

        org = self.payload["organization"]
        org_login = org["login"]
        org_url = org["html_url"]
        md_org = f"[{org_login}]({org_url})"

        return Message(
            title="Org Block",
            text=(
                f"{self.md_sender} {self.action} {md_blocked}"
                f" in organization {md_org}"
            ),
        )
