import argparse
import os
import time

import coinbasepro
import schedule

from coinbasepro_scheduler.logger import logger
from coinbasepro_scheduler.schemas.config import Config
from coinbasepro_scheduler.services.account import AccountService
from coinbasepro_scheduler.services.alert import DiscordAlertService
from coinbasepro_scheduler.services.buy import BuyService
from coinbasepro_scheduler.services.config import ConfigService
from coinbasepro_scheduler.services.scheduler import SchedulerService

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
    buy_service = BuyService(
        config=config,
        coinbasepro_client=coinbasepro_client,
    )
    logger.info("👏 Successfully created buy service.")
    return buy_service


def create_scheduler_service() -> SchedulerService:
    logger.info("⏰ Creating scheduler service.")
    scheduler_service = SchedulerService()
    logger.info("👏 Successfully created scheduler service.")
    return scheduler_service


def main() -> None:
    logger.info("⏰ Starting coinbasepro_scheduler.")
    args = get_args()
    config = create_config(args=args)
    coinbasepro_client = create_coinbasepro_auth_client(config=config)
    account_service = create_account_service(
        config=config,
        coinbasepro_client=coinbasepro_client,
    )
    buy_service = create_buy_service(
        config=config,
        coinbasepro_client=coinbasepro_client,
    )
    scheduler_service = create_scheduler_service()
    logger.info("📝 Setting schedules.")
    for scheduler in config.schedulers:
        scheduler_service.set_schedules(
            scheduler=scheduler,
            buy_service=buy_service,
            account_service=account_service,
        )


def run() -> None:
    args = get_args()
    config = create_config(args=args)
    discord = DiscordAlertService()
    try:
        main()  # pragma: no cover
        logger.info("🏃 Running schedules.")  # pragma: no cover
        while True:  # pragma: no cover
            schedule.run_pending()  # pragma: no cover
            time.sleep(1)  # pragma: no cover
    except Exception as e:
        fail_message = (
            f"🙈 Scheduler failed on an exception, {e}. Automatically restarting."
        )
        logger.error(fail_message)
        discord.send_alert(config=config, message=fail_message)
        run()


if __name__ == "__main__":
    run()
