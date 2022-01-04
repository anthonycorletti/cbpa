from typing import List

import coinbasepro

from coinbasepro_scheduler.logger import logger
from coinbasepro_scheduler.schemas.buy import Buy
from coinbasepro_scheduler.schemas.config import Config
from coinbasepro_scheduler.schemas.currency import FCC
from coinbasepro_scheduler.schemas.scheduler import Scheduler
from coinbasepro_scheduler.services.account import AccountService
from coinbasepro_scheduler.services.alert import DiscordAlertService


class BuyService:
    MARKET_SIDE = "buy"

    def __init__(
        self,
        config: Config,
        coinbasepro_client: coinbasepro.AuthenticatedClient,
    ) -> None:
        self.coinbasepro_client = coinbasepro_client
        self.discord = DiscordAlertService()
        self.config = config

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

    def recurring_buy(
        self, scheduler: Scheduler, account_service: AccountService
    ) -> None:
        buy_total = sum([buy.send_amount for buy in scheduler.buys])
        current_funds = account_service.get_balance(scheduler.account.fiat_currency)
        if current_funds >= buy_total:
            self.buy(scheduler.buys, scheduler.account.fiat_currency)
        elif current_funds < buy_total:
            if scheduler.account.auto_funding_enabled:
                response = account_service.add_funds(
                    buy_total=buy_total,
                    current_funds=current_funds,
                    max_fund=scheduler.account.auto_funding_limit,
                    fund_source=scheduler.account.source,
                    fiat=scheduler.account.fiat_currency,
                )
                if response.status == "Error":
                    logger.error(response.message)
                    self.discord.send_alert(
                        config=self.config, message=response.message
                    )
                elif response.status == "Success":
                    self.buy(scheduler.buys, scheduler.account.fiat_currency)
                else:
                    message = (
                        """🚨 Something unexpected occurred when adding funds """
                        """to your account for a recurring purchase."""
                    )
                    logger.error(message)
                    self.discord.send_alert(config=self.config, message=message)
            else:
                funding_msg = (
                    "🚨 Unable to complete your purchase."
                    "Insufficient funds to make purchase and "
                    "Auto-Funding is not enabled."
                    f"Please deposit at least {buy_total} "
                    f"{scheduler.account.fiat_currency} into your account."
                )
                logger.info(funding_msg)
                self.discord.send_alert(config=self.config, message=funding_msg)
