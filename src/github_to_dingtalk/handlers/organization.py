from github_to_dingtalk.handlers.base import BaseHandler, Message


class OrganizationHandler(BaseHandler):
    def build_message(self) -> Message:
        org = self.payload["organization"]
        org_login = org["login"]
        org_url = org["html_url"]
        md_org = f"[{org_login}]({org_url})"

        text = f"Organization {md_org} event: {self.action}"

        if self.action in ("member_added", "member_removed"):
            membership = self.payload.get("membership") or {}
            user = membership.get("user") or {}
            user_login = user.get("login")
            if user_login:
                text += f" ({user_login})"

        return Message(
            title="Organization",
            text=text,
        )
