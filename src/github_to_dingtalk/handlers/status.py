from github_to_dingtalk.handlers.base import BaseHandler, Message


class StatusHandler(BaseHandler):
    def build_message(self) -> Message:
        state = self.payload["state"]
        description = self.payload.get("description") or ""
        target_url = self.payload.get("target_url") or ""
        context = self.payload.get("context") or ""
        sha = self.payload["sha"]

        return Message(
            title="Status",
            text=(
                f"Commit status **{state}** for"
                f" `{sha[:7]}` in {self.md_repo}\n\n"
                f"Context: {context}\n\n"
                f"> {description}\n\n"
                f"[Details]({target_url})"
            ),
        )
