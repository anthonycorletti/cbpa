import coinbasepro

from cbpa.logger import logger
from cbpa.schemas.buy import Buy
from cbpa.schemas.config import Config
from cbpa.schemas.currency import FCC
from cbpa.services.discord import DiscordService


class BuyService:
    MARKET_SIDE = "buy"

    def __init__(
        self,
        config: Config,
        coinbasepro_client: coinbasepro.AuthenticatedClient,
    ) -> None:
        self.coinbasepro_client = coinbasepro_client
        self.discord = DiscordService()
        self.config = config

    def place_market_order(self, buy: Buy, fiat: FCC) -> None:
        pair = buy.pair()
        amount = buy.send_amount
        place_order_message = f"💸 Placing market order of {amount} {fiat} for {pair}."
        logger.info(place_order_message)
        self.discord.send_alert(config=self.config, message=place_order_message)
        response = self.coinbasepro_client.place_market_order(
            product_id=pair, side=self.MARKET_SIDE, funds=amount
        )
        order_id = response["id"]
        order_details = self.coinbasepro_client.get_order(order_id=order_id)
        order_filled_size = order_details["filled_size"]
        purchase_success_message = (
            f"👏 Successfully purchased {order_filled_size} of {pair}."
        )
        logger.info(purchase_success_message)
        self.discord.send_alert(config=self.config, message=purchase_success_message)
