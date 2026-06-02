from github_to_dingtalk.handlers.base import BaseHandler, Message


class InstallationHandler(BaseHandler):
    def build_message(self) -> Message:
        installation = self.payload["installation"]
        app_slug = installation["app_slug"]
        account = installation["account"]
        account_login = account["login"]
        account_url = account["html_url"]

        return Message(
            title="Installation",
            text=(
                f"App **{app_slug}** {self.action} for [{account_login}]({account_url})"
            ),
        )
