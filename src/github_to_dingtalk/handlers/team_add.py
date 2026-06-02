from github_to_dingtalk.handlers.base import BaseHandler, Message


class TeamAddHandler(BaseHandler):
    def build_message(self) -> Message:
        team = self.payload["team"]
        team_name = team["name"]

        return Message(
            title="Team Add",
            text=f"Team **{team_name}** was added to {self.md_repo}",
        )
