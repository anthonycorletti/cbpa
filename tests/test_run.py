import os
from unittest import mock

from typer.testing import CliRunner

from cbpa.main import app
from tests.mocks import MockCoinbaseClient


def test_timezone() -> None:
    assert os.environ["TZ"] == "UTC"


@mock.patch(
    "cbpa.main.create_coinbasepro_auth_client",
    return_value=MockCoinbaseClient(),
)
@mock.patch(
    "cbpa.services.discord.DiscordService.send_alert",
    return_value=None,
)
def test_run_with_alerts(
    mock_discord_service: mock.MagicMock,
    mock_coinbase_client: mock.MagicMock,
    cli_runner: CliRunner,
) -> None:
    cli_runner.invoke(app, ["run", "-f", "./examples/cbpa.yaml"])


@mock.patch(
    "cbpa.main.create_coinbasepro_auth_client",
    return_value=MockCoinbaseClient(),
)
@mock.patch(
    "cbpa.services.discord.DiscordService.send_alert",
    return_value=None,
)
def test_run_without_alerts(
    mock_discord_service: mock.MagicMock,
    mock_coinbase_client: mock.MagicMock,
    cli_runner: CliRunner,
) -> None:
    cli_runner.invoke(app, ["run", "-f", "./examples/cbpa-no-alerts.yaml"])


@mock.patch(
    "cbpa.main.create_coinbasepro_auth_client",
    return_value=MockCoinbaseClient(),
)
@mock.patch(
    "cbpa.services.discord.DiscordService.send_alert",
    return_value=None,
)
def test_run_trigger_over_limit(
    mock_discord_service: mock.MagicMock,
    mock_coinbase_client: mock.MagicMock,
    cli_runner: CliRunner,
) -> None:
    cli_runner.invoke(app, ["run", "-f", "./examples/cbpa-trigger-over-limit.yaml"])


@mock.patch(
    "cbpa.main.create_coinbasepro_auth_client",
    return_value=MockCoinbaseClient(),
)
@mock.patch(
    "cbpa.services.discord.DiscordService.send_alert",
    return_value=None,
)
def test_run_trigger_deposit(
    mock_discord_service: mock.MagicMock,
    mock_coinbase_client: mock.MagicMock,
    cli_runner: CliRunner,
) -> None:
    cli_runner.invoke(app, ["run", "-f", "./examples/cbpa-trigger-deposit.yaml"])
