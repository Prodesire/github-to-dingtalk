from github_to_dingtalk.handlers.base import BaseHandler, Message


class PageBuildHandler(BaseHandler):
    def build_message(self) -> Message:
        build = self.payload["build"]
        status = build["status"]
        duration = build["duration"]
        error = build.get("error") or {}
        error_message = error.get("message")

        text = (
            f"GitHub Pages build **{status}**"
            f" in {self.md_repo}\n\n"
            f"Duration: {duration}s"
        )
        if error_message:
            text += f"\n\nError: {error_message}"

        return Message(title="Page Build", text=text)
