from github_to_dingtalk.handlers.base import BaseHandler, Message


class PushHandler(BaseHandler):
    def build_message(self) -> Message:
        head_commit = self.payload["head_commit"]
        commit_id = head_commit["id"]
        commit_url = head_commit["url"]
        commit_message = head_commit["message"]
        added: list[str] = head_commit["added"]
        removed: list[str] = head_commit["removed"]
        modified: list[str] = head_commit["modified"]

        md_file_changes = ""
        if added:
            md_file_changes += f"\n- Added: {','.join(added)}"
        if removed:
            md_file_changes += f"\n- Removed: {','.join(removed)}"
        if modified:
            md_file_changes += f"\n- Modified: {','.join(modified)}"
        if md_file_changes:
            md_file_changes = "File Changes:" + md_file_changes

        return Message(
            title="Push",
            text=(
                f"{self.md_sender} has pushed commit(s)"
                f" {self.action_prep} {self.md_repo}\n\n"
                f"[#{commit_id}]({commit_url})\n\n"
                f"> {commit_message}\n\n"
                f"{md_file_changes}"
            ),
        )
