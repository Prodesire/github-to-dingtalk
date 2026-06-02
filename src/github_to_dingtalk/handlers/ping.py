from github_to_dingtalk.handlers.base import BaseHandler, Message


class PingHandler(BaseHandler):
    def build_message(self) -> Message:
        zen = self.payload["zen"]
        hook_id = self.payload["hook_id"]

        return Message(
            title="Ping",
            text=f"zen: {zen}\n\nhook_id: {hook_id}",
        )
