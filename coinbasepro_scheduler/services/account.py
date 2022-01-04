import json
import math
import time
from typing import Optional

import coinbasepro

from coinbasepro_scheduler.logger import logger
from coinbasepro_scheduler.schemas.account import AddFundsResponse, FundSource
from coinbasepro_scheduler.schemas.config import Config
from coinbasepro_scheduler.schemas.currency import FCC
from coinbasepro_scheduler.services.alert import DiscordAlertService


class AccountService:
    def __init__(
        self, config: Config, coinbasepro_client: coinbasepro.AuthenticatedClient
    ) -> None:
        self.coinbasepro_client = coinbasepro_client
        self.config = config
        self.discord = DiscordAlertService()

    def get_balance(self, fiat: FCC) -> int:
        accounts = self.coinbasepro_client.get_accounts()
        for account in accounts:
            if account["currency"] == fiat.value:
                return math.floor(account["balance"])
        return 0

    def get_funding_account(
        self, fund_amount: int, fiat: FCC, fund_source: FundSource
    ) -> Optional[str]:
        if fund_source.value == "default":
            payment_methods = self.coinbasepro_client.get_payment_methods()
            for payment in payment_methods:
                if payment["primary_buy"] is True:
                    return payment["id"]
        elif fund_source.value == "coinbase":
            payment_methods = self.coinbasepro_client.get_coinbase_accounts()
            for payment in payment_methods:
                if (payment["currency"] == fiat.value) and (
                    math.floor(payment["balance"] >= fund_amount)
                ):
                    return payment["id"]
                else:
                    return None
        return None

    def add_funds(
        self,
        buy_total: int,
        current_funds: int,
        max_fund: int,
        fund_source: FundSource,
        fiat: FCC,
    ) -> AddFundsResponse:
        if buy_total > max_fund:
            message = (
                f"Total cost is {buy_total} {fiat} but you "
                f"have your limit set to {max_fund} {fiat}. "
                "Unable to complete purchase. "
                f"Please update coinbasepro_scheduler.yaml if desired."
            )
            self.discord.send_alert(config=self.config, message=message)
            return AddFundsResponse(status="Error", message=message)
        else:
            if current_funds == 0:
                fund_amount = max_fund
            else:
                fund_amount = buy_total - current_funds
            fund_message = (
                f"Your balance is {current_funds} {fiat}. "
                f"A deposit of {fund_amount} {fiat} will be made "
                "using your selected payment account."
            )
            logger.info(fund_message)
            self.discord.send_alert(config=self.config, message=fund_message)
            payment_id = self.get_funding_account(
                fund_amount=fund_amount, fiat=fiat, fund_source=fund_source
            )
            if payment_id is None:
                return AddFundsResponse(
                    status="Error", message="Could not determine payment account id."
                )
            else:
                if fund_source == "coinbase":
                    deposit = self.coinbasepro_client.deposit_from_coinbase(
                        amount=fund_amount,
                        currency=fiat.value,
                        coinbase_account_id=payment_id,
                    )
                    return AddFundsResponse(
                        status="Success",
                        message=json.dumps(deposit, sort_keys=True, default=str),
                    )
                elif fund_source == "default":
                    deposit = self.coinbasepro_client.deposit(
                        amount=fund_amount,
                        currency=fiat.value,
                        payment_method_id=payment_id,
                    )
                    logger.info("Sleeping for 10 seconds while the deposit completes.")
                    time.sleep(10)
                    return AddFundsResponse(
                        status="Success",
                        message=json.dumps(deposit, sort_keys=True, default=str),
                    )
                else:
                    return AddFundsResponse(
                        status="Error",
                        message="Something went wrong attempting to add funds "
                        f"from unidentified fund source {fund_source}.",
                    )
