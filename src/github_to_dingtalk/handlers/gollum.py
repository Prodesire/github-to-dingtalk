from github_to_dingtalk.handlers.base import BaseHandler, Message


class GollumHandler(BaseHandler):
    def build_message(self) -> Message:
        pages = self.payload.get("pages") or []
        page_lines = "\n".join(
            f"- [{p['page_name']}]({p['html_url']}) ({p['action']})"
            for p in pages
        )

        return Message(
            title="Wiki",
            text=(
                f"{self.md_sender} updated wiki in {self.md_repo}\n\n"
                f"{page_lines}"
            ),
        )
