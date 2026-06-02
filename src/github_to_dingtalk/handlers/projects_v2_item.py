from github_to_dingtalk.handlers.base import BaseHandler, Message


class ProjectsV2ItemHandler(BaseHandler):
    def build_message(self) -> Message:
        item = self.payload["projects_v2_item"]
        content_type = item["content_type"]

        return Message(
            title="Project Item",
            text=(f"{self.md_sender} {self.action} a {content_type} item in project"),
        )
