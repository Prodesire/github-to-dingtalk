from github_to_dingtalk.handlers.base import BaseHandler, Message


class ForkHandler(BaseHandler):
    def build_message(self) -> Message:
        forkee = self.payload["forkee"]
        fork_full_name = forkee["full_name"]
        fork_url = forkee["html_url"]
        md_fork = f"[{fork_full_name}]({fork_url})"

        return Message(
            title="Fork",
            text=(
                f"{self.md_sender} forked {md_fork} from {self.md_repo}\n\n"
                f"⭐️{self.repo_star_count}"
            ),
        )
