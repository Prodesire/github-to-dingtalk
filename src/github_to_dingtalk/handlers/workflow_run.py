from github_to_dingtalk.handlers.base import BaseHandler, Message


class WorkflowRunHandler(BaseHandler):
    def build_message(self) -> Message:
        workflow_run = self.payload["workflow_run"]
        name = workflow_run["name"]
        head_branch = workflow_run["head_branch"]
        status = workflow_run["status"]
        conclusion = workflow_run.get("conclusion")
        url = workflow_run["html_url"]

        return Message(
            title="Workflow Run",
            text=(
                f"{self.md_sender} workflow **{name}** on `{head_branch}`"
                f" is {status} in {self.md_repo}\n\n"
                f"Conclusion: {conclusion}\n\n"
                f"[Details]({url})"
            ),
        )
