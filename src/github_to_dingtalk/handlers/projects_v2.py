from github_to_dingtalk.handlers.base import BaseHandler, Message


class ProjectsV2Handler(BaseHandler):
    def build_message(self) -> Message:
        project = self.payload["projects_v2"]
        title = project["title"]
        short_description = project.get("short_description") or ""

        header = f"{self.md_sender} {self.action} project **{title}** in {self.md_repo}"

        if self.action == "created":
            detail = f"\n\n{short_description}" if short_description else ""
        else:
            detail = ""

        return Message(
            title="Project",
            text=header + detail,
        )
