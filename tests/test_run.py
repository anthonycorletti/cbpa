import argparse
import os
from unittest import mock

from cbpa.main import main
from tests.mocks import MockCoinbaseClient


def test_timezone() -> None:
    assert os.environ["TZ"] == "America/New_York"


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(f="./examples/cbpa.yaml"),
)
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
    mock_args: mock.MagicMock,
) -> None:
    main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(f="./examples/cbpa-no-alerts.yaml"),
)
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
    mock_args: mock.MagicMock,
) -> None:
    main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(f="./examples/cbpa-trigger-over-limit.yaml"),
)
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
    mock_args: mock.MagicMock,
) -> None:
    main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(f="./examples/cbpa-trigger-deposit.yaml"),
)
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
    mock_args: mock.MagicMock,
) -> None:
    main()
