from github_to_dingtalk.handlers.base import BaseHandler, Message


class DeploymentStatusHandler(BaseHandler):
    def build_message(self) -> Message:
        deployment_status = self.payload["deployment_status"]
        state = deployment_status["state"]
        description = deployment_status.get("description") or ""
        target_url = deployment_status.get("target_url") or ""
        environment = deployment_status["environment"]

        return Message(
            title="Deployment Status",
            text=(
                f"Deployment to **{environment}** is **{state}**"
                f" in {self.md_repo}\n\n"
                f"{description}\n\n"
                f"[Details]({target_url})"
            ),
        )
