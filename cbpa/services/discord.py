from discord import RequestsWebhookAdapter, Webhook

from cbpa.schemas.config import Config


class DiscordService:
    def __init__(self) -> None:
        pass

    def send_alert(self, config: Config, message: str) -> None:
        if config.discord:
            webhook = Webhook.from_url(
                config.discord.webhook,
                adapter=RequestsWebhookAdapter(),
            )
            webhook.send(message)
