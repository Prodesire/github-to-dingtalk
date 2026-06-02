from github_to_dingtalk.handlers.base import BaseHandler, Message


class ReleaseHandler(BaseHandler):
    def build_message(self) -> Message:
        release = self.payload["release"]
        tag_name = release["tag_name"]
        release_name = release.get("name") or tag_name
        release_url = release["html_url"]
        body = release.get("body") or ""
        return Message(
            title=release_name,
            text=(
                f"## [{release_name}]({release_url})\n\n"
                + (body + "\n\n" if body else "")
            ),
        )
