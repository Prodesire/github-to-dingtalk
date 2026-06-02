from github_to_dingtalk.handlers.base import BaseHandler, Message


class TeamHandler(BaseHandler):
    def build_message(self) -> Message:
        team = self.payload["team"]
        team_name = team["name"]

        org = self.payload["organization"]
        org_login = org["login"]
        org_url = org["html_url"]
        md_org = f"[{org_login}]({org_url})"

        return Message(
            title="Team",
            text=f"{self.md_sender} {self.action} team **{team_name}** in {md_org}",
        )
