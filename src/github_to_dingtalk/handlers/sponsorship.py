from github_to_dingtalk.handlers.base import BaseHandler, Message


class SponsorshipHandler(BaseHandler):
    def build_message(self) -> Message:
        sponsorship = self.payload["sponsorship"]
        sponsor = sponsorship["sponsor"]
        sponsor_login = sponsor["login"]
        sponsor_url = sponsor["html_url"]
        md_sponsor = f"[{sponsor_login}]({sponsor_url})"

        tier = sponsorship["tier"]
        tier_name = tier["name"]
        monthly_price = tier["monthly_price_in_dollars"]

        return Message(
            title="Sponsorship",
            text=(
                f"{md_sponsor} sponsorship {self.action}"
                f" - Tier: **{tier_name}** (${monthly_price}/month)"
            ),
        )
