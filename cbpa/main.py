import os
from datetime import datetime
from typing import Optional

import coinbasepro
import typer
import uvicorn
import yaml
from fastapi import FastAPI
from google.cloud import secretmanager

from cbpa import __version__
from cbpa.logger import logger
from cbpa.schemas.buy import BuyResponse
from cbpa.schemas.config import Config
from cbpa.schemas.health import HealthcheckResponse
from cbpa.services.account import AccountService
from cbpa.services.buy import BuyService
from cbpa.services.config import ConfigService
from cbpa.services.discord import DiscordService

os.environ["TZ"] = "UTC"


def create_config(filepath: str) -> Config:
    config_service = ConfigService()
    logger.info(f"🤓 Reading config file at {filepath}.")
    config = config_service.load_config(filepath=filepath)
    logger.info(f"👏 Successfully parsed {filepath}.")
    return config


def retrieve_config_from_secret_manager(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> Config:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return Config(**yaml.safe_load(payload))


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
    config: Config,
    coinbasepro_client: coinbasepro.AuthenticatedClient,
    account_service: AccountService,
) -> BuyService:
    logger.info("💸 Creating buy service.")
    buy_service = BuyService(
        config=config,
        coinbasepro_client=coinbasepro_client,
        account_service=account_service,
    )
    logger.info("👏 Successfully created buy service.")
    return buy_service


def _main(config: Config) -> None:
    start = datetime.now()
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
        account_service=account_service,
    )
    done = {buy.receive_currency.value: False for buy in config.buys}

    buy_service.run(done=done)

    end = datetime.now()
    duration = end - start
    end_message = f"🤖 cbpa completed! Ran for {duration.total_seconds()} seconds."
    logger.info(end_message)
    discord_service.send_alert(config=config, message=end_message)


#
#   create the api
#
api = FastAPI(
    title="Coinbase Pro Automation API",
    description="Automate buys for your favourite cryptocurrencies.",
    version=__version__,
)


#
#   create api routes
#
@api.get("/healthcheck", response_model=HealthcheckResponse, tags=["health"])
def healthcheck() -> HealthcheckResponse:
    message = "Dollar cost averaging."
    logger.debug(message)
    return HealthcheckResponse(
        api_version=__version__,
        message=message,
        time=datetime.now(),
    )


@api.post("/buy", response_model=BuyResponse, tags=["buy"])
def buy() -> BuyResponse:
    logger.info("Buy API request initiated.")
    config = retrieve_config_from_secret_manager(
        project_id=os.environ["PROJECT_ID"], secret_id=os.environ["SECRET_ID"]
    )
    _main(config=config)
    logger.info("Buy API request completed.")
    return BuyResponse(message="Buy API request completed.")


#
#   create the cli
#
typer_app_name = "Coinbase Pro Automation"
app = typer.Typer(name=typer_app_name)


#
#   create cli commands
#
@app.command("version", help="prints the version")
def _version() -> None:
    typer.echo(__version__)


@app.command("run", help="executes buy orders listed in a config file")
def _run(
    filepath: str = typer.Option(
        ...,
        "-f",
        "--file",
        help="filepath to the yaml config",
    )
) -> None:
    config = create_config(filepath=filepath)
    _main(config=config)


@app.command("server", help="run an api server to handle automated buys")
def _server(
    port: Optional[str] = typer.Option(
        None, "--port", "-p", help="The port to run uvicorn on."
    ),
    host: str = typer.Option(
        "0.0.0.0", "--host", "-h", help="The host to run uvicorn on."
    ),
) -> None:
    if port is None:
        port = os.getenv("PORT", "8002")
    assert port is not None
    uvicorn.run(api, port=int(port), host=host)
