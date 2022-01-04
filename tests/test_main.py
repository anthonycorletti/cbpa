import argparse
import os
from unittest import mock

from coinbasepro_scheduler.main import main


def test_timezone() -> None:
    assert os.environ["TZ"] == "America/New_York"


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(f="./examples/coinbasepro-scheduler-daily.yaml"),
)
def test_main_daily(mock_args: mock.MagicMock) -> None:
    main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(f="./examples/coinbasepro-scheduler-weekly.yaml"),
)
def test_main_weekly(mock_args: mock.MagicMock) -> None:
    main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(f="./examples/coinbasepro-scheduler-seconds.yaml"),
)
def test_main_seconds(mock_args: mock.MagicMock) -> None:
    main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        f="./examples/coinbasepro-scheduler-daily-discord.yaml"
    ),
)
def test_main_daily_with_discord_alerts(mock_args: mock.MagicMock) -> None:
    main()
