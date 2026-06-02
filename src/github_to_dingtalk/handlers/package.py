from github_to_dingtalk.handlers.base import BaseHandler, Message


class PackageHandler(BaseHandler):
    def build_message(self) -> Message:
        package = self.payload["package"]
        name = package["name"]
        package_type = package["package_type"]
        html_url = package["html_url"]
        package_version = package.get("package_version") or {}
        version = package_version.get("version") or ""

        return Message(
            title="Package",
            text=(
                f"{self.md_sender} {self.action} package"
                f" **{name}** ({package_type}) v{version}"
                f" in {self.md_repo}\n\n"
                f"[View package]({html_url})"
            ),
        )
