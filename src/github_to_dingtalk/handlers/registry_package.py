from github_to_dingtalk.handlers.base import BaseHandler, Message


class RegistryPackageHandler(BaseHandler):
    def build_message(self) -> Message:
        pkg = self.payload["registry_package"]
        name = pkg["name"]
        package_type = pkg["package_type"]
        html_url = pkg["html_url"]
        version = pkg["package_version"]["version"]

        return Message(
            title="Registry Package",
            text=(
                f"{self.md_sender} {self.action} registry package"
                f" **{name}** ({package_type}) v{version}"
                f" in {self.md_repo}\n\n"
                f"[View]({html_url})"
            ),
        )
