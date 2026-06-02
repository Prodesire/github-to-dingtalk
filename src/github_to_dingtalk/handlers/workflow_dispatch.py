from github_to_dingtalk.handlers.base import BaseHandler, Message


class WorkflowDispatchHandler(BaseHandler):
    def build_message(self) -> Message:
        workflow = self.payload["workflow"]
        ref = self.payload["ref"]

        return Message(
            title="Workflow Dispatch",
            text=(
                f"{self.md_sender} triggered workflow `{workflow}`"
                f" on `{ref}` in {self.md_repo}"
            ),
        )
