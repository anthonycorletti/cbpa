import argparse
import os
import traceback
from datetime import datetime

import coinbasepro

from cbpa.logger import logger
from cbpa.schemas.config import Config
from cbpa.services.account import AccountService
from cbpa.services.buy import BuyService
from cbpa.services.config import ConfigService
from cbpa.services.discord import DiscordService

os.environ["TZ"] = "UTC"


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help="filepath to the yaml config")
    return parser.parse_args()


def create_config(args: argparse.Namespace) -> Config:
    config_service = ConfigService()
    logger.info(f"🤓 Reading config file at {args.f}.")
    config = config_service.load_config(filepath=args.f)
    logger.info(f"👏 Successfully parsed {args.f}.")
    return config


def create_coinbasepro_auth_client(config: Config) -> coinbasepro.AuthenticatedClient:
    logger.info("📡 Connecting to Coinbase Pro.")
    client = coinbasepro.AuthenticatedClient(
        key=config.api.key.get_secret_value(),
        secret=config.api.secret.get_secret_value(),
        passphrase=config.api.passphrase.get_secret_value(),
        api_url=config.api.url,
    )
    logger.info("👏 Successfully connected to Coinbase Pro.")
    return client


def create_account_service(
    config: Config, coinbasepro_client: coinbasepro.AuthenticatedClient
) -> AccountService:
    logger.info("🏦 Creating account service.")
    account_service = AccountService(
        config=config,
        coinbasepro_client=coinbasepro_client,
    )
    logger.info("👏 Successfully created account service.")
    return account_service


def create_buy_service(
    config: Config, coinbasepro_client: coinbasepro.AuthenticatedClient
) -> BuyService:
    logger.info("💸 Creating buy service.")
    buy_service = BuyService(
        config=config,
        coinbasepro_client=coinbasepro_client,
    )
    logger.info("👏 Successfully created buy service.")
    return buy_service


def main() -> None:
    start = datetime.now()
    args = get_args()
    config = create_config(args=args)
    discord_service = DiscordService()
    start_message = f"🤖 Starting cbpa ({start.isoformat()})"
    logger.info(start_message)
    discord_service.send_alert(config=config, message=start_message)
    coinbasepro_client = create_coinbasepro_auth_client(config=config)
    account_service = create_account_service(
        config=config, coinbasepro_client=coinbasepro_client
    )
    buy_service = create_buy_service(
        config=config,
        coinbasepro_client=coinbasepro_client,
    )
    done = {buy.receive_currency.value: False for buy in config.buys}

    def run() -> None:
        try:
            for buy in config.buys:
                if not done[buy.receive_currency.value]:
                    buy_total = buy.send_amount
                    current_funds = account_service.get_balance_for_currency(
                        config.account.fiat_currency
                    )
                    if current_funds >= buy_total:
                        buy_service.place_market_order(
                            buy, config.account.fiat_currency
                        )
                        done[buy.receive_currency.value] = True
                    elif current_funds < buy_total:
                        response = account_service.add_funds(
                            buy_total=buy_total,
                            current_funds=current_funds,
                            max_fund=config.account.auto_funding_limit,
                            fiat=config.account.fiat_currency,
                        )
                        if response.status == "Error":
                            logger.error(response.message)
                            discord_service.send_alert(
                                config=config, message=response.message
                            )
                        elif response.status == "Success":
                            buy_service.place_market_order(
                                buy, config.account.fiat_currency
                            )
                            done[buy.receive_currency.value] = True
                        else:
                            logger.info(
                                f"Unhandled response status {response.status}."
                                " Moving on."
                            )
            if not all(done.values()):
                run()
        except Exception:
            logger.error("Unhandled general exception occurred.")
            logger.error(traceback.format_exc())
            run()

    run()
    end = datetime.now()
    duration = end - start
    end_message = f"🤖 cbpa completed! Ran for {duration.total_seconds()} seconds."
    logger.info(end_message)
    discord_service.send_alert(config=config, message=end_message)


if __name__ == "__main__":
    main()  # pragma: no cover
