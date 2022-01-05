from typing import List

import coinbasepro

from cbpa.logger import logger
from cbpa.schemas.buy import Buy
from cbpa.schemas.config import Config
from cbpa.schemas.currency import FCC
from cbpa.services.account import AccountService
from cbpa.services.discord import DiscordService


class BuyService:
    MARKET_SIDE = "buy"

    def __init__(
        self,
        config: Config,
        account_service: AccountService,
        coinbasepro_client: coinbasepro.AuthenticatedClient,
    ) -> None:
        self.coinbasepro_client = coinbasepro_client
        self.discord = DiscordService()
        self.config = config
        self.account_service = account_service

    def buy(self, buys: List[Buy], fiat: FCC) -> None:
        for buy in buys:
            self.place_market_order(buy, fiat)

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

    def run(self) -> None:
        buy_total = sum([buy.send_amount for buy in self.config.buys])
        current_funds = self.account_service.get_balance_for_currency(
            self.config.account.fiat_currency
        )
        if current_funds >= buy_total:
            self.buy(self.config.buys, self.config.account.fiat_currency)
        elif current_funds < buy_total:
            response = self.account_service.add_funds(
                buy_total=buy_total,
                current_funds=current_funds,
                max_fund=self.config.account.auto_funding_limit,
                fiat=self.config.account.fiat_currency,
            )
            if response.status == "Error":
                logger.error(response.message)
                self.discord.send_alert(config=self.config, message=response.message)
            elif response.status == "Success":
                self.buy(self.config.buys, self.config.account.fiat_currency)
            else:
                logger.info(f"Unhandled response status {response.status}. Moving on.")
