from discord import RequestsWebhookAdapter, Webhook

from coinbasepro_scheduler.schemas.config import Config


class DiscordAlertService:
    def __init__(self) -> None:
        pass

    def send_alert(self, config: Config, message: str) -> None:
        if config.discord and config.discord.enabled:
            webhook = Webhook.from_url(
                config.discord.webhook,
                adapter=RequestsWebhookAdapter(),
            )
            webhook.send(message)
