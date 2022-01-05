import argparse
import os

import coinbasepro

from cbpa.logger import logger
from cbpa.schemas.config import Config
from cbpa.services.account import AccountService
from cbpa.services.buy import BuyService
from cbpa.services.config import ConfigService

os.environ["TZ"] = "America/New_York"


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help="filepath to scheduler yaml")
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
    account_service = create_account_service(
        config=config,
        coinbasepro_client=coinbasepro_client,
    )
    buy_service = BuyService(
        config=config,
        coinbasepro_client=coinbasepro_client,
        account_service=account_service,
    )
    logger.info("👏 Successfully created buy service.")
    return buy_service


def main() -> None:
    logger.info("⏰ Starting cbpa.")
    args = get_args()
    config = create_config(args=args)
    coinbasepro_client = create_coinbasepro_auth_client(config=config)
    buy_service = create_buy_service(
        config=config,
        coinbasepro_client=coinbasepro_client,
    )
    buy_service.run()


if __name__ == "__main__":
    main()
