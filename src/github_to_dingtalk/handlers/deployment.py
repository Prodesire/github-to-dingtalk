from github_to_dingtalk.handlers.base import BaseHandler, Message


class DeploymentHandler(BaseHandler):
    def build_message(self) -> Message:
        deployment = self.payload["deployment"]
        environment = deployment["environment"]
        ref = deployment["ref"]
        description = deployment.get("description") or ""

        return Message(
            title="Deployment",
            text=(
                f"{self.md_sender} created deployment to **{environment}**"
                f" from `{ref}` in {self.md_repo}\n\n"
                f"> {description}"
            ),
        )
