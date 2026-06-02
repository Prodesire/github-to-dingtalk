from github_to_dingtalk.handlers.base import BaseHandler, Message


class ProjectsV2Handler(BaseHandler):
    def build_message(self) -> Message:
        project = self.payload["projects_v2"]
        title = project["title"]
        short_description = project.get("short_description") or ""

        return Message(
            title="Project",
            text=(
                f"{self.md_sender} {self.action} project"
                f" **{title}** in {self.md_repo}\n\n"
                f"> {short_description}"
            ),
        )
