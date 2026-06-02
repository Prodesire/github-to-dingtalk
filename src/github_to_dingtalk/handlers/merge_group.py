from github_to_dingtalk.handlers.base import BaseHandler, Message


class MergeGroupHandler(BaseHandler):
    def build_message(self) -> Message:
        merge_group = self.payload["merge_group"]
        head_ref = merge_group["head_ref"]
        base_ref = merge_group["base_ref"]

        return Message(
            title="Merge Group",
            text=(
                f"Merge group {self.action} for `{base_ref}`"
                f" in {self.md_repo}\n\n"
                f"Head: `{head_ref}`"
            ),
        )
