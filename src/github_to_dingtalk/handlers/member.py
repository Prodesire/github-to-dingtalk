from github_to_dingtalk.handlers.base import BaseHandler, Message


class MemberHandler(BaseHandler):
    def build_message(self) -> Message:
        member = self.payload["member"]
        member_login = member["login"]
        member_url = member["html_url"]
        md_member = f"[{member_login}]({member_url})"

        return Message(
            title="Member",
            text=(
                f"{self.md_sender} {self.action} {md_member}"
                f" as collaborator {self.action_prep} {self.md_repo}"
            ),
        )
