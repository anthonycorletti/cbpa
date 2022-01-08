import time
import traceback
from typing import Dict

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
        coinbasepro_client: coinbasepro.AuthenticatedClient,
        account_service: AccountService,
    ) -> None:
        self.coinbasepro_client = coinbasepro_client
        self.discord_service = DiscordService()
        self.config = config
        self.account_service = account_service

    def place_market_order(self, buy: Buy, fiat: FCC) -> None:
        pair = buy.pair()
        amount = buy.send_amount
        place_order_message = f"💸 Placing market order of {amount} {fiat} for {pair}."
        logger.info(place_order_message)
        response = self.coinbasepro_client.place_market_order(
            product_id=pair, side=self.MARKET_SIDE, funds=amount
        )
        logger.info("Order placed! Getting order details.")
        self.get_placed_order_details(buy=buy, response=response)

    def get_placed_order_details(self, buy: Buy, response: Dict) -> None:
        order_id = response["id"]
        try:
            order_details = self.coinbasepro_client.get_order(order_id=order_id)
            order_filled_size = order_details["filled_size"]
            purchase_success_message = (
                f"👏 Successfully purchased {order_filled_size} of {buy.pair()}."
            )
            logger.info(purchase_success_message)
            self.discord_service.send_alert(
                config=self.config, message=purchase_success_message
            )
        except coinbasepro.exceptions.CoinbaseAPIError as e:
            logger.error(
                f"Coinbase returned an API error: {e}. "
                f"Order {order_id} was not created just yet. "
                "Retrying order detail retrieval in 2 seconds."
            )
            time.sleep(2)
            self.get_placed_order_details(buy=buy, response=response)

    def run(self, done: Dict) -> None:
        try:
            for buy in self.config.buys:
                if not done[buy.receive_currency.value]:
                    buy_total = buy.send_amount
                    current_funds = self.account_service.get_balance_for_currency(
                        self.config.account.fiat_currency
                    )
                    if current_funds >= buy_total:
                        self.place_market_order(buy, self.config.account.fiat_currency)
                        done[buy.receive_currency.value] = True
                    elif current_funds < buy_total:
                        response = self.account_service.add_funds(
                            buy_total=buy_total,
                            current_funds=current_funds,
                            max_fund=self.config.account.auto_funding_limit,
                            fiat=self.config.account.fiat_currency,
                        )
                        if response.status == "Error":
                            logger.error(response.message)
                            self.discord_service.send_alert(
                                config=self.config, message=response.message
                            )
                        elif response.status == "Success":
                            self.place_market_order(
                                buy, self.config.account.fiat_currency
                            )
                            done[buy.receive_currency.value] = True
                        else:
                            logger.info(
                                f"Unhandled response status {response.status}."
                                " Moving on."
                            )
            if not all(done.values()):
                self.run(done=done)
        except Exception:
            logger.error("Unhandled general exception occurred.")
            logger.error(traceback.format_exc())
            self.run(done=done)
