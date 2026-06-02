from github_to_dingtalk.handlers.base import BaseHandler, Message


class WorkflowJobHandler(BaseHandler):
    def build_message(self) -> Message:
        workflow_job = self.payload["workflow_job"]
        name = workflow_job["name"]
        workflow_name = workflow_job["workflow_name"]
        status = workflow_job["status"]
        conclusion = workflow_job.get("conclusion")
        url = workflow_job["html_url"]

        return Message(
            title="Workflow Job",
            text=(
                f"{self.md_sender} job **{name}** ({workflow_name})"
                f" is {status} in {self.md_repo}\n\n"
                f"Conclusion: {conclusion}\n\n"
                f"[Details]({url})"
            ),
        )
