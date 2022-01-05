import json
import math
import time
from typing import Union

import coinbasepro

from cbpa.logger import logger
from cbpa.schemas.account import AddFundsResponse
from cbpa.schemas.config import Config
from cbpa.schemas.currency import CCC, FCC
from cbpa.services.discord import DiscordService


class AccountService:
    def __init__(
        self, config: Config, coinbasepro_client: coinbasepro.AuthenticatedClient
    ) -> None:
        self.coinbasepro_client = coinbasepro_client
        self.config = config
        self.discord = DiscordService()

    def get_balance_for_currency(self, currency: Union[CCC, FCC]) -> int:
        """get_balance_for_currency

        Assuming there will only every be one account for a currency identifier.
        This account is not the same as a payment method.
        Think of it as just the allocation of a currency.
        """
        return [
            math.floor(account["balance"])
            for account in self.coinbasepro_client.get_accounts()
            if account["currency"] == currency.value
        ][0]

    def get_primary_buy_payment_method_id(self, fiat: FCC) -> str:
        return [
            primary_method["id"]
            for primary_method in self.coinbasepro_client.get_payment_methods()
            if primary_method["primary_buy"]
            and primary_method["currency"] == fiat.value
        ][0]

    def add_funds(
        self,
        buy_total: int,
        current_funds: int,
        max_fund: int,
        fiat: FCC,
    ) -> AddFundsResponse:
        if buy_total > max_fund:
            message = (
                f"Total cost is {buy_total} {fiat} but you "
                f"have your limit set to {max_fund} {fiat}. "
                "Unable to complete purchase. "
                "Update your settings appropriately to make changes if necessary."
            )
            self.discord.send_alert(config=self.config, message=message)
            return AddFundsResponse(status="Error", message=message)
        else:
            fund_amount = buy_total - current_funds
            if current_funds > 1:
                fund_amount = max_fund
            fund_message = (
                f"Your balance is {current_funds} {fiat}. "
                f"A deposit of {fund_amount} {fiat} will be made "
                "using your selected payment account."
            )
            logger.info(fund_message)
            self.discord.send_alert(config=self.config, message=fund_message)
            payment_id = self.get_primary_buy_payment_method_id(fiat=fiat)
            if payment_id is None:
                return AddFundsResponse(
                    status="Error", message="Could not determine payment account id."
                )
            else:
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
