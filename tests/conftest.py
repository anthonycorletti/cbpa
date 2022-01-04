import os

import pytest

from coinbasepro_scheduler.services.config import ConfigService

os.environ["TZ"] = "America/New_York"
config_service = ConfigService()


@pytest.fixture(scope="function", autouse=True)
def _function() -> None:
    pass
