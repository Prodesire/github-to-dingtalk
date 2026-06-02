from github_to_dingtalk.handlers.base import BaseHandler, Message


class MembershipHandler(BaseHandler):
    def build_message(self) -> Message:
        member = self.payload["member"]
        member_login = member["login"]
        member_url = member["html_url"]
        md_member = f"[{member_login}]({member_url})"

        team = self.payload["team"]
        team_name = team["name"]

        return Message(
            title="Membership",
            text=(
                f"{self.md_sender} {self.action} {md_member}"
                f" {self.action_prep} team **{team_name}**"
            ),
        )
