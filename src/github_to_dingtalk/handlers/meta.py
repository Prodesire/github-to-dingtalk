from github_to_dingtalk.handlers.base import BaseHandler, Message


class MetaHandler(BaseHandler):
    def build_message(self) -> Message:
        hook_id = self.payload["hook_id"]
        hook = self.payload["hook"]
        events = hook["events"]

        return Message(
            title="Meta",
            text=(
                f"Webhook {hook_id} {self.action} in {self.md_repo}\n\n"
                f"Events: {events}"
            ),
        )
